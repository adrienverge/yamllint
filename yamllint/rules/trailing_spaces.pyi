from collections.abc import Iterator as _Iterator
import string as string
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

class _Config(_TypedDict): ...

ID: _Literal["trailing-spaces"]
TYPE: _Literal["line"]

def check(
    conf: _Config,
    line: _Line,
) -> _Iterator[LintProblem]: ...
