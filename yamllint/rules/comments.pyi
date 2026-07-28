from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Comment as _Comment

_Config = _TypedDict(
    "_Config",
    {
        "require-starting-space": bool,
        "ignore-shebangs": bool,
        "min-spaces-from-content": int,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "require-starting-space": type[bool],
        "ignore-shebangs": type[bool],
        "min-spaces-from-content": type[int],
    },
)

ID: _Literal["comments"]
TYPE: _Literal["comment"]
CONF: _Conf
DEFAULT: _Config

def check(
    conf: _Config,
    comment: _Comment,
) -> _Iterator[LintProblem]: ...
