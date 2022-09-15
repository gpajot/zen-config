from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from zenconfig.write import Format


@dataclass
class YAMLFormat(Format):
    indent: int = 2
    sort_keys: bool = True

    def load(self, path: Path) -> dict[str, Any]:
        return yaml.safe_load(path.read_text())

    def dump(self, path: Path, config: dict[str, Any]) -> None:
        path.write_text(
            yaml.safe_dump(config, indent=self.indent, sort_keys=self.sort_keys)
        )
