"""Unit tests for Reflection Engine."""
import pytest
from patchforge.agents.reflection import ReflectionEngine
from patchforge.models.sandbox import SandboxResult


def test_reflection_syntax_error():
    engine = ReflectionEngine()
    sandbox_result = SandboxResult(
        exit_code=1,
        baseline_passed=False,
        reproduction_defended=False,
        stdout="",
        stderr="File 'app.py', line 28\n    cursor.execute(query,\n                         ^\nSyntaxError: unexpected EOF while parsing",
    )

    feedback = engine.critique(sandbox_result, iteration=1)
    assert feedback.iteration == 1
    assert "SyntaxError" in feedback.actionable_critique
    assert len(feedback.compiler_errors) >= 1


def test_reflection_test_assertion_failure():
    engine = ReflectionEngine()
    sandbox_result = SandboxResult(
        exit_code=1,
        baseline_passed=False,
        reproduction_defended=True,
        stdout="FAILED tests/test_app.py::test_user_list\nAssertionError: assert 0 == 1",
        stderr="",
    )

    feedback = engine.critique(sandbox_result, iteration=2)
    assert feedback.iteration == 2
    assert "AssertionError" in feedback.actionable_critique or "Test Assertion Failure" in feedback.actionable_critique
    assert any("FAILED" in t or "test_user_list" in t for t in feedback.failed_tests)


def test_reflection_reproduction_not_defended():
    engine = ReflectionEngine()
    sandbox_result = SandboxResult(
        exit_code=1,
        baseline_passed=True,
        reproduction_defended=False,
        stdout="All baseline tests passed.",
        stderr="PoC exploit succeeded: SQL injection triggered.",
    )

    feedback = engine.critique(sandbox_result, iteration=1)
    assert "NOT defended" in feedback.actionable_critique


def test_reflection_extracts_stack_trace():
    engine = ReflectionEngine()
    logs = (
        "Starting test runner...\n"
        "Traceback (most recent call last):\n"
        "  File 'app.py', line 30, in get_user\n"
        "    cursor.execute(query, username)\n"
        "TypeError: parameters must be a tuple or list\n\n"
        "Finished."
    )
    sandbox_result = SandboxResult(
        exit_code=1,
        baseline_passed=False,
        reproduction_defended=False,
        stdout="",
        stderr=logs,
    )

    feedback = engine.critique(sandbox_result, iteration=3)
    assert feedback.stack_trace_snippet is not None
    assert "TypeError: parameters must be a tuple or list" in feedback.stack_trace_snippet

