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


@pytest.mark.parametrize(
    (
        "first_problem",
        "second_problem",
    ),
    [
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test2.yaml"),
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
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test1.yaml"),
                line=7,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different line",
        ),
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=7,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different column",
        ),
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test2.yaml"),
                line=8,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="File and Line in reverse",
        ),
        pytest.param(
            LintProblem(
                file=Path("test.yaml"),
                line=5,
                column=20,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="Line And Column",
        ),
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test2.yaml"),
                line=6,
                column=20,
                desc="Grrr",
                rule="Grrr",
                level="Heaven",
            ),
            id="File And Column",
        ),
    ],
)
def test_order(first_problem: LintProblem, second_problem: LintProblem) -> None:
    assert first_problem < second_problem
    assert not (first_problem >= second_problem)


@pytest.mark.parametrize(
    ("problem1", "problem2"),
    [
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="rule1",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="rule2",
                level="Heaven",
            ),
            id="Different rule",
        ),
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="1",
            ),
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="Grrr",
                rule="Grrr",
                level="2",
            ),
            id="Different level",
        ),
        pytest.param(
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="desc1",
                rule="Grrr",
                level="Heaven",
            ),
            LintProblem(
                file=Path("test1.yaml"),
                line=6,
                column=6,
                desc="desc2",
                rule="Grrr",
                level="Heaven",
            ),
            id="Different decs",
        ),
    ],
)
def test_exluded_fields_dont_affect_order(
    problem1: LintProblem,
    problem2: LintProblem,
) -> None:
    assert not problem1 > problem2
    assert not problem1 < problem2
