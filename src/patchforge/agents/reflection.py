"""Reflection engine: parses sandbox stderr, compiler errors, and traces into actionable critique."""
import re
from typing import List, Optional
from patchforge.models.sandbox import SandboxResult
from patchforge.models.agents import ReflectionFeedback


class ReflectionEngine:
    """
    Parses sandbox telemetry (exit codes, stderr, stack traces, assertion failures)
    into structured diagnostic critique for Agent Beta's iterative self-healing.
    """

    def critique(self, sandbox_result: SandboxResult, iteration: int) -> ReflectionFeedback:
        """Analyzes SandboxResult and builds a diagnostic critique."""
        stderr = sandbox_result.stderr or ""
        stdout = sandbox_result.stdout or ""
        combined_logs = f"{stdout}\n{stderr}"

        failed_tests = self._extract_failed_tests(combined_logs)
        compiler_errors = self._extract_compiler_errors(combined_logs)
        stack_trace = self._extract_stack_trace(combined_logs)

        # Generate actionable advice
        critiques = []
        if compiler_errors:
            critiques.append(f"Syntax/Compiler Error: {compiler_errors[0]}. Please correct the syntax in the patch.")
        elif failed_tests:
            critiques.append(f"Test Assertion Failure: {failed_tests[0]}. Ensure all input parameters and expected behaviors match.")
        elif not sandbox_result.reproduction_defended:
            critiques.append("Reproduction PoC was NOT defended. The vulnerability is still exploitable.")
        elif not sandbox_result.baseline_passed:
            critiques.append("Baseline test regression occurred. The patch broke existing functionality.")
        else:
            critiques.append("Execution failed with non-zero exit code. Review logs and adjust patch.")

        actionable = " ".join(critiques)
        summary = f"Iteration {iteration} failed (Exit Code {sandbox_result.exit_code}). {len(failed_tests)} tests failed."

        return ReflectionFeedback(
            iteration=iteration,
            failure_summary=summary,
            actionable_critique=actionable,
            failed_tests=failed_tests,
            compiler_errors=compiler_errors,
            stack_trace_snippet=stack_trace[:1500] if stack_trace else None,
        )

    def _extract_failed_tests(self, logs: str) -> List[str]:
        """Extracts failed test identifiers from pytest or mocha output."""
        failed = []
        # pytest: FAILED test_file.py::test_case - AssertionError
        pytest_fails = re.findall(r"FAILED\s+([^\s]+)", logs)
        failed.extend(pytest_fails)

        # Assertion errors
        assert_errors = re.findall(r"(AssertionError:.*)", logs)
        failed.extend(assert_errors[:3])

        return list(set(failed))

    def _extract_compiler_errors(self, logs: str) -> List[str]:
        """Extracts SyntaxError, TypeError, or compilation errors."""
        errors = []
        syntax_errs = re.findall(r"(SyntaxError:.*)", logs)
        errors.extend(syntax_errs)
        type_errs = re.findall(r"(TypeError:.*)", logs)
        errors.extend(type_errs)
        name_errs = re.findall(r"(NameError:.*)", logs)
        errors.extend(name_errs)
        return errors

    def _extract_stack_trace(self, logs: str) -> str:
        """Extracts Python traceback snippet if present."""
        tb_match = re.search(r"(Traceback \(most recent call last\):.*?)(?:\n\n|\Z)", logs, re.DOTALL)
        if tb_match:
            return tb_match.group(1).strip()
        return logs[:1000]

