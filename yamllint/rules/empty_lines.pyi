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

ID: _Literal["empty-lines"]
TYPE: _Literal["line"]
CONF: dict[str, object]
DEFAULT: _Config

def check(conf: _Config, line: _Line) -> _Iterator[LintProblem]: ...
