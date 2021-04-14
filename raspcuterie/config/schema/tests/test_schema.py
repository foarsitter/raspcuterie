from pathlib import Path

import yaml

import raspcuterie
from raspcuterie.config import schema
from raspcuterie.config.schema.devices import DegreeSchema


def test_schema():

    file = raspcuterie.lib_path / Path("config_dev.yaml")

    data = yaml.safe_load(file.read_text())

    settings = schema.RaspcuterieConfigSchema.parse_obj(data)

    assert len(settings.devices) == 7

    assert isinstance(settings.devices[0], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[1], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[2], schema.RelaySwitchSchema)
    assert isinstance(settings.devices[3], schema.RelaySwitchSchema)

    assert isinstance(settings.devices[4], schema.SinusSchema)
    assert isinstance(settings.devices[5], schema.SinusSchema)

    assert "default" in settings.control

    default_control = settings.control.get("default")

    assert len(default_control.rules.keys()) == 2

    assert default_control.expires.year == 2020


def test_jsonschema():

    jsonschema = schema.RaspcuterieConfigSchema.schema_json()

    print(jsonschema)
