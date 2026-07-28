from collections.abc import Iterator as _Iterator
import re as re
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "require-numeral-before-decimal": bool,
        "forbid-scientific-notation": bool,
        "forbid-nan": bool,
        "forbid-inf": bool,
    },
)

ID: _Literal["float-values"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config
IS_NUMERAL_BEFORE_DECIMAL_PATTERN: re.Pattern[str]
IS_SCIENTIFIC_NOTATION_PATTERN: re.Pattern[str]
IS_INF_PATTERN: re.Pattern[str]
IS_NAN_PATTERN: re.Pattern[str]

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
