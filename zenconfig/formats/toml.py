from dataclasses import dataclass
from pathlib import Path
from typing import Any

import tomli
import tomli_w

from zenconfig.write import Format


@dataclass
class TOMLFormat(Format):
    multiline_strings: bool = True

    def load(self, path: Path) -> dict[str, Any]:
        return tomli.loads(path.read_text())

    def dump(self, path: Path, config: dict[str, Any]) -> None:
        path.write_text(tomli_w.dumps(config, multiline_strings=self.multiline_strings))
