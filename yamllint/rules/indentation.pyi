from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem
from yamllint.rules.common import (
    get_real_end_line as get_real_end_line,
)
from yamllint.rules.common import (
    is_explicit_key as is_explicit_key,
)

_Config = _TypedDict(
    "_Config",
    {
        "spaces": int | _Literal["consistent"],
        "indent-sequences": (
            bool | _Literal["whatever", "consistent"]
        ),
        "check-multi-line-strings": bool,
    },
)
_Conf = _TypedDict(
    "_Conf",
    {
        "spaces": tuple[type[int], _Literal["consistent"]],
        "indent-sequences": tuple[
            type[bool],
            _Literal["whatever"],
            _Literal["consistent"],
        ],
        "check-multi-line-strings": type[bool],
    },
)

ID: _Literal["indentation"]
TYPE: _Literal["token"]
CONF: _Conf
DEFAULT: _Config

ROOT: _Literal[0]
B_MAP: _Literal[1]
F_MAP: _Literal[2]
B_SEQ: _Literal[3]
F_SEQ: _Literal[4]
B_ENT: _Literal[5]
KEY: _Literal[6]
VAL: _Literal[7]
labels: tuple[
    _Literal["ROOT"],
    _Literal["B_MAP"],
    _Literal["F_MAP"],
    _Literal["B_SEQ"],
    _Literal["F_SEQ"],
    _Literal["B_ENT"],
    _Literal["KEY"],
    _Literal["VAL"],
]

class Parent:
    type: int
    indent: int
    line_indent: int | None
    explicit_key: bool
    implicit_block_seq: bool

    def __init__(
        self,
        type: int,
        indent: int,
        line_indent: int | None = None,
    ) -> None: ...

_Context = _TypedDict(
    "_Context",
    {
        "stack": list[Parent],
        "cur_line": int,
        "spaces": int | _Literal["consistent"],
        "indent-sequences": (
            bool | _Literal["whatever", "consistent"]
        ),
        "cur_line_indent": int,
    },
    total=False,
)

def check_scalar_indentation(
    conf: _Config,
    token: yaml.Token,
    context: _Context,
) -> _Iterator[LintProblem]: ...
def check(
    conf: _Config,
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    nextnext: yaml.Token | None,
    context: _Context,
) -> _Iterator[LintProblem]: ...
