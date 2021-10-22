import os
from flask import Flask
from sqlalchemy import MetaData

from src.grdb.database import Base as research_db_Base
from .models import Base as webapp_db_Base
from .db import Database

meta = MetaData()
research_db = Database(research_db_Base)
webapp_db = Database(webapp_db_Base)


def register_blueprints(app):
    from .views import index
    app.register_blueprint(index)
    from .views import auth
    app.register_blueprint(auth)


def create_schema(database: Database):
    from .models import user
    database._Base.metadata.create_all(database.engine)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('server.config.Config')

    research_db.init(app.config["DEV_DATABASE_URL"])
    module_dir = os.path.dirname(os.path.abspath(__file__))
    tempdb = os.path.join(module_dir, 'temp.db')
    webapp_db.init('sqlite:///{}'.format(tempdb))  # TODO: Add another DB in AWS

    register_blueprints(app)
    create_schema(webapp_db)

    return app
