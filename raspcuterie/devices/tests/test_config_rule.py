import pytest

from raspcuterie.devices.input.am2302 import AM2302
from raspcuterie.devices.control import ControlRule
from raspcuterie.devices import OutputDevice
from raspcuterie.devices.output.relay import DBRelay


@pytest.mark.parametrize("temperature,match", [(11, True), (9, False)])
def test_matches(monkeypatch, temperature, match):

    monkeypatch.setattr(AM2302, "read", lambda x: (0, temperature))

    AM2302("am2303")

    relay = DBRelay("test", created_table=False)

    x = ControlRule(device=relay, expression="temperature >= 10", action="on")

    assert x.matches() == match


def test_execute(monkeypatch):

    monkeypatch.setattr(AM2302, "read", lambda: (0, 7))

    relay = DBRelay("test", created_table=False)

    assert len(OutputDevice.registry) == 5

    x = ControlRule(device=relay, expression="True", action="on")
    x.execute()
