from flask import Flask, request
from flask_babel import Babel

from raspcuterie import base_path
from raspcuterie.config import setup
from raspcuterie.dashboard import api, dashboard
from raspcuterie.db import close_db, init_db, raw_connection

babel = Babel()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder="./templates")
    app.config.from_mapping(DATABASE=str(base_path / "raspcuterie.db"))

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config["BABEL_TRANSLATION_DIRECTORIES"] = str(base_path / "translations")

    app.register_blueprint(api.bp)
    app.register_blueprint(dashboard.bp)

    app.teardown_appcontext(close_db)

    babel.init_app(app)

    setup(app)
    init_db(raw_connection(app))
    return app


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(["nl", "en"])