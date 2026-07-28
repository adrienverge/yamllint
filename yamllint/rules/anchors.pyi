from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "forbid-undeclared-aliases": bool,
        "forbid-duplicated-anchors": bool,
        "forbid-unused-anchors": bool,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "forbid-undeclared-aliases": type[bool],
        "forbid-duplicated-anchors": type[bool],
        "forbid-unused-anchors": type[bool],
    },
)

class _AnchorInfo(_TypedDict):
    line: int
    column: int
    used: bool

class _Context(_TypedDict, total=False):
    anchors: dict[str, _AnchorInfo]

ID: _Literal["anchors"]
TYPE: _Literal["token"]
CONF: _Conf
DEFAULT: _Config

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: _Context,
) -> _Iterator[LintProblem]: ...
