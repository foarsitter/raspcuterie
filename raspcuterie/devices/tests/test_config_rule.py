import pytest

from raspcuterie.devices.am2302 import AM2302
from raspcuterie.devices.config import ConfigRule
from raspcuterie.devices.relay import manager, OutputDevice


@pytest.mark.parametrize("temperature,match", [(11, True), (9, False)])
def test_matches(monkeypatch, temperature, match):

    monkeypatch.setattr(AM2302, "read", lambda: (0, temperature))

    x = ConfigRule(device=manager.relay_1, expression="temperature >= 10", action="on")

    assert x.matches() == match


def test_execute(monkeypatch):

    monkeypatch.setattr(AM2302, "read", lambda: (0, 7))

    # x = ConfigRule(device=manager.relay_1, expression="True", action="off")
    # x.execute()
    # x = ConfigRule(device=manager.relay_2, expression="True", action="off")
    # x.execute()
    # x = ConfigRule(device=manager.relay_3, expression="True", action="off")
    # x.execute()

    assert len(OutputDevice._registry) == 4

    x = ConfigRule(device=manager.relay_4, expression="True", action="on")
    x.execute()
