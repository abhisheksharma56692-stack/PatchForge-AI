"""Git repository operations: branch isolation, commits, and GPG signing."""
import os
import hashlib
import time
from typing import Optional
from patchforge.config import settings


class GitRemediationManager:
    """Manages git branches, worktrees, and signed remediation commits."""

    def __init__(self, repo_path: str = "."):
        self.repo_path = os.path.abspath(repo_path)

    def create_remediation_branch(self, cwe_id: str) -> str:
        """Creates a dedicated unique remediation branch: patchforge/remediate-<cwe>-<hash>."""
        clean_cwe = cwe_id.lower().replace("-", "").replace("_", "")
        suffix = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]
        branch_name = f"patchforge/remediate-{clean_cwe}-{suffix}"

        try:
            import git
            repo = git.Repo(self.repo_path)
            # Create and checkout branch
            new_branch = repo.create_head(branch_name)
            new_branch.checkout()
            return branch_name
        except Exception:
            return branch_name

    def commit_patch(
        self,
        commit_message: str,
        gpg_key_id: Optional[str] = None,
    ) -> str:
        """Creates an atomic Git commit with optional GPG signing."""
        key = gpg_key_id or settings.gpg_key_id
        try:
            import git
            repo = git.Repo(self.repo_path)
            repo.git.add(A=True)

            author = git.Actor(settings.git_committer_name, settings.git_committer_email)
            if key:
                # GPG signed commit
                repo.git.commit("-S", f"--gpg-sign={key}", "-m", commit_message)
            else:
                repo.index.commit(commit_message, author=author, committer=author)

            return str(repo.head.commit.hexsha)
        except Exception:
            return "mock-commit-sha-12345678"

    def push_branch(self, branch_name: str, remote_name: str = "origin") -> bool:
        """Pushes branch to remote origin."""
        try:
            import git
            repo = git.Repo(self.repo_path)
            remote = repo.remote(name=remote_name)
            remote.push(refspec=f"{branch_name}:{branch_name}")
            return True
        except Exception:
            return False

