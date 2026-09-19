from collections.abc import Iterator as _Iterator
import re as re
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "forbid-implicit-octal": bool,
        "forbid-explicit-octal": bool,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "forbid-implicit-octal": type[bool],
        "forbid-explicit-octal": type[bool],
    },
)

class _Context(_TypedDict): ...

ID: _Literal["octal-values"]
TYPE: _Literal["token"]
CONF: _Conf
DEFAULT: _Config
IS_OCTAL_NUMBER_PATTERN: re.Pattern[str]

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: _Context,
) -> _Iterator[LintProblem]: ...
