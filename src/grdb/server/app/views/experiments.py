from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_

from grdb.database.models import (
    Furnace, Substrate, EnvironmentConditions, Recipe, PreparationStep, Experiment, Author, SemFile, SemAnalysis,
    Software, RamanFile, RamanAnalysis, Properties
)
# from .utils import aws_s3
from .. import read_db, write_db

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
    body = request.get_json()
    try:
        if body.get('useCustomEnvironmentConditions'):
            ambient_temperature = body.get('useCustomEnvironmentConditions') \
                if body.get('useCustomEnvironmentConditions') else None
            dew_point = body.get('ambientTemperature') if body.get('ambientTemperature') else None
            env_con = EnvironmentConditions(dew_point=dew_point,
                                            ambient_temperature=ambient_temperature)
            db.add(env_con)
            db.flush()
            environment_conditions_id = env_con.id
        else:
            environment_conditions_id = body.get('environmentConditionsNumber')

        if body.get('useCustomFurnace'):
            tube_diameter = body.get('tubeDiameter') if body.get('tubeDiameter') else None
            cross_sectional_area = body.get('crossSectionalArea') if body.get('crossSectionalArea') else None
            tube_length = body.get('tubeLength') if body.get('tubeLength') else None
            length_of_heated_region = body.get('lengthOfHeatedRegion') if body.get('lengthOfHeatedRegion') else None
            furnace = Furnace(tube_diameter=tube_diameter,
                              cross_sectional_area=cross_sectional_area,
                              tube_length=tube_length,
                              length_of_heated_region=length_of_heated_region)
            db.add(furnace)
            db.flush()
            furnace_id = furnace.id
        else:
            furnace_id = body.get('furnaceNumber')

        if body.get('useCustomSubstrate'):
            catalyst = body.get('catalyst') if body.get('catalyst') else None
            thickness = body.get('thickness') if body.get('thickness') else None
            diameter = body.get('diameter') if body.get('diameter') else None
            length = body.get('length') if body.get('length') else None
            surface_area = body.get('surfaceArea') if body.get('surfaceArea') else None
            substrate = Substrate(catalyst=catalyst,
                                  thickness=thickness,
                                  diameter=diameter,
                                  length=length,
                                  surface_area=surface_area)
            db.add(substrate)
            db.flush()
            substrate_id = substrate.id
        else:
            substrate_id = body.get('substrateNumber')

        if body.get('useCustomRecipe'):
            carbon_source = body.get('carbonSource') if body.get('carbonSource') else None
            base_pressure = body.get('basePressure') if body.get('basePressure') else None
            recipe = Recipe(carbon_source=carbon_source,
                            base_pressure=base_pressure)
            db.add(recipe)
            db.flush()  # flush to get recipe.id
            recipe_id = recipe.id
        else:
            recipe_id = body.get('recipeNumber')

        for i, prep_step in enumerate(body.get('preparationSteps')):
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
                                submitted_by=body.get('authors')[0].get('id'),
                                experiment_date=datetime.now(),
                                material_name=body.get('material_name'))
        db.add(experiment)
        db.flush()  # flush to get experiment.id

        if body.get('useCustomProperties'):
            average_thickness_of_growth = body.get('avgThicknessOfGrowth') if body.get('avgThicknessOfGrowth') else None
            standard_deviation_of_growth = body.get('stdDevOfGrowth') if body.get('stdDevOfGrowth') else None
            number_of_layers = body.get('numberOfLayers') if body.get('numberOfLayers') else None
            growth_coverage = body.get('growthCoverage') if body.get('growthCoverage') else None
            domain_size = body.get('domainSize') if body.get('domainSize') else None
            shape = body.get('shape') if body.get('shape') else None
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
            properties = db.query(Properties).filter_by(id=body.get('propertiesNumber')).first()
            new_properties = Properties(experiment_id=experiment.id,
                                        average_thickness_of_growth=properties.average_thickness_of_growth,
                                        standard_deviation_of_growth=properties.standard_deviation_of_growth,
                                        number_of_layers=properties.number_of_layers,
                                        growth_coverage=properties.growth_coverage,
                                        domain_size=properties.domain_size,
                                        shape=properties.shape)
            db.add(new_properties)
        db.commit()
    except Exception as e:
        db.rollback()
        return make_response("Error occurred", 400)
    db.close()
    return make_response("Submission successful", 200)


@experiments.route('/<int:experiment_id>', methods=['GET'])
def get_experiment(experiment_id):
    db = read_db.Session()

    experiment = db.query(Experiment).filter_by(id=experiment_id).first()
    experiment_json = experiment.json_encodable()

    raman_files = db.query(RamanFile).filter_by(experiment_id=experiment.id).all()
    # raman_files = []

    raman_files_json = []
    for raman_file in raman_files:
        raman_files_json.append(raman_file.read_file())

    sem_files = db.query(SemFile).filter_by(experiment_id=experiment.id).all()
    sem_file_urls = [sem_file.url for sem_file in sem_files]
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
        elif category == 'environmentalCondition':
            environmental_condition_filters.append(filt)
        elif category == 'furnace':
            furnace_filters.append(filt)
        # elif category == 'recipe': TODO: how to filter recipe?
        #     recipe_filters.append(filt)
        elif category == 'substrate':
            property_filters.append(filt)

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
                    .filter(and_(Substrate.thickness >= furnace_filter['min'],
                                 Substrate.thickness <= furnace_filter['max']))
            elif 'Diameter' in filter_name:
                query = query \
                    .filter(and_(Substrate.diameter >= furnace_filter['min'],
                                 Substrate.diameter <= furnace_filter['max']))
            elif 'Length' in filter_name:
                query = query \
                    .filter(and_(Substrate.length >= furnace_filter['min'],
                                 Substrate.length <= furnace_filter['max']))
            elif 'Surface Area' in filter_name:
                query = query \
                    .filter(and_(Substrate.surface_area >= furnace_filter['min'],
                                 Substrate.surface_area <= furnace_filter['max']))
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

    db.close()
    res = db.query(Experiment).filter(Experiment.id.in_(exp_ids)).all()
    res = [r.json_encodable() for r in res]
    return jsonify(res)
