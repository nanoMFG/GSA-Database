from datetime import datetime, timedelta
from flask import Blueprint, request, make_response, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from ..config import Config

from grdb.database.models import Author, User
from server import read_db, write_db

auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    institution = data.get('institution')
    email = data.get('email')
    password = data.get('password')

    if not (first_name and last_name and email and password):
        return make_response('Missing required field.', 400)

    password_hash = generate_password_hash(password)

    db = write_db.Session()
    user = db.filter_by(email=email).first()

    if not user:
        author = Author(first_name=first_name, last_name=last_name, institution=institution)
        db.add(author)
        db.flush()

        user = User(
            email=email,
            password_hash=password_hash,
            author_id=author.id
        )
        db.add(user)
        db.commit()

        return make_response('User registered.', 201)
    else:
        return make_response('User already exists', 409)


# TODO: ADD JWT
@auth.route("/signin", methods=['post'])
def login():
    token = request.headers.get('Authorization')
    if token:
        user_info = jwt.decode(token, Config.JWT_SECRET)
        email = user_info['email']
        expiration = user_info['expiration']
        elapsed_secs = (datetime.now() - datetime.fromtimestamp(expiration)).total_seconds()
        if elapsed_secs < 3600:  # 1 hour
            new_expiration = datetime.now() + timedelta(hours=1)
            new_expiration = new_expiration.timestamp()
            payload = {'email': email,
                       'expiration': new_expiration}
            token = jwt.encode(payload, Config.JWT_SECRET)
            return jsonify({'token': token})

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not (email or password):
        return make_response("Missing required fields.", 400)

    db = read_db.Session()
    user = db.query(User).filter_by(email=email).first()
    db.close()

    if user and check_password_hash(user.password_hash, password):
        return make_response("Login successful.", 200)
    else:
        return make_response('Incorrect username or password', 403)


@auth.route("/users")
def users():
    return jsonify()
