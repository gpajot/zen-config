from typing import Callable, List, Optional

from zenconfig.formats.abc import Format

FormatSelector = Callable[[str], Optional[Format]]


def _json_selector(ext: str) -> Optional[Format]:
    if ext != ".json":
        return None
    from zenconfig.formats.json import JSONFormat

    return JSONFormat()


def _yaml_selector(ext: str) -> Optional[Format]:
    if ext not in {".yml", ".yaml"}:
        return None
    try:
        from zenconfig.formats.yaml import YAMLFormat

        return YAMLFormat()
    except ImportError:
        raise ValueError("yaml config is not supported, install the yaml extra")


def _toml_selector(ext: str) -> Optional[Format]:
    if ext != ".toml":
        return None
    try:
        from zenconfig.formats.toml import TOMLFormat

        return TOMLFormat()
    except ImportError:
        raise ValueError("toml config is not supported, install the toml extra")


format_selectors: List[FormatSelector] = [
    _json_selector,
    _yaml_selector,
    _toml_selector,
]
