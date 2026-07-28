import argparse as argparse
from collections.abc import Iterable as _Iterable
from collections.abc import Iterator as _Iterator
import locale as locale
import os as os
import platform as platform
import sys as sys
from typing import Literal as _Literal
from typing import NoReturn as _NoReturn
from typing import TypeAlias as _TypeAlias

from yamllint import (
    APP_DESCRIPTION as APP_DESCRIPTION,
)
from yamllint import (
    APP_NAME as APP_NAME,
)
from yamllint import (
    APP_VERSION as APP_VERSION,
)
from yamllint import (
    linter as linter,
)
from yamllint.config import (
    YamlLintConfig as YamlLintConfig,
)
from yamllint.config import (
    YamlLintConfigError as YamlLintConfigError,
)
from yamllint.linter import (
    PROBLEM_LEVELS as PROBLEM_LEVELS,
)
from yamllint.linter import (
    LintProblem as _LintProblem,
)

_OutputFormat: _TypeAlias = _Literal[
    "auto", "colored", "github", "parsable", "standard"
]

def find_files_recursively(
    items: _Iterable[str],
    conf: YamlLintConfig,
) -> _Iterator[str]: ...
def supports_color() -> bool: ...

class Format:
    @staticmethod
    def parsable(problem: _LintProblem, filename: str) -> str: ...
    @staticmethod
    def standard(problem: _LintProblem, filename: str) -> str: ...
    @staticmethod
    def standard_color(problem: _LintProblem, filename: str) -> str: ...
    @staticmethod
    def github(problem: _LintProblem, filename: str) -> str: ...

def show_problems(
    problems: _Iterable[_LintProblem],
    file: str,
    args_format: _OutputFormat,
    no_warn: bool,
) -> int: ...
def find_project_config_filepath(path: str = ".") -> str | None: ...
def run(argv: _Iterable[str] | None = None) -> _NoReturn: ...
