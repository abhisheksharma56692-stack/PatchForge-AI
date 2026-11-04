"""Agent Alpha: Red-Team Security Test Synthesizer."""
import re
from typing import Optional
from patchforge.models.vulnerability import VulnerabilityReport
from patchforge.models.slicing import ASTContextSlice
from patchforge.models.agents import TestArtifact
from patchforge.agents.prompts import AGENT_ALPHA_SYSTEM_PROMPT, AGENT_ALPHA_USER_TEMPLATE
from patchforge.agents.llm_client import LLMClient


class TestSynthesizerAgent:
    """
    Agent Alpha (Red Team): Analyzes vulnerability finding and slice context
    to generate an executable Proof-of-Concept security reproduction test.
    """
    __test__ = False

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def synthesize(self, vuln: VulnerabilityReport, slice_context: ASTContextSlice) -> TestArtifact:
        """Generates a standalone reproduction test."""
        user_prompt = AGENT_ALPHA_USER_TEMPLATE.format(
            finding_id=vuln.finding_id,
            cwe_id=vuln.cwe_id,
            file_path=vuln.file_path,
            start_line=vuln.start_line,
            end_line=vuln.end_line,
            sink_symbol=vuln.sink_symbol or "sink",
            slice_code=slice_context.slice_code,
        )

        raw_response = self.llm.generate(
            system=AGENT_ALPHA_SYSTEM_PROMPT,
            user=user_prompt,
            temperature=0.2,
        )

        test_code = self._extract_code(raw_response)
        ext = "js" if slice_context.language in {"javascript", "js", "typescript", "ts"} else "py"
        test_file_path = f"tests/reproduction/test_{vuln.cwe_id.lower().replace('-', '_')}_poc.{ext}"

        return TestArtifact(
            test_file_path=test_file_path,
            test_code=test_code,
            test_type="reproduction_poc",
            target_cwe=vuln.cwe_id,
            execution_command="pytest" if ext == "py" else "npm test",
        )

    def _extract_code(self, response_text: str) -> str:
        """Strips markdown code blocks if present."""
        code_blocks = re.findall(r"```(?:\w+)?\n(.*?)```", response_text, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        return response_text.strip()
