"""Applies unified git diff patches inside sandbox workspace directories."""
import os
import subprocess
from typing import Tuple


class PatchApplier:
    """Safely applies candidate patches using git apply."""

    def apply_patch(self, repo_dir: str, patch_diff: str) -> Tuple[bool, str]:
        """
        Applies a unified diff patch to repo_dir.
        Returns (success: bool, output/error: str).
        """
        patch_file = os.path.join(repo_dir, "temp_candidate.patch")
        try:
            with open(patch_file, "w", encoding="utf-8") as f:
                f.write(patch_diff)

            # Try git apply
            cmd = ["git", "apply", "--whitespace=nowarn", patch_file]
            result = subprocess.run(
                cmd,
                cwd=repo_dir,
                capture_output=True,
                text=True,
            )

            if result.returncode == 0:
                return True, "Patch applied successfully."
            else:
                return False, f"Git apply failed: {result.stderr}"
        except Exception as e:
            return False, f"Patch apply error: {str(e)}"
        finally:
            if os.path.exists(patch_file):
                try:
                    os.remove(patch_file)
                except OSError:
                    pass

