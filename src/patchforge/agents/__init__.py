"""AI Agent Logic and LLM Orchestration Subsystem."""
from patchforge.agents.prompts import (
    AGENT_ALPHA_SYSTEM_PROMPT,
    AGENT_ALPHA_USER_TEMPLATE,
    AGENT_BETA_SYSTEM_PROMPT,
    AGENT_BETA_USER_TEMPLATE,
    AGENT_GAMMA_SYSTEM_PROMPT,
    REFLECTION_CRITIQUE_TEMPLATE,
)
from patchforge.agents.llm_client import LLMClient
from patchforge.agents.bedrock_client import BedrockLLMClient
from patchforge.agents.test_synthesizer import TestSynthesizerAgent
from patchforge.agents.patch_synthesizer import PatchSynthesizerAgent
from patchforge.agents.auditor import AntiTamperAuditor
from patchforge.agents.reflection import ReflectionEngine

__all__ = [
    "AGENT_ALPHA_SYSTEM_PROMPT",
    "AGENT_ALPHA_USER_TEMPLATE",
    "AGENT_BETA_SYSTEM_PROMPT",
    "AGENT_BETA_USER_TEMPLATE",
    "AGENT_GAMMA_SYSTEM_PROMPT",
    "REFLECTION_CRITIQUE_TEMPLATE",
    "LLMClient",
    "BedrockLLMClient",
    "TestSynthesizerAgent",
    "PatchSynthesizerAgent",
    "AntiTamperAuditor",
    "ReflectionEngine",
]

