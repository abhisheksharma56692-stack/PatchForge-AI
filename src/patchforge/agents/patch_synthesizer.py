"""Agent Beta: Blue-Team Patch Synthesizer."""
import re
from typing import Optional
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.formal import FormalInvariant
from patchforge.models.agents import TestArtifact, PatchCandidate, ReflectionFeedback
from patchforge.agents.prompts import (
    AGENT_BETA_SYSTEM_PROMPT,
    AGENT_BETA_USER_TEMPLATE,
    REFLECTION_CRITIQUE_TEMPLATE,
)
from patchforge.agents.llm_client import LLMClient


class PatchSynthesizerAgent:
    """
    Agent Beta (Blue Team): Synthesizes surgical, minimal Git unified diffs
    that eliminate vulnerabilities and adhere strictly to Z3 formal invariants.
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def synthesize(
        self,
        slice_context: ASTContextSlice,
        invariants: FormalInvariant,
        poc_test: TestArtifact,
        feedback: Optional[ReflectionFeedback] = None,
    ) -> PatchCandidate:
        """Synthesizes a candidate unified diff."""
        # Format invariants string
        inv_strings = "\n".join(f"- {inv}" for inv in invariants.required_invariants)
        if not inv_strings:
            inv_strings = "- Must ensure all inputs are sanitized and bounds are enforced."

        # Format reflection critique if present
        critique_section = ""
        if feedback:
            critique_section = REFLECTION_CRITIQUE_TEMPLATE.format(
                iteration=feedback.iteration,
                exit_code=1,
                stderr=feedback.stack_trace_snippet or "Test failure",
                failure_summary=feedback.failure_summary + "\n" + feedback.actionable_critique,
            )

        user_prompt = AGENT_BETA_USER_TEMPLATE.format(
            file_path="target_file",
            cwe_id=poc_test.target_cwe or "Vulnerability",
            slice_code=slice_context.slice_code,
            formal_invariants=inv_strings,
            reproduction_test_code=poc_test.test_code,
            reflection_critique_section=critique_section,
        )

        raw_response = self.llm.generate(
            system=AGENT_BETA_SYSTEM_PROMPT,
            user=user_prompt,
            temperature=0.1,
        )

        diff = self._extract_diff(raw_response)
        tombstone = self._extract_tombstone(raw_response, poc_test.target_cwe)

        model_val = getattr(self.llm, "model", "claude-3-5-sonnet")
        model_name = model_val if isinstance(model_val, str) else "claude-3-5-sonnet"

        return PatchCandidate(
            diff_content=diff,
            target_file="target_file",
            explanation="Synthesized remediation patch satisfying formal Z3 invariants.",
            tombstone_inscription=tombstone,
            model_name=model_name,
        )

    def _extract_diff(self, response_text: str) -> str:
        """Extracts unified diff content from LLM response."""
        diff_match = re.search(r"```(?:diff)?\n(---.*?\n\+\+\+.*?\n@@.*?)```", response_text, re.DOTALL)
        if diff_match:
            return diff_match.group(1).strip()
        
        # If no markdown block, search for raw unified diff headers
        raw_match = re.search(r"(--- a/.*?\n\+\+\+ b/.*?\n@@.*)", response_text, re.DOTALL)
        if raw_match:
            return raw_match.group(1).strip()

        return response_text.strip()

    def _extract_tombstone(self, response_text: str, cwe_id: str) -> str:
        """Extracts tombstone inscription or provides Halloween default."""
        match = re.search(r"(⚰️.*)", response_text)
        if match:
            return match.group(1).strip()
        return f"⚰️ R.I.P. {cwe_id} — Neutralized by PatchForge AI"
