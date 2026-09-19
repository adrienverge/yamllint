from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem
from yamllint.parser import Line as _Line

_Config = _TypedDict(
    "_Config",
    {
        "max": int,
        "allow-non-breakable-words": bool,
        "allow-non-breakable-inline-mappings": bool,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "max": type[int],
        "allow-non-breakable-words": type[bool],
        "allow-non-breakable-inline-mappings": type[bool],
    },
)

ID: _Literal["line-length"]
TYPE: _Literal["line"]
CONF: _Conf
DEFAULT: _Config

def check_inline_mapping(line: _Line) -> bool: ...
def check(conf: _Config, line: _Line) -> _Iterator[LintProblem]: ...
