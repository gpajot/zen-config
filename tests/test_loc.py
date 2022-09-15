import os
from pathlib import Path

import pytest

from zenconfig.loc import Loc


class TestLoc:
    def test_should_raise_if_nothing_provided(self):
        loc = Loc()
        with pytest.raises(ValueError, match="could not find the config path"):
            loc.path

    def test_should_fallback_on_default_if_no_env(self):
        loc = Loc(env="THE_PATH", default="the_path.json")
        assert loc.path == Path("the_path.json")

    def test_should_prefer_env_value(self):
        loc = Loc(env="THE_PATH", default="the_path.json")
        os.environ["THE_PATH"] = "the_env_path.json"
        assert loc.path == Path("the_env_path.json")
