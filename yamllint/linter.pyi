from collections.abc import Iterator as _Iterator
import io as io
import re as re
from typing import Literal as _Literal

import yaml as yaml

from yamllint import decoder as decoder
from yamllint import parser as parser
from yamllint.config import YamlLintConfig as _YamlLintConfig

PROBLEM_LEVELS: dict[int | str | None, int | str | None]
DISABLE_RULE_PATTERN: re.Pattern[str]
ENABLE_RULE_PATTERN: re.Pattern[str]

class LintProblem:
    line: int
    column: int
    desc: str
    rule: str | None
    level: _Literal["warning", "error"] | None

    def __init__(
        self,
        line: int,
        column: int,
        desc: str = "<no description>",
        rule: str | None = None,
    ) -> None: ...

    @property
    def message(self) -> str: ...

    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: LintProblem) -> bool: ...

def get_cosmetic_problems(
    buffer: str,
    conf: _YamlLintConfig,
    filepath: str | None,
) -> _Iterator[LintProblem]: ...
def get_syntax_error(buffer: str) -> LintProblem | None: ...
def _run(
    buffer: str | bytes,
    conf: _YamlLintConfig,
    filepath: str | None,
) -> _Iterator[LintProblem]: ...
def run(
    input: str | bytes | io.IOBase,
    conf: _YamlLintConfig,
    filepath: str | None = None,
) -> _Iterator[LintProblem] | tuple[()]: ...
