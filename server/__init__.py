from flask import Flask

from .db import DataBase

research_db = DataBase()
webapp_db = DataBase()


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('server.config.Config')

    research_db.init(app.config["DEV_DATABASE_URL"])
    # TODO: webapp_db.init()

    from .views.index import index
    app.register_blueprint(index)

    return app
