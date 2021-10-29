from flask import Blueprint, request, make_response, jsonify
from flask_cors import CORS, cross_origin
from werkzeug.security import generate_password_hash, check_password_hash

from grdb.database.models import Author, User
from server import db

auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth)


@auth.route("/signup", methods=["POST"])
@cross_origin()
def signup():
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    institution = data['institution']
    email = data['email']
    password = data['password']
    password_hash = generate_password_hash(password)

    user = User.query.filter_by(email=email).first()

    if not user:
        author = Author(first_name=first_name, last_name=last_name, institution=institution)
        db.Session.add(author)
        db.Session.flush()

        user = User(
            email=email,
            password_hash=password_hash,
            author_id=author.id
        )
        db.Session.add(user)
        db.Session.commit()

        return make_response('User registered.', 201)
    else:
        return make_response('User already exists', 202)


# TODO: ADD JWT
@auth.route("/login", methods=['post'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return make_response("Login successful.", 200)
    else:
        return make_response('Incorrect username or password', 403)


@auth.route("/users")
def users():
    print(User.query.all()[0])
    return jsonify()
