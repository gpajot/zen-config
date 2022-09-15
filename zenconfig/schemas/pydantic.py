from dataclasses import dataclass
from typing import Any, Type, TypeVar

from pydantic import BaseModel

from zenconfig.schemas.abc import Schema

C = TypeVar("C", bound=BaseModel)


@dataclass
class PydanticSchema(Schema[BaseModel]):
    exclude_unset: bool = False
    exclude_defaults: bool = True

    def from_dict(self, cls: Type[C], cfg: dict[str, Any]) -> C:
        return cls.parse_obj(cfg)

    def to_dict(self, config: C) -> dict[str, Any]:
        return config.dict(
            exclude_unset=self.exclude_unset, exclude_defaults=self.exclude_defaults
        )
