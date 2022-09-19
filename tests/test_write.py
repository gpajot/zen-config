from pathlib import Path

import pytest

from zenconfig.base import Format, Schema
from zenconfig.write import Config


class TestReadOnlyConfig:
    @pytest.fixture()
    def path(self, mocker):
        return mocker.Mock(spec=Path)

    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=Format)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=Schema)

    @pytest.fixture()
    def config(self, path, fmt, schema):
        class Cfg(Config):
            _PATH = path
            FORMAT = fmt
            SCHEMA = schema

        return Cfg()

    def test_should_be_able_to_write_to_file(self, path, fmt, schema, config):
        path.exists.return_value = True

        def dump(p, o):
            o.append(p)

        fmt.dump.side_effect = dump
        obj = []
        schema.to_dict.return_value = obj

        config.save()
        assert obj == [path]

    def test_should_be_able_to_clear_file(self, config, path):
        config.clear()
        path.unlink.assert_called_once()
