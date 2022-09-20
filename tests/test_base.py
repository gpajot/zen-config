import os
from pathlib import Path

import pytest

from zenconfig.base import BaseConfig, Format, Schema


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

    def test_paths_should_raise_if_nothing_provided(self, config):
        with pytest.raises(ValueError, match="could not find the config path"):
            config._paths()

    def test_paths_should_fallback_on_default_if_no_env(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        assert config._paths() == (Path(".").absolute() / "the_path.json",)

    def test_paths_should_prefer_env_value(self, config):
        config.ENV_PATH = "THE_PATH"
        config.PATH = "the_path.json"
        os.environ["THE_PATH"] = "the_env_path.json"
        assert config._paths() == (Path(".").absolute() / "the_env_path.json",)

    def test_paths_should_handle_globbing(self, config):
        config.PATH = "./*/config_?.*"
        assert config._paths() == (
            Path(__file__).parent.absolute() / "test_files" / "config_a.yaml",
            Path(__file__).parent.absolute() / "test_files" / "config_b.toml",
        )
