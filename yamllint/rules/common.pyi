import string as string

import yaml as yaml

from yamllint.linter import LintProblem as LintProblem

def spaces_after(
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    min: int = -1,
    max: int = -1,
    min_desc: str | None = None,
    max_desc: str | None = None,
) -> LintProblem | None: ...
def spaces_before(
    token: yaml.Token,
    prev: yaml.Token | None,
    next: yaml.Token | None,
    min: int = -1,
    max: int = -1,
    min_desc: str | None = None,
    max_desc: str | None = None,
) -> LintProblem | None: ...
def get_line_indent(token: yaml.Token) -> int: ...
def get_real_end_line(token: yaml.Token) -> int: ...
def is_explicit_key(token: yaml.Token) -> bool: ...
