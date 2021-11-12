import json
from flask import Blueprint, jsonify, request
from flask_cors import CORS
from src.grdb.database.models import (
    Furnace, Substrate, EnvironmentConditions, Recipe, PreparationStep, Experiment, Author, SemFile, SemAnalysis,
    Software, RamanFile, RamanAnalysis, Properties, User
)

from .. import read_db, write_db
from .utils.query import query_experiment_data

index = Blueprint('index', __name__, url_prefix='/')
CORS(index)


@index.route('/db/tables/all', methods=['GET'])
def all_tables():
    env_conditions = EnvironmentConditions.query.all()
    env_conditions_json = [env_condition.json_encodable() for env_condition in env_conditions]

    furnaces = Furnace.query.all()
    furnaces_json = [f.json_encodable() for f in furnaces]

    properties = Properties.query.all()
    properties_json = [p.json_encodable() for p in properties]

    recipes = Recipe.query.all()
    recipes_json = []
    for r in recipes:
        recipe_json = r.json_encodable()
        prep_steps = r.preparation_steps
        prep_steps_json = [p.json_encodable() for p in prep_steps]
        recipe_json['preparation_steps'] = prep_steps_json
        recipes_json.append(recipe_json)

    substrates = Substrate.query.all()
    substrates_json = [s.json_encodable() for s in substrates]
    return {
        'environmental_conditions': env_conditions_json,
        'furnaces': furnaces_json,
        'properties': properties_json,
        'recipes': recipes_json,
        'substrates': substrates_json
    }


@index.route('/experiments/filtered/webapp', methods=['POST'])
def filtered_experiments():
    body = request.get_json()
    environmental_condition_filters = body.get('environmentalConditionFilters')
    furnace_filters = body.get('furnaceFilters')
    substrate_filters = body.get('substrateFilters')
    recipe_filters = body.get('recipeFilters')

    session = read_db.Session()
    q = session.query(Experiment)

    if environmental_condition_filters:
        env_cond_ids = [evn_cond.get('id') for evn_cond in environmental_condition_filters]
        q = q.filter(Experiment.environment_conditions_id.in_(env_cond_ids))

    if furnace_filters:
        furnace_ids = [furnace.get('id') for furnace in furnace_filters]
        q = q.filter(Experiment.furnace_id.in_(furnace_ids))

    if substrate_filters:
        substrate_ids = [substrate.get('id') for substrate in substrate_filters]
        q = q.filter(Experiment.furnace_id.in_(substrate_ids))

    if recipe_filters:
        recipe_ids = [recipe.get('id') for recipe in recipe_filters]
        q = q.filter(Experiment.recipe_id.in_(recipe_ids))

    experiments = q.all()
    experiments_json = [experiment.json_encodable() for experiment in experiments]
    return jsonify(experiments_json)


@index.route('/experiments/data', methods=['GET'])
def experiment_data():
    params = request.args
    session = read_db.Session()
    q = session.query(Experiment)

    # CURRENTLY SUPPORTED COLUMNS: recipe, substrate, furnace
    experiments = query_experiment_data(q, params)
    output = []
    for e in experiments:
        exp_dict = {'carbon_source': None,
                    'base_pressure': None,
                    'catalyst': None,
                    'dew_point': None,
                    'ambient_temperature': None,
                    'thickness': None,
                    'diameter': None,
                    'length': None,
                    'surface_area': None,
                    'tube_diameter': None,
                    'cross_sectional_area': None,
                    'tube_length': None,
                    'length_of_heated_region': None,
                    'average_thickness_of_growth': None,
                    'standard_deviation_of_growth': None,
                    'number_of_layers': None,
                    'growth_coverage': None,
                    'domain_size': None,
                    'shape': None,
                    'date': e.experiment_date,
                    'material': e.material_name
                    }
        if e.recipe:
            exp_dict['carbon_source'] = e.recipe.carbon_source
            exp_dict['base_pressure'] = e.recipe.base_pressure
        if e.substrate:
            exp_dict['catalyst'] = e.substrate.catalyst
            exp_dict['thickness'] = e.substrate.thickness
            exp_dict['diameter'] = e.substrate.diameter
            exp_dict['length'] = e.substrate.length
            exp_dict['surface_area'] = e.substrate.surface_area
        if e.environment_conditions:
            exp_dict['dew_point'] = e.environment_conditions.dew_point
            exp_dict['ambient_temperature'] = e.environment_conditions.ambient_temperature
        if e.furnace:
            exp_dict['tube_diameter'] = e.furnace.tube_diameter
            exp_dict['cross_sectional_area'] = e.furnace.cross_sectional_area
            exp_dict['tube_length'] = e.furnace.tube_length
            exp_dict['length_of_heated_region'] = e.furnace.length_of_heated_region
        if e.properties:
            exp_dict['average_thickness_of_growth'] = e.properties.average_thickness_of_growth
            exp_dict['standard_deviation_of_growth'] = e.properties.standard_deviation_of_growth
            exp_dict['number_of_layers'] = e.properties.number_of_layers
            exp_dict['growth_coverage'] = e.properties.growth_coverage
            exp_dict['domain_size'] = e.properties.domain_size
            exp_dict['shape'] = e.properties.shape

        output.append(exp_dict)
    session.close()
    return jsonify(output)
