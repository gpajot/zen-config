from pathlib import Path

import pytest

from zenconfig.base import ZenConfigError
from zenconfig.write import Config


class TestReadOnlyConfig:
    def test_should_not_be_able_to_write_to_multiple_files(self):
        class Cfg(Config):
            _PATHS = (Path(), Path())

        with pytest.raises(ZenConfigError, match="cannot save"):
            Cfg().save()
