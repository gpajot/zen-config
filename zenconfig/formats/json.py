import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from zenconfig.write import Format


@dataclass
class JSONFormat(Format):
    indent: int = 2
    sort_keys: bool = True
    ensure_ascii: bool = False

    def load(self, path: Path) -> dict[str, Any]:
        return json.loads(path.read_text())

    def dump(self, path: Path, config: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(
                config,
                indent=self.indent,
                sort_keys=self.sort_keys,
                ensure_ascii=self.ensure_ascii,
            ),
        )
