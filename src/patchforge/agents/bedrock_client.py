"""AWS Bedrock runtime client for managed LLM inference."""
import json
import time
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError


class BedrockLLMClient:
    """
    AWS Bedrock inference wrapper invoking Anthropic Claude models
    via the bedrock-runtime InvokeModel API.
    """

    DEFAULT_MODEL_ID = "anthropic.claude-3-5-sonnet-20240620-v1:0"

    def __init__(
        self,
        region_name: str = "us-east-1",
        model_id: str = DEFAULT_MODEL_ID,
        bedrock_runtime_client: Optional[Any] = None,
    ):
        self.region_name = region_name
        self.model_id = model_id
        if bedrock_runtime_client:
            self.client = bedrock_runtime_client
        else:
            try:
                self.client = boto3.client("bedrock-runtime", region_name=self.region_name)
            except Exception:
                self.client = None

        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_latency_ms = 0.0
        self.call_count = 0

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> str:
        """
        Invokes Claude model on AWS Bedrock using the Bedrock Messages API format.
        """
        if self.client is None:
            raise RuntimeError("Bedrock client not initialized. Check AWS credentials.")

        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [
                {"role": "user", "content": user_message}
            ],
        }

        body_bytes = json.dumps(payload).encode("utf-8")
        start_time = time.time()

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=body_bytes,
                contentType="application/json",
                accept="application/json",
            )
        except ClientError as e:
            raise RuntimeError(f"AWS Bedrock invocation error: {e}") from e

        duration_ms = (time.time() - start_time) * 1000
        self.total_latency_ms += duration_ms
        self.call_count += 1

        response_body = json.loads(response["body"].read().decode("utf-8"))
        
        # Token metrics tracking
        usage = response_body.get("usage", {})
        self.total_input_tokens += usage.get("input_tokens", 0)
        self.total_output_tokens += usage.get("output_tokens", 0)

        # Extract output text
        content = response_body.get("content", [])
        if content and "text" in content[0]:
            return content[0]["text"]
        return ""

