from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "allowed-values": list[str],
        "check-keys": bool,
    },
)

TRUTHY_1_1: list[str]
TRUTHY_1_2: list[str]
ID: _Literal["truthy"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config

def yaml_spec_version_for_document(
    context: dict[str, object],
) -> object: ...
def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
