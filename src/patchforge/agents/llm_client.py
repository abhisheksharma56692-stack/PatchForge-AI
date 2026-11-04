"""Unified LLM API wrapper supporting AWS Bedrock, Anthropic direct, and OpenAI."""
import os
import time
from typing import Optional, Dict, Any
from patchforge.agents.bedrock_client import BedrockLLMClient


class LLMClient:
    """
    Unified LLM Client providing seamless switching between AWS Bedrock,
    Anthropic direct API, and OpenAI-compatible providers with retries.
    """

    def __init__(
        self,
        provider: str = "bedrock",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        region_name: str = "us-east-1",
    ):
        self.provider = provider.lower()
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.region_name = region_name
        self.total_tokens_used = 0
        self.total_calls = 0

        if self.provider == "bedrock":
            self.model = model or BedrockLLMClient.DEFAULT_MODEL_ID
            self.bedrock = BedrockLLMClient(region_name=self.region_name, model_id=self.model)
        else:
            self.model = model or "claude-3-5-sonnet-20241022"
            self.bedrock = None

    def generate(
        self,
        system: str,
        user: str,
        temperature: float = 0.1,
    ) -> str:
        """Executes a single LLM completion."""
        self.total_calls += 1

        if self.provider == "bedrock":
            result = self.bedrock.generate(
                system_prompt=system,
                user_message=user,
                temperature=temperature,
            )
            self.total_tokens_used = self.bedrock.total_input_tokens + self.bedrock.total_output_tokens
            return result

        elif self.provider == "anthropic":
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=self.api_key)
                response = client.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    temperature=temperature,
                    system=system,
                    messages=[{"role": "user", "content": user}],
                )
                self.total_tokens_used += (response.usage.input_tokens + response.usage.output_tokens)
                return response.content[0].text
            except Exception as e:
                raise RuntimeError(f"Anthropic API call failed: {e}") from e

        elif self.provider == "openai":
            try:
                import openai
                client = openai.OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(
                    model=self.model,
                    temperature=temperature,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user},
                    ],
                )
                if response.usage:
                    self.total_tokens_used += response.usage.total_tokens
                return response.choices[0].message.content or ""
            except Exception as e:
                raise RuntimeError(f"OpenAI API call failed: {e}") from e

        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def generate_with_retry(
        self,
        system: str,
        user: str,
        temperature: float = 0.1,
        max_retries: int = 3,
        backoff_sec: float = 1.0,
    ) -> str:
        """Executes LLM call with exponential backoff on transient errors."""
        last_err = None
        for attempt in range(1, max_retries + 1):
            try:
                return self.generate(system, user, temperature=temperature)
            except Exception as e:
                last_err = e
                if attempt < max_retries:
                    time.sleep(backoff_sec * (2 ** (attempt - 1)))
        raise RuntimeError(f"LLM call failed after {max_retries} attempts: {last_err}") from last_err

