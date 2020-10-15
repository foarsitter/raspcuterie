from flask import Flask, render_template

from raspcuterie import FAKE_VALUES
from raspcuterie.dashboard import api

app = Flask(__name__, template_folder="./templates")

app.register_blueprint(api.bp)


@app.route("/")
def dashboard():
    print(FAKE_VALUES)
    return render_template("base.html")
