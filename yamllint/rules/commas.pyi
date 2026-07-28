from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem
from yamllint.rules.common import (
    spaces_after as spaces_after,
)
from yamllint.rules.common import (
    spaces_before as spaces_before,
)

_Config = _TypedDict(
    "_Config",
    {
        "max-spaces-before": int,
        "min-spaces-after": int,
        "max-spaces-after": int,
    },
)

ID: _Literal["commas"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
