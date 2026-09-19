from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "forbid-in-block-mappings": bool,
        "forbid-in-flow-mappings": bool,
        "forbid-in-block-sequences": bool,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "forbid-in-block-mappings": type[bool],
        "forbid-in-flow-mappings": type[bool],
        "forbid-in-block-sequences": type[bool],
    },
)

class _Context(_TypedDict): ...

ID: _Literal["empty-values"]
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
