"""Unit tests for AWS Bedrock LLM client (boto3 mocked)."""
import io
import json
import pytest
from unittest.mock import MagicMock
from botocore.exceptions import ClientError
from patchforge.agents.bedrock_client import BedrockLLMClient


def test_bedrock_client_initialization():
    mock_boto = MagicMock()
    client = BedrockLLMClient(
        region_name="us-west-2",
        model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
        bedrock_runtime_client=mock_boto,
    )
    assert client.region_name == "us-west-2"
    assert client.model_id == "anthropic.claude-3-5-sonnet-20240620-v1:0"
    assert client.call_count == 0


def test_bedrock_generate_success():
    mock_boto = MagicMock()
    
    # Mock response body
    bedrock_response_payload = {
        "id": "msg_01234",
        "type": "message",
        "role": "assistant",
        "content": [
            {"type": "text", "text": "```python\ndef patch(): pass\n```"}
        ],
        "usage": {
            "input_tokens": 120,
            "output_tokens": 45,
        }
    }
    
    response_bytes = json.dumps(bedrock_response_payload).encode("utf-8")
    mock_body = io.BytesIO(response_bytes)
    mock_boto.invoke_model.return_value = {"body": mock_body}

    client = BedrockLLMClient(bedrock_runtime_client=mock_boto)
    result = client.generate(
        system_prompt="You are a patch synthesizer.",
        user_message="Fix SQL injection.",
        temperature=0.1,
    )

    assert "def patch():" in result
    assert client.total_input_tokens == 120
    assert client.total_output_tokens == 45
    assert client.call_count == 1
    assert client.total_latency_ms > 0

    # Verify invoke_model parameters
    mock_boto.invoke_model.assert_called_once()
    _, kwargs = mock_boto.invoke_model.call_args
    assert kwargs["modelId"] == BedrockLLMClient.DEFAULT_MODEL_ID
    assert kwargs["contentType"] == "application/json"
    
    sent_body = json.loads(kwargs["body"].decode("utf-8"))
    assert sent_body["anthropic_version"] == "bedrock-2023-05-31"
    assert sent_body["system"] == "You are a patch synthesizer."
    assert sent_body["messages"][0]["content"] == "Fix SQL injection."


def test_bedrock_client_error_handling():
    mock_boto = MagicMock()
    mock_boto.invoke_model.side_effect = ClientError(
        error_response={"Error": {"Code": "AccessDeniedException", "Message": "Not authorized"}},
        operation_name="InvokeModel",
    )

    client = BedrockLLMClient(bedrock_runtime_client=mock_boto)
    with pytest.raises(RuntimeError, match="AWS Bedrock invocation error"):
        client.generate("sys", "user")

