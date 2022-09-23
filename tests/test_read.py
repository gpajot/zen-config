import pytest

from zenconfig.base import Schema
from zenconfig.read import MergeStrategy, ReadOnlyConfig


class TestReadOnlyConfig:
    @pytest.mark.parametrize(
        ("merge_strategy", "expected"),
        [
            (
                MergeStrategy.SHALLOW,
                {"a": "a", "b": 2, "deep": {"deeper": {"d": True}}},
            ),
            (
                MergeStrategy.DEEP,
                {"a": "a", "b": 2, "deep": {"c": True, "deeper": {"d": True}}},
            ),
        ],
    )
    def test_should_be_able_to_load_from_multiple_files(
        self, merge_strategy, expected, mocker
    ):
        schema = mocker.Mock(spec=Schema)
        schema.from_dict.side_effect = lambda _, d: d

        class Cfg(ReadOnlyConfig):
            PATH = "./*/config_?.*"
            MERGE_STRATEGY = merge_strategy
            SCHEMA = schema

        assert Cfg.load() == expected

    def test_should_not_fail_if_file_does_not_exist(self):
        class Cfg(ReadOnlyConfig, dict):
            PATH = "test_config.json"

        assert Cfg.load() == {}
