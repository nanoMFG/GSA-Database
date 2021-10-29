from flask import Flask
from sqlalchemy import MetaData

from src.grdb.database import Base
from .db import Database

meta = MetaData()
db = Database(Base)


def register_blueprints(app):
    from .views import index
    app.register_blueprint(index)
    from .views import auth
    app.register_blueprint(auth)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('server.config.Config')

    db.init(app.config["DEV_DATABASE_URL"])

    from grdb.database.models import User
    Base.metadata.create_all(bind=db.engine)

    register_blueprints(app)

    return app
