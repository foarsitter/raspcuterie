from flask import Flask

from raspcuterie.config import setup
from raspcuterie.dashboard import api, dashboard


def create_app():
    app = Flask(__name__, template_folder="./templates")

    app.register_blueprint(api.bp)
    app.register_blueprint(dashboard.bp)

    setup()

    return app
