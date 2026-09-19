from collections.abc import Iterator as _Iterator
from typing import Literal as _Literal
from typing import TypedDict as _TypedDict

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

class _Config(_TypedDict):
    present: bool

class _Conf(_TypedDict):
    present: type[bool]

class _Context(_TypedDict): ...

ID: _Literal["document-end"]
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
) -> _Iterator[LintProblem]: ...
