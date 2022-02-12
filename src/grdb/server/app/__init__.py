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


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object('grdb.server.app.config.Config')
    app.config['CORS_HEADERS'] = 'Content-Type'
    read_db.init(app.config["DEV_DATABASE_URL_READ"])
    write_db.init(app.config["DEV_DATABASE_URL_WRITE"])
    admin_db.init(app.config["DEV_DATABASE_URL_ADMIN"])

    register_blueprints(app)
    return app
