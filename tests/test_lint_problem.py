from pathlib import Path

import pytest

from yamllint.lint_problem import LintProblem


@pytest.mark.parametrize("test_line", [0, 1, 6, 666,],)
@pytest.mark.parametrize("test_column", [0, 1, 6, 666,],)
@pytest.mark.parametrize("test_level", ["error", "warning",])
def test_creation(test_line: int, test_column: int, test_level: str) -> None:
    # Arrange.
    test_path = Path("test.yaml")
    test_desc = "I Love Attrs"
    test_rule = "attrs"

    # Act.
    expected_result = LintProblem(file=test_path, line=test_line, column=test_column, desc=test_desc, rule=test_rule, level=test_level)

    # Assert.
    assert expected_result.file == test_path
    assert expected_result.line == test_line
    assert expected_result.column == test_column
    assert expected_result.desc == test_desc
    assert expected_result.rule == test_rule
    assert expected_result.level == test_level
