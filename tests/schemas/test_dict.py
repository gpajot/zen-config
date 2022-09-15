from typing import ClassVar

from zenconfig.schemas.dict import DictSchema
from zenconfig.write import Config


class DictConfig(Config, dict):
    PATH: ClassVar[str] = "test.json"


def test_dataclass():
    assert isinstance(DictConfig._schema(), DictSchema)
    cfg = DictConfig(a="a", b=1)
    cfg.save()
    reloaded = DictConfig.load()
    assert reloaded == {"a": "a", "b": 1}
    cfg.clear()
