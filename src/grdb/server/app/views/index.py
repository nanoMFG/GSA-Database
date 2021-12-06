from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS
from grdb.database.models import (
    Furnace, Substrate, EnvironmentConditions, Recipe, PreparationStep, Experiment, Author, SemFile, SemAnalysis,
    Software, RamanFile, RamanAnalysis, Properties, User
)
from datetime import datetime
from .. import read_db, write_db
from .utils.query import query_experiment_data

index = Blueprint('index', __name__, url_prefix='/')
CORS(index)
