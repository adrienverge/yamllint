from abc import ABC, abstractmethod
from pathlib import Path

class ProjectFormat(ABC):
    @abstractmethod
    def format(workdir: Path) -> str:
        pass
