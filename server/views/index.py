from flask import Blueprint, jsonify, request
from src.grdb.database.models import (
    Author, EnvironmentConditions, Experiment, Furnace, Recipe, Substrate)

from server import research_db
from .utils import query_experiment_data

index = Blueprint('index', __name__, url_prefix='/')


@index.route('/data/experiments', methods=['GET'])
def experiment_data():
    params = request.args

    q = research_db.Session.query(Experiment)

    # CURRENTLY SUPPORTED COLUMNS: recipe, substrate, furnace
    experiments = query_experiment_data(q, params)
    output = []
    for experiment in experiments:
        exprmnt_dict = {'carbon_source': experiment.recipe.carbon_source,
                        'base_pressure': experiment.recipe.base_pressure,
                        'catalyst': experiment.substrate.catalyst,
                        'thickness': experiment.substrate.thickness,
                        'diameter': experiment.substrate.diameter,
                        'length': experiment.substrate.length,
                        'surface_area': experiment.substrate.surface_area,
                        'tube_diameter': experiment.furnace.tube_diameter,
                        'cross_sectional_area': experiment.furnace.cross_sectional_area,
                        'tube_length': experiment.furnace.tube_length,
                        'length_of_heated_region': experiment.furnace.length_of_heated_region}
        output.append(exprmnt_dict)
    return jsonify(output)
