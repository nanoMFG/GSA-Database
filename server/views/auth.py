from flask import Flask, Blueprint, request, make_response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

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
    password_hash = generate_password_hash(password, salt_length=len(last_name))

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password_hash
        )
        webapp_db.session.add(user)
        webapp_db.session.commit()

        return make_response('User registered.', 201)
    else:
        return make_response('User already exists', 202)


@auth.route("/users")
def users():
    print(User.query.all()[0])
    return jsonify()
