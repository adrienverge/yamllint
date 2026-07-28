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
        "forbid": bool | _Literal["non-empty"],
        "min-spaces-inside": int,
        "max-spaces-inside": int,
        "min-spaces-inside-empty": int,
        "max-spaces-inside-empty": int,
    },
)

ID: _Literal["brackets"]
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
