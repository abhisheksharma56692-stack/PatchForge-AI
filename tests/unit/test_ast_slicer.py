"""Unit tests for Tree-sitter AST, CFG, DDG, PDG and Backward Slicing."""
import pytest
from patchforge.slicing.parser import MultiLanguageParser
from patchforge.slicing.cfg_builder import CFGBuilder
from patchforge.slicing.ddg_builder import DDGBuilder
from patchforge.slicing.pdg import PDGBuilder
from patchforge.slicing.backward_slice import BackwardTaintSlicer

SAMPLE_PYTHON_CODE = """import os
import sqlite3

def query_user(user_id):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    if user_id > 0:
        query = "SELECT * FROM users WHERE id = " + str(user_id)
        cursor.execute(query)
    else:
        query = "SELECT * FROM users WHERE active = 1"
        cursor.execute(query)
    return cursor.fetchall()
"""


def test_python_function_parsing():
    parser = MultiLanguageParser("python")
    tree = parser.parse(SAMPLE_PYTHON_CODE)
    assert tree.root_node is not None
    assert tree.root_node.type == "module"

    body = parser.extract_function_body(tree, "query_user", SAMPLE_PYTHON_CODE)
    assert "def query_user" in body
    assert "cursor.execute(query)" in body


def test_cfg_if_else_branching():
    parser = MultiLanguageParser("python")
    tree = parser.parse(SAMPLE_PYTHON_CODE)
    builder = CFGBuilder()
    cfg = builder.build(tree.root_node, SAMPLE_PYTHON_CODE)

    assert len(cfg.nodes) > 0
    assert len(cfg.edges) > 0
    # CFG should contain if_statement node with branch edges
    if_nodes = [n for n, d in cfg.nodes(data=True) if d.get("node_type") == "if_statement"]
    assert len(if_nodes) >= 1
    # Check that branches emerge from if condition
    successors = list(cfg.successors(if_nodes[0]))
    assert len(successors) >= 1


def test_ddg_variable_def_use_chain():
    parser = MultiLanguageParser("python")
    tree = parser.parse(SAMPLE_PYTHON_CODE)
    ddg_builder = DDGBuilder()
    ddg = ddg_builder.build(tree.root_node, SAMPLE_PYTHON_CODE)

    assert len(ddg.nodes) > 0
    # Find edges with variable 'query'
    query_edges = [
        (u, v, d) for u, v, d in ddg.edges(data=True) if d.get("variable") == "query"
    ]
    assert len(query_edges) >= 1


def test_pdg_merges_cfg_and_ddg():
    parser = MultiLanguageParser("python")
    tree = parser.parse(SAMPLE_PYTHON_CODE)
    cfg = CFGBuilder().build(tree.root_node, SAMPLE_PYTHON_CODE)
    ddg = DDGBuilder().build(tree.root_node, SAMPLE_PYTHON_CODE)
    pdg = PDGBuilder().build(cfg, ddg)

    # Should have both control and data edge types
    edge_types = {d.get("edge_type") for _, _, d in pdg.edges(data=True)}
    assert "data_dependence" in edge_types or "data" in edge_types
    assert "control" in edge_types or "control_flow" in edge_types


def test_backward_slice_extracts_minimal_context():
    slicer = BackwardTaintSlicer("python")
    slice_result = slicer.slice_from_location(
        SAMPLE_PYTHON_CODE, line=9, sink_symbol="cursor.execute(query)"
    )

    assert slice_result is not None
    assert "cursor.execute(query)" in slice_result.slice_code
    assert "query =" in slice_result.slice_code
    # Sliced lines should be fewer than total
    total_lines = len(SAMPLE_PYTHON_CODE.splitlines())
    assert len(slice_result.sliced_lines) < total_lines


def test_slice_preserves_import_statements():
    slicer = BackwardTaintSlicer("python")
    slice_result = slicer.slice_from_location(
        SAMPLE_PYTHON_CODE, line=9, sink_symbol="cursor.execute(query)"
    )

    assert "import sqlite3" in slice_result.slice_code
    assert len(slice_result.imported_symbols) >= 1


def test_1000_line_file_reduces_to_under_60_lines():
    # Generate 1000-line synthetic python program with bloat
    bloat_lines = [f"def filler_fn_{i}():\n    x = {i}\n    return x * 2\n" for i in range(250)]
    vuln_func = (
        "def target_func(payload):\n"
        "    sanitized = str(payload)\n"
        "    sink = 'EXECUTE ' + sanitized\n"
        "    run_sink(sink)\n"
    )
    large_code = "import sys\n\n" + "\n".join(bloat_lines) + "\n" + vuln_func
    assert len(large_code.splitlines()) > 800

    slicer = BackwardTaintSlicer("python")
    sink_line = len(large_code.splitlines()) - 1
    slice_result = slicer.slice_from_location(large_code, line=sink_line, sink_symbol="run_sink(sink)")

    sliced_line_count = len(slice_result.slice_code.splitlines())
    assert sliced_line_count < 60
    assert "run_sink(sink)" in slice_result.slice_code

