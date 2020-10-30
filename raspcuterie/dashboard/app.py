from flask import Flask, request
from flask_babel import Babel

from raspcuterie import base_path
from raspcuterie.config import setup
from raspcuterie.dashboard import api, dashboard

babel = Babel()


def create_app():
    app = Flask(__name__, template_folder="./templates")

    app.register_blueprint(api.bp)
    app.register_blueprint(dashboard.bp)

    app.config["BABEL_TRANSLATION_DIRECTORIES"] = str(base_path / "translations")

    babel.init_app(app)

    setup()

    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(["nl", "en"])

