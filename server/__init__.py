from flask import Flask
from flask_cors import CORS

from src.grdb.database import Base
from .db import Database

db = Database(Base)


def register_blueprints(app):
    from .views import index
    app.register_blueprint(index)
    from .views.auth import auth
    app.register_blueprint(auth)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, resources={r"/*": {"origins":"*"}})
    app.config.from_object('server.config.Config')
    app.config['CORS_HEADERS'] = 'Content-Type'
    db.init(app.config["DEV_DATABASE_URL"])

    # create user table
    # from grdb.database.models import User
    # Base.metadata.create_all(bind=db.engine)

    register_blueprints(app)
    return app
