from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "forbid-undeclared-aliases": bool,
        "forbid-duplicated-anchors": bool,
        "forbid-unused-anchors": bool,
    },
)

ID: _Literal["anchors"]
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
