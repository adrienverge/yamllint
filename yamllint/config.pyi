import os as os
from types import ModuleType as _ModuleType
from typing import Literal as _Literal
from typing import TypeAlias as _TypeAlias
from typing import overload as _overload

from pathspec import GitIgnoreSpec as GitIgnoreSpec
import yaml as yaml

import yamllint as yamllint
from yamllint import decoder as decoder

_Path: _TypeAlias = (
    str | bytes | os.PathLike[str] | os.PathLike[bytes]
)
_RuleConfiguration: _TypeAlias = dict[str, object] | _Literal[False]

class YamlLintConfigError(Exception): ...

class YamlLintConfig:
    ignore: GitIgnoreSpec | None
    yaml_files: GitIgnoreSpec
    locale: str | None
    rules: dict[str, _RuleConfiguration]

    @_overload
    def __init__(
        self,
        content: str | bytes,
        file: None = None,
    ) -> None: ...
    @_overload
    def __init__(self, content: None, file: _Path) -> None: ...
    @_overload
    def __init__(self, *, file: _Path) -> None: ...

    def is_file_ignored(self, filepath: str) -> bool | None: ...
    def is_yaml_file(self, filepath: str) -> bool: ...
    def enabled_rules(self, filepath: str | None) -> list[_ModuleType]: ...
    def extend(self, base_config: YamlLintConfig) -> None: ...
    def parse(self, raw_content: str | bytes) -> None: ...
    def validate(self) -> None: ...

def validate_rule_conf(
    rule: _ModuleType,
    conf: _RuleConfiguration,
) -> _RuleConfiguration: ...
def get_extended_config_file(name: str) -> str: ...
