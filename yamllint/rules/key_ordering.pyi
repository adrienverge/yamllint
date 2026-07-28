from collections.abc import Iterator as _Iterator
from locale import strcoll as strcoll
import re as re
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict("_Config", {"ignored-keys": list[str]})

ID: _Literal["key-ordering"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config
MAP: _Literal[0]
SEQ: _Literal[1]

class Parent:
    type: int
    keys: list[object]

    def __init__(self, type: int) -> None: ...

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
