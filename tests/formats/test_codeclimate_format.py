from collections.abc import Iterable
import json
from pathlib import Path
from typing import Any

import pytest

from yamllint.lint_problem import LintProblem

from yamllint.formats.codeclimate_format import CodeClimateFormat

@pytest.mark.parametrize(
    "problems",
    [
        pytest.param(
            [[]],
            id="no problems",
        ),
        pytest.param(
            [
                [
                    LintProblem(
                        file=Path("test.yaml"),
                        line=6,
                        column=6,
                        desc="Test 1",
                        rule="Test 1",
                        level="error",
                    )
                ]
            ],
            id="single error",
        ),
    ],
)
def test_format(problems: Iterable[LintProblem]) -> None:
    # Arrange.
    workdir: Path = Path("/my/workdir")
    expected_output_object: list[dict[str, Any]] = [
        {
            "type": "issue",
            "check_name": problem.rule,
            "description": problem.desc,
            "fingerprint": f"{problem.file!s}:{problem.line}:{problem.column}:{problem.rule}",
            "categories": [],  # Currently do not support categories.
            "location": {
                "path": (
                    problem.file.relative_to(workdir)
                    if problem.file.is_absolute()
                    else problem.file
                ).as_posix(),
                "lines": {
                    "begin": problem.line,
                },
                "severity": "minor" if problem.level == "warning" else "major"
            },
        }
        for problem in problems
    ]
    
    # Act.
    actual_output = CodeClimateFormat().format(workdir, problems)

    # Assert.
    assert actual_output == json.dumps(expected_output_object)
