import pytest

from zenconfig.loc import Loc
from zenconfig.read import ReadOnlyConfig, ReadOnlyFormat, ReadOnlySchema


class TestReadOnlyConfig:
    @pytest.fixture()
    def loc(self, mocker):
        return mocker.Mock(spec=Loc)

    @pytest.fixture()
    def fmt(self, mocker):
        return mocker.Mock(spec=ReadOnlyFormat)

    @pytest.fixture()
    def schema(self, mocker):
        return mocker.Mock(spec=ReadOnlySchema)

    @pytest.fixture()
    def config(self, loc, fmt, schema):
        class Config(ReadOnlyConfig):
            LOC = loc
            FORMAT = fmt
            SCHEMA = schema

        return Config

    def test_should_be_able_to_load_from_file(self, loc, fmt, schema, config):
        loc.path = "./test.json"
        fmt.load.side_effect = lambda p: {"a": p}
        schema.from_dict.side_effect = lambda c, o: (c, o)

        assert config.load() == (config, {"a": "./test.json"})
