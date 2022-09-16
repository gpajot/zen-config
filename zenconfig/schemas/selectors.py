from dataclasses import is_dataclass
from typing import Callable, List, Optional

from zenconfig.schemas.abc import Schema

SchemaSelector = Callable[[type], Optional[Schema]]


def _dataclass_selector(cls: type) -> Optional[Schema]:
    if not is_dataclass(cls):
        return None
    from zenconfig.schemas.dataclass import DataclassSchema

    return DataclassSchema()


def _pydantic_selector(cls: type) -> Optional[Schema]:
    try:
        from pydantic import BaseModel
    except ImportError:
        return None
    if not issubclass(cls, BaseModel):
        return None
    from zenconfig.schemas.pydantic import PydanticSchema

    return PydanticSchema()


def _dict_selector(cls: type) -> Optional[Schema]:
    if not issubclass(cls, dict):
        return None
    from zenconfig.schemas.dict import DictSchema

    return DictSchema()


schema_selectors: List[SchemaSelector] = [
    _dataclass_selector,
    _pydantic_selector,
    _dict_selector,
]
