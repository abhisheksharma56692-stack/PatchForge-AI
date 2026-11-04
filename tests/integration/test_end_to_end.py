"""Full End-to-End integration test across all Member 1 & Member 2 subsystems."""
import os
import boto3
import pytest
from moto import mock_aws
from patchforge.orchestrator.graph import RemediationPipelineGraph
from patchforge.aws.s3_client import S3ArtifactClient
from patchforge.aws.dynamodb_client import DynamoDBAuditLogger


@mock_aws
def test_full_remediation_pipeline_end_to_end(tmp_path):
    region = "us-east-1"
    
    # 1. Setup mock S3
    s3 = boto3.client("s3", region_name=region)
    s3.create_bucket(Bucket="patchforge-artifacts")
    s3_client = S3ArtifactClient(bucket_name="patchforge-artifacts", region_name=region, s3_client=s3)

    # 2. Setup mock DynamoDB
    dynamodb = boto3.resource("dynamodb", region_name=region)
    dynamodb.create_table(
        TableName="PatchForgeAuditTrail",
        KeySchema=[{"AttributeName": "run_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "run_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    # Upload input SARIF to S3
    sarif_file = "tests/fixtures/sarif/semgrep_cwe89_sqli.sarif.json"
    s3_uri = s3_client.upload_sarif(sarif_file, run_id="e2e-run-1")
    assert s3_uri is not None

    # Run the orchestrator pipeline
    os.environ["PATCHFORGE_USE_STUBS"] = "true"
    pipeline = RemediationPipelineGraph()

    initial_state = {
        "sarif_raw": {"file_path": sarif_file, "s3_uri": s3_uri},
        "vulnerability": None,
        "cwe_id": "CWE-UNKNOWN",
        "cve_id": None,
        "ast_slice": None,
        "formal_invariants": None,
        "reproduction_test": None,
        "candidate_patch_diff": None,
        "iteration_count": 0,
        "max_iterations": 5,
        "error_feedback_history": [],
        "sandbox_result": None,
        "audit_passed": False,
        "pr_url": None,
        "status": "AWAKENING",
    }

    final_state = pipeline.invoke(initial_state)

    # Verify pipeline state completion
    assert final_state["status"] == "TOMBSTONE_READY"
    assert final_state["cwe_id"] == "CWE-89"
    assert "github.com" in final_state["pr_url"]

    # Verify audit trail in DynamoDB
    db = DynamoDBAuditLogger(table_name="PatchForgeAuditTrail", region_name=region, dynamodb_resource=dynamodb)
    records = db.get_graveyard_records()
    assert len(records) >= 1
    assert records[0]["status"] == "TOMBSTONE_READY"
    assert "R.I.P." in records[0]["tombstone_inscription"]

