from flask import Blueprint, jsonify, request, make_response
from flask_cors import CORS
from datetime import datetime
from sqlalchemy import and_

from grdb.database.models import (
    Furnace, Substrate, EnvironmentConditions, Recipe, PreparationStep, Experiment, Author, SemFile, SemAnalysis,
    Software, RamanFile, RamanAnalysis, Properties
)

from .. import read_db, write_db, s3

authors = Blueprint('authors', __name__, url_prefix='/authors')
CORS(authors)

@authors.route('/<int:id>', methods=['GET'])
def get_author_id(id):
    db = read_db.Session()
    author = db.query(Author).filter_by(id=id).first()
    db.close()
    return jsonify(author.json_encodable())

@authors.route('', methods=['GET'])
def get_author():
    data = request.args
    first_name = data['first_name']
    last_name = data['last_name']
    institution = data['institution']
    db = read_db.Session()
    author = db.query(Author).filter_by(first_name=first_name,
                                        last_name=last_name,
                                        institution=institution).first()
    db.close()
    return jsonify(author.json_encodable())


@authors.route('', methods=['POST'])
def add_author():
    data = request.get_json()
    author = Author(first_name=data['first_name'],
                    last_name=data['last_name'],
                    institution=data['institution'])
    db = write_db.Session()
    db.add(author)
    db.commit()
    db.close()
    return jsonify({'id': author.id})
