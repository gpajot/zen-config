# simple-config
Simple configuration loader for python.

Compared to other solutions, the goal is to bring:
- simple usage for simple use cases
- multiple format support
- use objects rather than plain dict to interact with the config
- optionally use the power of pydantic for validation

## Simple usage
If you don't want to configure much, you can use:
```python
from dataclasses import dataclass
from zenconfig import Config

@dataclass
class MyConfig(Config):
    PATH = "~/myconfig.json"
    
    some_key: str
    some_optional_key: bool = False


cfg = MyConfig(some_key="hello")
cfg.save()
...
cfg = MyConfig.load()
cfg.some_optional_key = True
cfg.save()
...
cfg.clear()
```

## Config file loading
When creating your config, you can specify at least one of those two attributes:
- `ENV_PATH` the environment variable name containing the path to the config file
- `PATH` directly the config path

> 💡 When supplying both, if the env var is not set, it will use `PATH`.

The only transformation on the path made is to expand user constructs.
If the file does not exist it will be created (not parent directories though).
You can specify the file mode via `Config.FILE_MODE`.

## Read only
If you do not want to be able to modify the config from your code, you can use `ReadOnlyConfig`.

## Supported formats
Currently, those formats are supported:
- JSON
- YAML - requires the `yaml` extra
- TOML - requires the `toml` extra

The format is automatically inferred from the config file extension.
You can still specify it manually using `Config.FORMAT`, for custom ones or configuring dump options.

To use them:
```python
from dataclasses import dataclass
from zenconfig import Config
from zenconfig.formats.yaml import YAMLFormat

@dataclass
class MyYAMLConfig(Config):
    PATH = "~/myconfig.yaml"
```

Other formats can be added by subclassing either `Format` or `ReadOnlyFormat`

## Supported schemas
Currently, those schemas are supported:
- plain dict
- dataclasses
- pydantic models - requires the `pydantic` extra


The format is automatically inferred from the config class.
You can still specify it manually using `Config.SCHEMA`, for custom ones or configuring dump options.

To use pydantic:
```python
from typing import ClassVar
from pydantic import BaseModel
from zenconfig import Config

class MyPydanticConfig(Config, BaseModel):
    PATH: ClassVar[str] = "~/myconfig.yaml"
```

> ⚠️ When using pydantic, you have to supply the `ClassVar` type annotations
> otherwise pydantic will treat those as its own fields and complain.

