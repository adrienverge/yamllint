from collections.abc import Collection, Mapping
import json
from typing import Any

from typing_extensions import Self, override

from yamllint.lint_problem import LintProblem

from .project_format import ProjectFormat


class CodeClimateFormat(ProjectFormat):
    def __init__(self: Self):
        super().__init__()

    @override
    def format(self: Self, workdir: Path, problems: Iterable[LintProblem]) -> str:
        dict_format: Collection[Mapping[str, Any]] = []
        return json.dumps(dict_format)
