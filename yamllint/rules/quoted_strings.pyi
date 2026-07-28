from collections.abc import Iterator as _Iterator
import re as re
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

_Config = _TypedDict(
    "_Config",
    {
        "quote-type": _Literal[
            "any", "single", "double", "consistent"
        ],
        "required": bool | _Literal["only-when-needed"],
        "extra-required": list[str],
        "extra-allowed": list[str],
        "allow-quoted-quotes": bool,
        "check-keys": bool,
    },
)

ID: _Literal["quoted-strings"]
TYPE: _Literal["token"]
CONF: dict[str, object]
DEFAULT: _Config
DEFAULT_SCALAR_TAG: _Literal["tag:yaml.org,2002:str"]

def VALIDATE(conf: _Config) -> str | None: ...
def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: dict[str, object],
) -> _Iterator[LintProblem]: ...
