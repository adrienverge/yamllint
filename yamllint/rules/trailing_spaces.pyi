from collections.abc import Iterator as _Iterator
import string as string
from typing import Literal as _Literal

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

ID: _Literal["trailing-spaces"]
TYPE: _Literal["line"]

def check(
    conf: dict[str, object],
    line: _Line,
) -> _Iterator[LintProblem]: ...
