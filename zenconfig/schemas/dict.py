from typing import Any, Dict, Type, TypeVar

from zenconfig.schemas.abc import Schema

C = TypeVar("C", bound=dict)


class DictSchema(Schema[C]):
    def from_dict(self, cls: Type[C], cfg: Dict[str, Any]) -> C:
        return cls(cfg)

    def to_dict(self, config: C) -> Dict[str, Any]:
        return dict(config)
