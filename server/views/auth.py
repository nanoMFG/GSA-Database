from flask import Blueprint, request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from ..models.user import User

from server import webapp_db

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/register", methods=["POST"])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    username = request.form['username']
    password = request.form['password']
    password_hash = generate_password_hash(password)

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )
        webapp_db.Session.add(user)
        webapp_db.Session.commit()

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
