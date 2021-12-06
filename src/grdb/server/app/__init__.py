from flask import Flask
from flask_cors import CORS

# from grdb.database.dal import DataAccessLayer
# from grdb.config import Config
from grdb.database import Base
from .db import Database

read_db = Database(Base)
write_db = Database(Base)
admin_db = Database(Base)


# read_db = DataAccessLayer()
# conf = Config(prefix="DEV_DATABASE", suffix="_READ", debug=True, try_secrets=False)
# read_db.init_db(conf, privileges={"read": True, "write": False, "validate": False})
# write_db = DataAccessLayer()
# conf = Config(prefix="DEV_DATABASE", suffix="_WRITE", debug=True, try_secrets=False)
# write_db.init_db(conf, privileges={"read": True, "write": True, "validate": True})


def register_blueprints(app):
    from .views import experiments
    app.register_blueprint(experiments)
    from .views.auth import auth
    app.register_blueprint(auth)


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object('grdb.server.app.config.Config')
    app.config['CORS_HEADERS'] = 'Content-Type'
    read_db.init(app.config["DEV_DATABASE_URL_READ"])
    write_db.init(app.config["DEV_DATABASE_URL_WRITE"])
    admin_db.init(app.config["DEV_DATABASE_URL_ADMIN"])

    # ***************** move below to notebook ***********************
    # # create tables for webapp
    # from grdb.database.models import User
    # from grdb.database.models import Institution
    # Base.metadata.create_all(bind=admin_db.engine)
    #
    # #init school database
    # import json
    # file = open('/Users/jlee/gresq/GSA-Database/src/grdb/server/allSchools.json') #fix url as needed
    # schools = json.load(file)
    # schools.sort(key=lambda s: s['name'])
    # db = admin_db.Session()
    # i = 0
    # for school in schools:
    #     institution = Institution(name=school['name'], country=school['country'])
    #     db.add(institution)
    #     if i % 2000 == 0:
    #         print(i, '/', len(schools))
    #     i += 1
    # db.commit()
    # db.close()

    register_blueprints(app)
    return app
