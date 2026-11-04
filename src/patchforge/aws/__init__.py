"""AWS Cloud Services integration layer for PatchForge AI."""
from patchforge.aws.s3_client import S3ArtifactClient
from patchforge.aws.sqs_client import SQSVulnerabilityQueue
from patchforge.aws.dynamodb_client import DynamoDBAuditLogger
from patchforge.aws.ecr_client import ECRRuntimeRegistry

__all__ = [
    "S3ArtifactClient",
    "SQSVulnerabilityQueue",
    "DynamoDBAuditLogger",
    "ECRRuntimeRegistry",
]

