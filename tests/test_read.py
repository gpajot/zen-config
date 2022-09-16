from pathlib import Path

import pytest

from zenconfig.formats.abc import Format
from zenconfig.read import ReadOnlyConfig
from zenconfig.schemas.abc import Schema


class TestReadOnlyConfig:
    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=Format)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=Schema)

    @pytest.fixture()
    def config(self, fmt, schema):
        class Config(ReadOnlyConfig):
            FORMAT = fmt
            SCHEMA = schema

        return Config

    def test_should_be_able_to_load_from_file(self, fmt, schema, config):
        config._PATH = Path("test.json")
        fmt.load.side_effect = lambda p: {"a": str(p)}
        schema.from_dict.side_effect = lambda c, o: (c, o)

        assert config.load() == (config, {"a": "test.json"})
