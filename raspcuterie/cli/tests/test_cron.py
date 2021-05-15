import sys

import pytest

from raspcuterie.cli import cron


@pytest.mark.skipif(
    sys.platform.startswith("win"), reason="requires python3.6 or higher"
)
def test_log_values(runner):
    result = runner.invoke(cron.log, catch_exceptions=False)
    assert result.exit_code == 0, result.exception
