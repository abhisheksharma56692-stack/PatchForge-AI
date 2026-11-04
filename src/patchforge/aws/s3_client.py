"""Amazon S3 client for SARIF reports, diff artifacts, and V-BOM storage."""
import os
import boto3
from typing import Optional, Any
from patchforge.config import settings


class S3ArtifactClient:
    """Manages artifact persistence in Amazon S3."""

    def __init__(
        self,
        bucket_name: Optional[str] = None,
        region_name: Optional[str] = None,
        s3_client: Optional[Any] = None,
    ):
        self.bucket = bucket_name or settings.s3_artifact_bucket
        self.region = region_name or settings.aws_region
        self.client = s3_client or boto3.client("s3", region_name=self.region)

    def upload_sarif(self, file_path: str, run_id: str) -> str:
        """Uploads a raw SARIF report to S3 and returns the s3 uri."""
        key = f"runs/{run_id}/sarif/{os.path.basename(file_path)}"
        with open(file_path, "rb") as f:
            self.client.put_object(
                Bucket=self.bucket,
                Key=key,
                Body=f.read(),
                ContentType="application/json",
            )
        return f"s3://{self.bucket}/{key}"

    def upload_patch_artifact(self, patch_diff: str, run_id: str) -> str:
        """Uploads candidate unified diff to S3."""
        key = f"runs/{run_id}/patches/candidate_patch.diff"
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=patch_diff.encode("utf-8"),
            ContentType="text/x-diff",
        )
        return f"s3://{self.bucket}/{key}"

    def upload_vbom(self, vbom_json: str, run_id: str) -> str:
        """Uploads Verification Bill of Materials (V-BOM) to S3."""
        key = f"runs/{run_id}/vbom/verification_bom.json"
        self.client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=vbom_json.encode("utf-8"),
            ContentType="application/json",
        )
        return f"s3://{self.bucket}/{key}"

    def download_artifact(self, key: str) -> str:
        """Downloads an artifact from S3 as a UTF-8 string."""
        clean_key = key.replace(f"s3://{self.bucket}/", "")
        response = self.client.get_object(Bucket=self.bucket, Key=clean_key)
        return response["Body"].read().decode("utf-8")

