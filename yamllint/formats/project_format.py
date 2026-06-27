from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

from typing_extensions import Self

from yamllint.lint_problem import LintProblem


class ProjectFormat(ABC):
    @abstractmethod
    def format(self: Self, workdir: Path, problems: Iterable[LintProblem]) -> str:
        pass
