"""Integration tests for AWS services using moto."""
import os
import boto3
import pytest
from moto import mock_aws
from patchforge.aws.s3_client import S3ArtifactClient
from patchforge.aws.sqs_client import SQSVulnerabilityQueue
from patchforge.aws.dynamodb_client import DynamoDBAuditLogger


@mock_aws
def test_s3_artifact_upload_download(tmp_path):
    region = "us-east-1"
    bucket_name = "test-patchforge-artifacts"
    s3 = boto3.client("s3", region_name=region)
    s3.create_bucket(Bucket=bucket_name)

    client = S3ArtifactClient(bucket_name=bucket_name, region_name=region, s3_client=s3)

    # Test SARIF upload
    sarif_file = tmp_path / "test.sarif"
    sarif_file.write_text('{"runs": []}', encoding="utf-8")
    s3_uri = client.upload_sarif(str(sarif_file), run_id="run-123")
    assert s3_uri.startswith("s3://test-patchforge-artifacts/runs/run-123/sarif/")

    # Test patch diff upload & download
    diff_content = "--- a/app.py\n+++ b/app.py\n@@ -1,1 +1,1 @@\n"
    patch_uri = client.upload_patch_artifact(diff_content, run_id="run-123")
    downloaded = client.download_artifact(patch_uri)
    assert downloaded == diff_content

    # Test V-BOM upload
    vbom = client.upload_vbom('{"vbom": "clean"}', run_id="run-123")
    assert "verification_bom.json" in vbom


@mock_aws
def test_sqs_vulnerability_queue():
    region = "us-east-1"
    sqs = boto3.client("sqs", region_name=region)
    q_res = sqs.create_queue(QueueName="test-vuln-queue")
    q_url = q_res["QueueUrl"]

    queue = SQSVulnerabilityQueue(queue_url=q_url, region_name=region, sqs_client=sqs)

    # Send event
    msg_id = queue.send_vulnerability_event({"finding_id": "cwe89-01", "cwe": "CWE-89"})
    assert msg_id is not None

    # Poll events
    events = queue.poll_vulnerability_events(max_messages=1)
    assert len(events) == 1
    assert events[0]["data"]["cwe"] == "CWE-89"

    # Delete event
    receipt = events[0]["receipt_handle"]
    queue.delete_event(receipt)

    # Queue should be empty now
    empty_events = queue.poll_vulnerability_events(max_messages=1, wait_time_sec=0)
    assert len(empty_events) == 0


@mock_aws
def test_dynamodb_audit_trail():
    region = "us-east-1"
    table_name = "PatchForgeAuditTrail"
    dynamodb = boto3.resource("dynamodb", region_name=region)

    # Create table schema
    dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "run_id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "run_id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )

    logger = DynamoDBAuditLogger(table_name=table_name, region_name=region, dynamodb_resource=dynamodb)

    # Record run
    logger.record_run(
        run_id="run-cwe89-99",
        cwe_id="CWE-89",
        status="TOMBSTONE_READY",
        duration=15.2,
        pr_url="https://github.com/org/repo/pull/99",
        tombstone_inscription="⚰️ R.I.P. CWE-89 (SQLi) — Neutralized",
    )

    # Read back
    record = logger.get_run("run-cwe89-99")
    assert record is not None
    assert record["cwe_id"] == "CWE-89"
    assert record["status"] == "TOMBSTONE_READY"
    assert record["is_remediated"] is True

    # Test Graveyard retrieval
    graveyard = logger.get_graveyard_records()
    assert len(graveyard) == 1
    assert "R.I.P." in graveyard[0]["tombstone_inscription"]

