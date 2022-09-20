from abc import ABC
from enum import IntEnum
from typing import Any, ClassVar, Dict, Type, TypeVar

from zenconfig.base import BaseConfig, ZenConfigError


class MergeStrategy(IntEnum):
    SHALLOW = 1
    DEEP = 2


C = TypeVar("C", bound="ReadOnlyConfig")


class ReadOnlyConfig(BaseConfig, ABC):
    MERGE_STRATEGY: ClassVar[MergeStrategy] = MergeStrategy.DEEP

    @classmethod
    def load(cls: Type[C]) -> C:
        dict_config: Dict[str, Any] = {}
        for path in cls._paths():
            config = cls._format(path).load(path)
            if not dict_config:
                dict_config = config
            elif cls.MERGE_STRATEGY is MergeStrategy.SHALLOW:
                dict_config.update(config)
            elif cls.MERGE_STRATEGY is MergeStrategy.DEEP:
                _deep_merge(dict_config, config)
            else:
                raise ZenConfigError(f"unsupported merge strategy {cls.MERGE_STRATEGY}")
        return cls._schema().from_dict(cls, dict_config)


def _deep_merge(a: Dict[str, Any], b: Dict[str, Any]) -> None:
    for k, v in b.items():
        if k not in a or not isinstance(a[k], dict) or not isinstance(v, dict):
            a[k] = v
        else:
            _deep_merge(a[k], v)
