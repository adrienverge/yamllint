from collections.abc import Iterator as _Iterator
from locale import strcoll as strcoll
import re as re
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict("_Config", {"ignored-keys": list[str]})
_Conf = _TypedDict("_Conf", {"ignored-keys": list[type[str]]})

ID: _Literal["key-ordering"]
TYPE: _Literal["token"]
CONF: _Conf
DEFAULT: _Config
MAP: _Literal[0]
SEQ: _Literal[1]

class Parent:
    type: int
    keys: list[str]

    def __init__(self, type: int) -> None: ...

class _Context(_TypedDict, total=False):
    stack: list[Parent]

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: _Context,
) -> _Iterator[LintProblem]: ...
