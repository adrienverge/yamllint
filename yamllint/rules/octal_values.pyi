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

ID: _Literal["octal-values"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config
IS_OCTAL_NUMBER_PATTERN: re.Pattern[str]

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
