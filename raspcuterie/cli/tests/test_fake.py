from .. import fake
from ...db import get_db
from ...devices.series import IntegerSeries


def test_fake_humidity(runner, app):

    with app.app_context():
        IntegerSeries("test").create_table(get_db())
    result = runner.invoke(fake.humidity, "test", catch_exceptions=False)
    assert result.exit_code == 0, result.exception
