from collections.abc import Iterator as _Iterator
from os import linesep as linesep
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

class _Config(_TypedDict):
    type: _Literal["unix", "dos", "platform"]

class _Conf(_TypedDict):
    type: tuple[
        _Literal["unix"],
        _Literal["dos"],
        _Literal["platform"],
    ]

ID: _Literal["new-lines"]
TYPE: _Literal["line"]
CONF: _Conf
DEFAULT: _Config

def check(conf: _Config, line: _Line) -> _Iterator[LintProblem]: ...
