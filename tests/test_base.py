import os
from pathlib import Path

import pytest

from zenconfig.base import BaseConfig
from zenconfig.formats.abc import Format
from zenconfig.schemas.abc import Schema


class TestBaseConfig:
    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=Format)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=Schema)

    @pytest.fixture()
    def config(self, fmt, schema):
        class Config(BaseConfig):
            FORMAT = fmt
            SCHEMA = schema

        return Config

    def test_path_should_raise_if_nothing_provided(self, config):
        with pytest.raises(ValueError, match="could not find the config path"):
            config._path()

    def test_path_should_fallback_on_default_if_no_env(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        assert config._path() == Path("the_path.json")

    def test_path_should_prefer_env_value(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        os.environ["THE_PATH"] = "the_env_path.json"
        assert config._path() == Path("the_env_path.json")
