from pathlib import Path

import pytest

from zenconfig.loc import Loc
from zenconfig.write import Config, Format, Schema


class TestReadOnlyConfig:
    @pytest.fixture()
    def loc(self, mocker):
        loc = mocker.Mock(spec=Loc)
        loc.path = mocker.Mock(spec=Path)
        return loc

    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=Format)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=Schema)

    @pytest.fixture()
    def config(self, loc, fmt, schema):
        class Cfg(Config):
            LOC = loc
            FORMAT = fmt
            SCHEMA = schema

        return Cfg()

    def test_should_be_able_to_write_to_file(self, loc, fmt, schema, config):
        loc.path.exists.return_value = True

        def dump(p, o):
            o.append(p)

        fmt.dump.side_effect = dump
        obj = []
        schema.to_dict.return_value = obj

        config.save()
        assert obj == [loc.path]

    def test_should_be_able_to_clear_file(self, config, loc):
        config.clear()
        loc.path.unlink.assert_called_once()
