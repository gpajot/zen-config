from dataclasses import asdict, fields, is_dataclass
from typing import Any, Dict, Type, TypeVar

from zenconfig.schemas.abc import Schema

C = TypeVar("C")


class DataclassSchema(Schema[C]):
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return _load_nested(cls, cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        cfg: Dict[str, Any] = {}
        for field in fields(config):
            value = getattr(config, field.name)
            if is_dataclass(field.type):
                value = asdict(value)
            cfg[field.name] = value
        return cfg


def _load_nested(cls: Type[C], cfg: Dict[str, Any]) -> C:
    """Load nested dataclasses."""
    kwargs: Dict[str, Any] = {}
    for field in fields(cls):
        if field.name not in cfg:
            continue
        value = cfg[field.name]
        if is_dataclass(field.type):
            value = _load_nested(field.type, value)
        kwargs[field.name] = value
    return cls(**kwargs)
