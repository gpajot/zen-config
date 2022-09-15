import os
from pathlib import Path

import pytest

from zenconfig.read import ReadOnlyConfig, ReadOnlyFormat, ReadOnlySchema


class TestReadOnlyConfig:
    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=ReadOnlyFormat)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=ReadOnlySchema)

    @pytest.fixture()
    def config(self, fmt, schema):
        class Config(ReadOnlyConfig):
            FORMAT = fmt
            SCHEMA = schema

        return Config

    def test_path_should_raise_if_nothing_provided(self, config):
        with pytest.raises(ValueError, match="could not find the config path"):
            config.path()

    def test_path_should_fallback_on_default_if_no_env(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        assert config.path() == Path("the_path.json")

    def test_path_should_prefer_env_value(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        os.environ["THE_PATH"] = "the_env_path.json"
        assert config.path() == Path("the_env_path.json")

    def test_should_be_able_to_load_from_file(self, fmt, schema, config):
        config.PATH = "test.json"
        fmt.load.side_effect = lambda p: {"a": str(p)}
        schema.from_dict.side_effect = lambda c, o: (c, o)

        assert config.load() == (config, {"a": "test.json"})
