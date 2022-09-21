from typing import ClassVar

from tests.schemas.utils import parametrize_formats
from zenconfig.schemas.dict import DictSchema
from zenconfig.write import Config


@parametrize_formats
def test_dict(fmt, path):
    class DictConfig(Config, dict):
        PATH: ClassVar[str] = path

    assert isinstance(DictConfig._format(), fmt)
    assert isinstance(DictConfig._schema(), DictSchema)
    cfg = DictConfig(a="a", b=1)
    cfg.save()
    reloaded = DictConfig.load()
    assert reloaded == {"a": "a", "b": 1}
    cfg.clear()
