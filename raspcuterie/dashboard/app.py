from flask import Flask, render_template

from raspcuterie import FAKE_VALUES
from raspcuterie.dashboard import api
from raspcuterie.devices.hx711 import hx
from raspcuterie.devices.relay import manager
from raspcuterie.devices.am2302 import AM2302

app = Flask(__name__, template_folder="./templates")

app.register_blueprint(api.bp)


@app.route("/")
def dashboard():

    relay_1 = manager.is_on(1)
    relay_2 = manager.is_on(2)
    relay_3 = manager.is_on(3)
    relay_4 = manager.is_on(4)

    humidity, temperature = AM2302.read()

    weight = hx.get_grams()

    return render_template(
        "base.html",
        relay_1=relay_1,
        relay_2=relay_2,
        relay_3=relay_3,
        relay_4=relay_4,
        humidity=humidity,
        temperature=temperature,
        weight=weight
    )
