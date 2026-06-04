from abc import ABC, abstractmethod
from collections.abc import Iterable
from pathlib import Path

from yamllint.linter import LintProblem

class ProjectFormat(ABC):
    @abstractmethod
    def format(workdir: Path, problems: Iterable[LintProblem]) -> str:
        pass
