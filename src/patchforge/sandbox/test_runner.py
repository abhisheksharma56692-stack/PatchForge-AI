"""In-container test execution engine."""
import subprocess
from typing import Dict, Any


class SandboxTestRunner:
    """Executes baseline test suites and security reproduction tests."""

    def run_tests(self, cwd: str, command: str = "pytest", timeout_sec: int = 60) -> Dict[str, Any]:
        """Runs test command in directory and extracts pass/fail indicators."""
        try:
            res = subprocess.run(
                command,
                cwd=cwd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
            )
            passed = (res.returncode == 0)
            return {
                "exit_code": res.returncode,
                "passed": passed,
                "stdout": res.stdout,
                "stderr": res.stderr,
            }
        except subprocess.TimeoutExpired:
            return {
                "exit_code": 124,
                "passed": False,
                "stdout": "",
                "stderr": f"Test runner timed out after {timeout_sec} seconds.",
            }
        except Exception as e:
            return {
                "exit_code": 1,
                "passed": False,
                "stdout": "",
                "stderr": str(e),
            }

