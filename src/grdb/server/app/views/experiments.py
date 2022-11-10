import json

from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_

from grdb.database.models import (
    Furnace, Substrate, EnvironmentConditions, Recipe, PreparationStep, Experiment, Author, SemFile, SemAnalysis,
    Software, RamanFile, RamanAnalysis, Properties
)

from .. import read_db, write_db, s3

experiments = Blueprint('experiments', __name__, url_prefix='/experiments')
CORS(experiments)


@experiments.route('/init', methods=['GET'])
def tool_init():
    db = read_db.Session()
    env_conditions = db.query(EnvironmentConditions).order_by(EnvironmentConditions.id.desc()).all()
    env_conditions_json = [env_condition.json_encodable() for env_condition in env_conditions]

    furnaces = db.query(Furnace).order_by(Furnace.id.desc()).all()
    furnaces_json = [f.json_encodable() for f in furnaces]

    properties = db.query(Properties).order_by(Properties.id.desc()).all()
    properties_json = [p.json_encodable() for p in properties]

    recipes = db.query(Recipe).order_by(Recipe.id.desc()).all()
    recipes_json = []
    for r in recipes:
        recipe_json = r.json_encodable()
        prep_steps = r.preparation_steps
        prep_steps_json = [p.json_encodable() for p in prep_steps]
        recipe_json['preparation_steps'] = prep_steps_json
        recipes_json.append(recipe_json)

    substrates = db.query(Substrate).order_by(Substrate.id.desc()).all()
    substrates_json = [s.json_encodable() for s in substrates]

    authors = db.query(Author).order_by(Author.id.desc()).all()
    authors_json = [a.json_encodable() for a in authors]
    db.close()
    return {
        'environment_conditions': env_conditions_json,
        'furnaces': furnaces_json,
        'properties': properties_json,
        'recipes': recipes_json,
        'substrates': substrates_json,
        'authors': authors_json,
    }


@experiments.route('/submit', methods=['POST'])
def submit_experiment():
    db = write_db.Session()
    data = dict(request.form).get('experimentData')
    data = json.loads(data)
    uploaded_files = request.files

    try:
        if data.get('useCustomEnvironmentConditions'):
            ambient_temperature = data.get('ambientTemperature') if data.get('ambientTemperature') else None
            dew_point = data.get('dewPoint') if data.get('dewPoint') else None
            env_con = EnvironmentConditions(dew_point=dew_point,
                                            ambient_temperature=ambient_temperature)
            db.add(env_con)
            db.flush()
            environment_conditions_id = env_con.id
        else:
            environment_conditions_id = data.get('environmentConditionsNumber')

        if data.get('useCustomFurnace'):
            tube_diameter = data.get('tubeDiameter') if data.get('tubeDiameter') else None
            cross_sectional_area = data.get('crossSectionalArea') if data.get('crossSectionalArea') else None
            tube_length = data.get('tubeLength') if data.get('tubeLength') else None
            length_of_heated_region = data.get('lengthOfHeatedRegion') if data.get('lengthOfHeatedRegion') else None
            furnace = Furnace(tube_diameter=tube_diameter,
                              cross_sectional_area=cross_sectional_area,
                              tube_length=tube_length,
                              length_of_heated_region=length_of_heated_region)
            db.add(furnace)
            db.flush()
            furnace_id = furnace.id
        else:
            furnace_id = data.get('furnaceNumber')

        if data.get('useCustomSubstrate'):
            catalyst = data.get('catalyst') if data.get('catalyst') else None
            thickness = data.get('thickness') if data.get('thickness') else None
            diameter = data.get('diameter') if data.get('diameter') else None
            length = data.get('length') if data.get('length') else None
            surface_area = data.get('surfaceArea') if data.get('surfaceArea') else None
            substrate = Substrate(catalyst=catalyst,
                                  thickness=thickness,
                                  diameter=diameter,
                                  length=length,
                                  surface_area=surface_area)
            db.add(substrate)
            db.flush()
            substrate_id = substrate.id
        else:
            substrate_id = data.get('substrateNumber')

        if data.get('useCustomRecipe'):
            carbon_source = data.get('carbonSource') if data.get('carbonSource') else None
            base_pressure = data.get('basePressure') if data.get('basePressure') else None
            recipe = Recipe(carbon_source=carbon_source,
                            base_pressure=base_pressure)
            db.add(recipe)
            db.flush()  # flush to get recipe.id
            recipe_id = recipe.id
        else:
            recipe_id = data.get('recipeNumber')

        for i, prep_step in enumerate(data.get('preparationSteps')):
            name = prep_step.get('name') if prep_step.get('name') else None
            duration = prep_step.get('duration') if prep_step.get('duration') else None
            furnace_temperature = prep_step.get('furnaceTemperature') if prep_step.get('furnaceTemperature') else None
            furnace_pressure = prep_step.get('furnacePressure') if prep_step.get('furnacePressure') else None
            sample_location = prep_step.get('sampleLocation') if prep_step.get('sampleLocation') else None
            helium_flow_rate = prep_step.get('heliumFlowRate') if prep_step.get('heliumFlowRate') else None
            hydrogen_flow_rate = prep_step.get('hydrogenFlowRate') if prep_step.get('hydrogenFlowRate') else None
            carbon_source_flow_rate = prep_step.get('carbonSourceFlowRate') \
                if prep_step.get('carbonSourceFlowRate') else None
            argon_flow_rate = prep_step.get('argonFlowRate') if prep_step.get('argonFlowRate') else None
            cooling_rate = prep_step.get('coolingRate') if prep_step.get('coolingRate') else None
            preparation_step = PreparationStep(recipe_id=recipe_id,
                                               step=i,
                                               name=name,
                                               duration=duration,
                                               furnace_temperature=furnace_temperature,
                                               furnace_pressure=furnace_pressure,
                                               sample_location=sample_location,
                                               helium_flow_rate=helium_flow_rate,
                                               hydrogen_flow_rate=hydrogen_flow_rate,
                                               carbon_source_flow_rate=carbon_source_flow_rate,
                                               argon_flow_rate=argon_flow_rate,
                                               cooling_rate=cooling_rate)
            db.add(preparation_step)

        experiment = Experiment(recipe_id=recipe_id,
                                environment_conditions_id=environment_conditions_id,
                                substrate_id=substrate_id,
                                furnace_id=furnace_id,
                                submitted_by=data.get('authors')[0].get('id'),
                                experiment_date=datetime.now(),
                                material_name=data.get('materialName'))
        db.add(experiment)
        db.flush()  # flush to get experiment.id
        author_ids = list(map(lambda x: x['id'], data.get('authors')))
        authors = db.query(Author).filter(Author.id.in_(author_ids)).all()
        for author in authors:
            experiment.authors.append(author)

        if data.get('useCustomProperties'):
            average_thickness_of_growth = data.get('avgThicknessOfGrowth') if data.get('avgThicknessOfGrowth') else None
            standard_deviation_of_growth = data.get('stdDevOfGrowth') if data.get('stdDevOfGrowth') else None
            number_of_layers = data.get('numberOfLayers') if data.get('numberOfLayers') else None
            growth_coverage = data.get('growthCoverage') if data.get('growthCoverage') else None
            domain_size = data.get('domainSize') if data.get('domainSize') else None
            shape = data.get('shape') if data.get('shape') else None
            properties = Properties(experiment_id=experiment.id,
                                    average_thickness_of_growth=average_thickness_of_growth,
                                    standard_deviation_of_growth=standard_deviation_of_growth,
                                    number_of_layers=number_of_layers,
                                    growth_coverage=growth_coverage,
                                    domain_size=domain_size,
                                    shape=shape)
            db.add(properties)
            db.flush()
        else:
            properties = db.query(Properties).filter_by(id=data.get('propertiesNumber')).first()
            new_properties = Properties(experiment_id=experiment.id,
                                        average_thickness_of_growth=properties.average_thickness_of_growth,
                                        standard_deviation_of_growth=properties.standard_deviation_of_growth,
                                        number_of_layers=properties.number_of_layers,
                                        growth_coverage=properties.growth_coverage,
                                        domain_size=properties.domain_size,
                                        shape=properties.shape)
            db.add(new_properties)

        i = 1
        for filename, file in uploaded_files.items():
            object_name = s3.generate_object_name(filename, i)
            sem_file = SemFile(s3_object_name=object_name)
            db.add(sem_file)
            sem_file.experiment = experiment
            s3.upload_file(file, object_name)
            i += 1
        db.commit()
    except Exception as e:
        db.rollback()
        db.close()
        return make_response("Error occurred", 400)
    db.close()
    return make_response("Submission successful", 200)


@experiments.route('/<int:experiment_id>', methods=['GET'])
def get_experiment(experiment_id):
    db = read_db.Session()

    experiment = db.query(Experiment).filter_by(id=experiment_id).first()
    experiment_json = experiment.json_encodable()

    raman_files = db.query(RamanFile).filter_by(experiment_id=experiment.id).all()

    raman_files_json = []
    for raman_file in raman_files:
        raman_files_json.append(raman_file.read_file())

    sem_files = db.query(SemFile).filter_by(experiment_id=experiment.id).all()
    sem_file_urls = []
    for sem_file in sem_files:
        if sem_file.s3_object_name:
            sem_file_urls.append(s3.create_presigned_url(sem_file.s3_object_name))

    db.close()
    data = {
        'experiment': experiment_json,
        'raman_files': raman_files_json,
        'sem_file_urls': sem_file_urls
    }
    return jsonify(data)


@experiments.route('/query', methods=['POST'])
def query_experiments():
    filters = request.get_json()
    db = read_db.Session()
    author_filters = []
    property_filters = []
    environmental_condition_filters = []
    furnace_filters = []
    recipe_filters = []
    substrate_filters = []
    for filt in filters:
        category = filt['category']
        if category == 'author':
            author_filters.append(filt)
        elif category == 'property':
            property_filters.append(filt)
        elif category == 'environmentCondition':
            environmental_condition_filters.append(filt)
        elif category == 'furnace':
            furnace_filters.append(filt)
        elif category == 'recipe': # TODO: how to filter recipe?
            recipe_filters.append(filt)
        elif category == 'substrate':
            substrate_filters.append(filt)

    def extract_first_elem(x):
        return list(map(lambda x: x[0], x))

    exp_ids = set(extract_first_elem(db.query(Experiment.id).all()))  # set of all experiment ids

    '''    QUERYING AUTHOR FILTERS    '''
    if author_filters:
        author_ids = list(map(lambda x: x['id'], author_filters))
        result = db.query(Experiment.id).filter(Experiment.authors.any(Author.id.in_(author_ids))).all()
        exp_ids_satisfying_furnace_filters = extract_first_elem(result)
        exp_ids.intersection_update(exp_ids_satisfying_furnace_filters)

    '''    QUERYING FURNACE FILTERS    '''
    if furnace_filters:
        query = db.query(Experiment.id).join(Furnace)
        for furnace_filter in furnace_filters:
            filter_name = furnace_filter['name']
            if 'Tube Diameter' in filter_name:
                query = query \
                    .filter(and_(Furnace.tube_diameter >= furnace_filter['min'],
                                 Furnace.tube_diameter <= furnace_filter['max']))
            elif 'Cross Sectional Area' in filter_name:
                query = query \
                    .filter(and_(Furnace.cross_sectional_area >= furnace_filter['min'],
                                 Furnace.cross_sectional_area <= furnace_filter['max']))
            elif 'Tube Length' in filter_name:
                query = query \
                    .filter(and_(Furnace.tube_length >= furnace_filter['min'],
                                 Furnace.tube_length <= furnace_filter['max']))
            elif 'Length of Heated Region' in filter_name:
                query = query \
                    .filter(and_(Furnace.length_of_heated_region >= furnace_filter['min'],
                                 Furnace.length_of_heated_region <= furnace_filter['max']))
            else:
                pass
        exp_ids_satisfying_furnace_filters = extract_first_elem(query.all())
        exp_ids.intersection_update(exp_ids_satisfying_furnace_filters)

    '''    QUERYING SUBSTRATE FILTERS  '''
    if substrate_filters:
        query = db.query(Experiment.id).join(Substrate)
        for substrate_filter in substrate_filters:
            filter_name = substrate_filter['name']
            if 'Catalyst' in filter_name:
                query = query \
                    .filter(Substrate.catalyst == substrate_filter['value'])
            elif 'Thickness' in filter_name:
                query = query \
                    .filter(and_(Substrate.thickness >= substrate_filter['min'],
                                 Substrate.thickness <= substrate_filter['max']))
            elif 'Diameter' in filter_name:
                query = query \
                    .filter(and_(Substrate.diameter >= substrate_filter['min'],
                                 Substrate.diameter <= substrate_filter['max']))
            elif 'Length' in filter_name:
                query = query \
                    .filter(and_(Substrate.length >= substrate_filter['min'],
                                 Substrate.length <= substrate_filter['max']))
            elif 'Surface Area' in filter_name:
                query = query \
                    .filter(and_(Substrate.surface_area >= substrate_filter['min'],
                                 Substrate.surface_area <= substrate_filter['max']))
            else:
                pass
        exp_ids_satisfying_substrate_filters = extract_first_elem(query.all())
        exp_ids.intersection_update(exp_ids_satisfying_substrate_filters)

    '''    QUERYING PROPERTY FILTERS    '''
    if property_filters:
        query = db.query(Experiment.id).join(Properties)
        for property_filter in property_filters:
            filter_name = property_filter['name']
            if filter_name == 'Shape':
                query = query \
                    .filter(Properties.shape == property_filter['value'])
            elif 'Average Thickness of Growth' in filter_name:
                query = query \
                    .filter(and_(Properties.average_thickness_of_growth >= property_filter['min'],
                                 Properties.average_thickness_of_growth <= property_filter['max']))
            elif 'Std. Dev. of Growth' in filter_name:
                query = query \
                    .filter(and_(Properties.standard_deviation_of_growth >= property_filter['min'],
                                 Properties.standard_deviation_of_growth <= property_filter['max']))
            elif 'Number of Layers' == filter_name:
                query = query \
                    .filter(Properties.number_of_layers == property_filter['value'])
            elif 'Growth Coverage' in filter_name:
                query = query \
                    .filter(and_(Properties.growth_coverage >= property_filter['min'],
                                 Properties.growth_coverage <= property_filter['max']))
            elif 'Domain Size' in filter_name:
                query = query \
                    .filter(and_(Properties.domain_size >= property_filter['min'],
                                 Properties.domain_size <= property_filter['max']))

        exp_ids_satisfying_property_filters = extract_first_elem(query.all())
        exp_ids.intersection_update(exp_ids_satisfying_property_filters)
    
    '''    QUERYING ENVIRONMENT CONDITIONS FILTERS    '''
    if environmental_condition_filters:
        query = db.query(Experiment.id).join(EnvironmentConditions)
        for environmental_condition_filter in environmental_condition_filters:
            filter_name = environmental_condition_filter['name']
            if 'Dew Point' in filter_name:
                query = query \
                    .filter(and_(EnvironmentConditions.dew_point, EnvironmentConditions.dew_point >= environmental_condition_filter['min'],
                                 EnvironmentConditions.dew_point <= environmental_condition_filter['max']))
            elif 'Ambient Temperature' in filter_name:
                query = query \
                    .filter(and_(EnvironmentConditions.ambient_temperature, EnvironmentConditions.ambient_temperature >= environmental_condition_filter['min'],
                                 EnvironmentConditions.ambient_temperature <= environmental_condition_filter['max']))
        exp_ids_satisfying_environmental_condition_filters = extract_first_elem(query.all())
        exp_ids.intersection_update(exp_ids_satisfying_environmental_condition_filters)    

    '''    QUERYING RECIPE FILTERS    '''
    if recipe_filters:
        query = db.query(Experiment.id).join(Recipe)
        for recipe_filter in recipe_filters:
            filter_name = recipe_filter['name']
            if filter_name == 'Carbon Source' :
                query = query \
                    .filter(Recipe.carbon_source == recipe_filter['value'])
            elif 'Base Pressure' in filter_name:
                query = query \
                    .filter(and_(Recipe.base_pressure >= recipe_filter['min'],
                                 Recipe.base_pressure <= recipe_filter['max']))
            elif 'Inert Gas' in filter_name:
                if 'Argon' in recipe_filter['value']:
                    query = query \
                        .filter(Recipe.uses_argon == True)
                elif 'Helium' in recipe_filter['value']:
                    query = query \
                        .filter(Recipe.uses_helium == True)
            elif 'Maximum Temperature' in filter_name:
                query = query \
                    .filter(and_(Recipe.maximum_temperature >= recipe_filter['min'],
                                 Recipe.maximum_temperature <= recipe_filter['max']))
            elif 'Maximum Pressure' in filter_name:
                query = query \
                    .filter(and_(Recipe.maximum_pressure >= recipe_filter['min'],
                                 Recipe.maximum_pressure <= recipe_filter['max']))
            elif 'Max Flow Rate' in filter_name:
                query = query \
                    .filter(and_(Recipe.max_flow_rate >= recipe_filter['min'],
                                 Recipe.max_flow_rate <= recipe_filter['max']))
            elif 'Growth Duration' in filter_name:
                query = query \
                    .filter(and_(Recipe.growth_duration >= recipe_filter['min'],
                                 Recipe.growth_duration <= recipe_filter['max']))
            elif 'Carbon Source Flow Rate' in filter_name:
                query = query \
                    .filter(and_(Recipe.carbon_source_flow_rate >= recipe_filter['min'],
                                 Recipe.carbon_source_flow_rate <= recipe_filter['max']))
        #for row in query.all():
        #    print(row)
        exp_ids_satisfying_recipe_filters = extract_first_elem(query.all())
        exp_ids.intersection_update(exp_ids_satisfying_recipe_filters)

    db.close()
    res = db.query(Experiment).filter(Experiment.id.in_(exp_ids)).all()
    res = [r.json_encodable() for r in res]

    return jsonify(res)
