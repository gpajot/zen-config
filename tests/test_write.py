from pathlib import Path

import pytest

from zenconfig.base import ZenConfigError
from zenconfig.write import Config


class TestReadOnlyConfig:
    def test_should_not_be_able_to_write_to_multiple_files(self, mocker):
        class Cfg(Config): ...

        mocker.patch.object(Cfg, "_paths", return_value=(Path(), Path()))

        with pytest.raises(ZenConfigError, match="cannot save"):
            Cfg().save()
