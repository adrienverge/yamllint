from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

ID: _Literal["new-line-at-end-of-file"]
TYPE: _Literal["line"]

def check(
    conf: dict[str, object],
    line: _Line,
) -> _Iterator[LintProblem]: ...
