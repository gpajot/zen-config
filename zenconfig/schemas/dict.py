from typing import Any, Type, TypeVar

from zenconfig.write import Schema

C = TypeVar("C", bound=dict)


class DictSchema(Schema[C]):
    def from_dict(self, cls: Type[C], cfg: dict[str, Any]) -> C:
        return cls(cfg)

    def to_dict(self, config: C) -> dict[str, Any]:
        return dict(config)
