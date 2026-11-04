"""Amazon DynamoDB client for remediation audit trails and graveyard history."""
import time
from typing import Dict, Any, List, Optional
import boto3
from patchforge.config import settings


class DynamoDBAuditLogger:
    """Manages audit trails and historical run records in Amazon DynamoDB."""

    def __init__(
        self,
        table_name: Optional[str] = None,
        region_name: Optional[str] = None,
        dynamodb_resource: Optional[Any] = None,
    ):
        self.table_name = table_name or settings.dynamodb_table_name
        self.region = region_name or settings.aws_region
        self.dynamodb = dynamodb_resource or boto3.resource("dynamodb", region_name=self.region)
        self.table = self.dynamodb.Table(self.table_name)

    def record_run(
        self,
        run_id: str,
        cwe_id: str,
        status: str,
        duration: float,
        pr_url: Optional[str] = None,
        tombstone_inscription: Optional[str] = None,
    ) -> None:
        """Writes an execution record to the audit trail table."""
        timestamp = int(time.time())
        item = {
            "run_id": run_id,
            "timestamp": timestamp,
            "cwe_id": cwe_id,
            "status": status,
            "duration": str(duration),
            "pr_url": pr_url or "NONE",
            "tombstone_inscription": tombstone_inscription or f"⚰️ R.I.P. {cwe_id} — Neutralized",
            "is_remediated": status in {"TOMBSTONE_READY", "SUCCEEDED"},
        }
        try:
            self.table.put_item(Item=item)
        except Exception:
            pass

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single run record by partition key."""
        try:
            response = self.table.get_item(Key={"run_id": run_id})
            return response.get("Item")
        except Exception:
            return None

    def get_run_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Scans recent remediation runs."""
        try:
            response = self.table.scan(Limit=limit)
            return response.get("Items", [])
        except Exception:
            return []

    def get_graveyard_records(self) -> List[Dict[str, Any]]:
        """Returns all remediated records to display in the Halloween Graveyard."""
        runs = self.get_run_history(limit=100)
        return [r for r in runs if r.get("is_remediated") is True or r.get("status") in {"TOMBSTONE_READY", "SUCCEEDED"}]
