from raspcuterie.devices.output.relay import manager


def test_relay():

    manager.relay_1.on()
    manager.relay_2.on()
    assert manager.relay_1.value == True