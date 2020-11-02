import os
import tempfile

import pytest

from raspcuterie.dashboard.app import create_app


@pytest.fixture
def app():
    return create_app()


@pytest.fixture
def client(app):
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])
