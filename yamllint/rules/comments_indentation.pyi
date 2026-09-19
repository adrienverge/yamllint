from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Comment as _Comment
from yamllint.rules.common import get_line_indent as get_line_indent

class _Config(_TypedDict): ...

ID: _Literal["comments-indentation"]
TYPE: _Literal["comment"]

def check(
    conf: _Config,
    comment: _Comment,
) -> _Iterator[LintProblem]: ...
