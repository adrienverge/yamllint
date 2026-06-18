from pathlib import Path
from typing import Annotated

from attrs import define, field
from annotated_types import Ge, MinLen


@define(frozen=True, eq=True, order=True,)
class LintProblem:
    file: Path
    line: Annotated[int, Ge(0)]
    column: Annotated[int, Ge(0)]
    desc: str = field(eq=False, order=False,)
    rule: Annotated[str, MinLen(1)] | None = field(order=False,)
    # Don't compare the level as if they
    # point to the same location and talk about
    # the same thing, that's enough.
    level: str | None = field(eq=False, order=False,)
