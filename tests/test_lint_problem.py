from pathlib import Path

import pytest

from yamllint.lint_problem import LintProblem


@pytest.mark.parametrize(
    "test_line",
    [
        0,
        1,
        6,
        666,
    ],
)
@pytest.mark.parametrize(
    "test_column",
    [
        0,
        1,
        6,
        666,
    ],
)
@pytest.mark.parametrize(
    "test_level",
    [
        "error",
        "warning",
    ],
)
@pytest.mark.parametrize(
    "test_rule",
    [
        None,
        "my-rule",
    ],
)
def test_creation(
    test_line: int, test_column: int, test_level: str, test_rule: str
) -> None:
    # Arrange.
    test_path = Path("test.yaml")
    test_desc = "I Love Attrs"

    # Act.
    expected_result = LintProblem(
        file=test_path,
        line=test_line,
        column=test_column,
        desc=test_desc,
        rule=test_rule,
        level=test_level,
    )

    # Assert.
    assert expected_result.file == test_path
    assert expected_result.line == test_line
    assert expected_result.column == test_column
    assert expected_result.desc == test_desc
    assert expected_result.rule == test_rule
    assert expected_result.level == test_level


@pytest.mark.parametrize(
    (
        "problem1",
        "problem2",
    ),
    [
        pytest.param(
            *(
                LintProblem(
                    file=Path("test.yaml"),
                    line=6,
                    column=6,
                    desc="Grrr",
                    rule="Grrr",
                    level="Heaven",
                ),
            )
            * 2,
            id="Exactly the same items.",
        ),
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="GuraGura",
                rule="Grrr",
                level="Hell",
            ),
            id="Equal only on the necessary fields",
        ),
    ],
)
def test_equation_on_equal_problems(
    problem1: LintProblem,
    problem2: LintProblem,
) -> None:
    # Act & Assert.
    assert problem1 == problem2


@pytest.mark.parametrize(
    (
        "problem1",
        "problem2",
    ),
    [
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("actual_test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different file",
        ),
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="GuraGura",
                level="Heaven",
            ),
            id="Different rule",
        ),
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test.yaml"),
                line=67,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different line",
        ),
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=67,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different column",
        ),
    ],
)
def test_equation_on_non_equal_problems(
    problem1: LintProblem,
    problem2: LintProblem,
) -> None:
    # Act & Assert.
    assert problem1 != problem2
