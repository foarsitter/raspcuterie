from raspcuterie.devices.output.relay import DBRelay


def test_on():

    x = DBRelay("test")

    x.on()

    assert x.value() is True


def test_off():

    x = DBRelay("test")

    x.off()

    assert x.value() is False
