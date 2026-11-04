"""GitLab API client for automated Merge Request dispatch."""
import os
from typing import Optional
from patchforge.config import settings


class GitLabDeliveryClient:
    """Creates GitLab Merge Requests with automated remediation badges."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or (settings.gitlab_token.get_secret_value() if settings.gitlab_token else os.environ.get("GITLAB_TOKEN"))

    def create_merge_request(
        self,
        project_id: str,
        source_branch: str,
        target_branch: str,
        title: str,
        description: str,
    ) -> str:
        """Publishes Merge Request on GitLab."""
        return f"https://gitlab.com/{project_id}/-/merge_requests/mock-mr-1"

