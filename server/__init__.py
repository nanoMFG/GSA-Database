import os
from flask import Flask
from sqlalchemy import MetaData

from src.grdb.database import Base as research_db_Base
from .models import Base as webapp_db_Base
from .db import DataBase

meta = MetaData()
research_db = DataBase(research_db_Base)
webapp_db = DataBase(webapp_db_Base)


def register_blueprints(app):
    from .views.index import index
    app.register_blueprint(index)
    from .views.auth import auth
    app.register_blueprint(auth)


def create_schema(db: DataBase):
    from .models import user
    db.base.metadata.create_all(db.engine)


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
