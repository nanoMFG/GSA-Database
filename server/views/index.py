from flask import Blueprint, jsonify, request
from src.grdb.database.models import *

from server import db
from .utils import query_experiment_data

index = Blueprint('index', __name__, url_prefix='/')


@index.route('/experiments/data', methods=['GET'])
def experiment_data():
    params = request.args
    session = db.Session()
    q = session.query(Experiment)

    # CURRENTLY SUPPORTED COLUMNS: recipe, substrate, furnace
    experiments = query_experiment_data(q, params)
    output = []
    for e in experiments:
        exp_dict = dict()
        if e.recipe:
            exp_dict['carbon_source'] = e.recipe.carbon_source
            exp_dict['base_pressure'] = e.recipe.base_pressure

        exp_dict = {'carbon_source': e.recipe.carbon_source if e.recipe else None,
                    'base_pressure': e.recipe.base_pressure if e.recipe else None,
                    'catalyst': e.substrate.catalyst if e.substrate else None,
                    'dew_point': e.environment_conditions.dew_point if e.environment_conditions else None,
                    'ambient_temperature': e.environment_conditions.ambient_temperature if e.environment_conditions else None,
                    'thickness': e.substrate.thickness if e.substrate else None,
                    'diameter': e.substrate.diameter if e.substrate else None,
                    'length': e.substrate.length if e.substrate else None,
                    'surface_area': e.substrate.surface_area if e.substrate else None,
                    'tube_diameter': e.furnace.tube_diameter if e.furnace else None,
                    'cross_sectional_area': e.furnace.cross_sectional_area if e.furnace else None,
                    'tube_length': e.furnace.tube_length if e.furnace else None,
                    'length_of_heated_region': e.furnace.length_of_heated_region if e.furnace else None,
                    'average_thickness_of_growth': e.properties.average_thickness_of_growth if e.properties else None,
                    'standard_deviation_of_growth': e.properties.standard_deviation_of_growth if e.properties else None,
                    'number_of_layers': e.properties.number_of_layers if e.properties else None,
                    'growth_coverage': e.properties.growth_coverage if e.properties else None,
                    'domain_size': e.properties.domain_size if e.properties else None,
                    'shape': e.properties.shape if e.properties else None,
                    'date': e.experiment_date,
                    'material': e.material_name
                    }
        output.append(exp_dict)
    session.close()
    return jsonify(output)
