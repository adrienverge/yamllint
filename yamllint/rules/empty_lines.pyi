from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

_Config = _TypedDict(
    "_Config",
    {
        "max": int,
        "max-start": int,
        "max-end": int,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {"max": type[int], "max-start": type[int], "max-end": type[int]},
)

ID: _Literal["empty-lines"]
TYPE: _Literal["line"]
CONF: _Conf
DEFAULT: _Config

def check(conf: _Config, line: _Line) -> _Iterator[LintProblem]: ...
