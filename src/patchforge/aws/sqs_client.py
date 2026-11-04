"""Amazon SQS client for asynchronous vulnerability event ingestion."""
import json
import boto3
from typing import List, Dict, Any, Optional
from patchforge.config import settings


class SQSVulnerabilityQueue:
    """Consumes and produces vulnerability ingestion events via Amazon SQS."""

    def __init__(
        self,
        queue_url: Optional[str] = None,
        region_name: Optional[str] = None,
        sqs_client: Optional[Any] = None,
    ):
        self.queue_url = queue_url or settings.sqs_queue_url or "https://sqs.us-east-1.amazonaws.com/123456789012/patchforge-vuln-queue"
        self.region = region_name or settings.aws_region
        self.client = sqs_client or boto3.client("sqs", region_name=self.region)

    def send_vulnerability_event(self, event_data: Dict[str, Any]) -> str:
        """Publishes a vulnerability event payload to the queue."""
        response = self.client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(event_data),
        )
        return response.get("MessageId", "")

    def poll_vulnerability_events(
        self, max_messages: int = 5, wait_time_sec: int = 1
    ) -> List[Dict[str, Any]]:
        """Polls SQS queue for incoming vulnerability events."""
        try:
            response = self.client.receive_message(
                QueueUrl=self.queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time_sec,
            )
            messages = response.get("Messages", [])
            events = []
            for msg in messages:
                body = json.loads(msg.get("Body", "{}"))
                events.append({
                    "message_id": msg.get("MessageId"),
                    "receipt_handle": msg.get("ReceiptHandle"),
                    "data": body,
                })
            return events
        except Exception:
            return []

    def delete_event(self, receipt_handle: str) -> None:
        """Deletes processed message from SQS."""
        self.client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=receipt_handle,
        )

