from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as _LintProblem
from yamllint.rules.common import (
    is_explicit_key as is_explicit_key,
)
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
        "max-spaces-after": int,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {"max-spaces-before": type[int], "max-spaces-after": type[int]},
)

class _Context(_TypedDict): ...

ID: _Literal["colons"]
TYPE: _Literal["token"]
CONF: _Conf
DEFAULT: _Config

def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: _Context,
) -> _Iterator[_LintProblem]: ...
