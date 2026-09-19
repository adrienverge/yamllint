from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem
from yamllint.rules.common import (
    spaces_after as spaces_after,
)
from yamllint.rules.common import (
    spaces_before as spaces_before,
)

_Config = _TypedDict(
    "_Config",
    {
        "forbid": bool | _Literal["non-empty"],
        "min-spaces-inside": int,
        "max-spaces-inside": int,
        "min-spaces-inside-empty": int,
        "max-spaces-inside-empty": int,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "forbid": tuple[type[bool], _Literal["non-empty"]],
        "min-spaces-inside": type[int],
        "max-spaces-inside": type[int],
        "min-spaces-inside-empty": type[int],
        "max-spaces-inside-empty": type[int],
    },
)

class _Context(_TypedDict): ...

ID: _Literal["braces"]
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
