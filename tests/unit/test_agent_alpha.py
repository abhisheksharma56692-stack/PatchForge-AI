"""Unit tests for Agent Alpha (Security Test Synthesizer)."""
import pytest
from unittest.mock import MagicMock
from patchforge.agents.test_synthesizer import TestSynthesizerAgent
from patchforge.models.vulnerability import VulnerabilityReport
from patchforge.models.slicing import ASTContextSlice


def test_agent_alpha_synthesis():
    mock_llm = MagicMock()
    mock_llm.generate.return_value = (
        "Here is the reproduction test:\n"
        "```python\n"
        "import requests\n"
        "def test_sqli():\n"
        "    payload = \"' OR '1'='1\"\n"
        "    res = requests.get(f'http://localhost:5000/user?username={payload}')\n"
        "    assert len(res.json()['users']) > 1\n"
        "```"
    )

    agent = TestSynthesizerAgent(llm_client=mock_llm)
    vuln = VulnerabilityReport(
        finding_id="semgrep-cwe89-0",
        cwe_id="CWE-89",
        title="SQL Injection",
        description="Untrusted user input concatenated into SQL query",
        severity="HIGH",
        file_path="app.py",
        start_line=28,
        end_line=28,
        sink_symbol="cursor.execute(query)",
    )
    ast_slice = ASTContextSlice(
        slice_code="query = 'SELECT * FROM users WHERE username = ' + username\ncursor.execute(query)",
        start_line=26,
        end_line=28,
        language="python",
    )

    test_art = agent.synthesize(vuln, ast_slice)

    assert test_art.test_type == "reproduction_poc"
    assert test_art.target_cwe == "CWE-89"
    assert "def test_sqli():" in test_art.test_code
    assert "test_cwe_89_poc.py" in test_art.test_file_path
    mock_llm.generate.assert_called_once()

