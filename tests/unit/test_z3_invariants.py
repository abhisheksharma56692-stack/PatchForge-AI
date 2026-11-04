"""Unit tests for Z3 SMT Formal Invariant Engine."""
import z3
import pytest
from patchforge.formal.z3_translator import Z3ASTTranslator
from patchforge.formal.invariant_engine import SMTInvariantVerifier
from patchforge.formal.boundary_checker import BoundaryChecker
from patchforge.models.slicing import ASTContextSlice


def test_z3_translator_conditionals():
    translator = Z3ASTTranslator()
    ast_slice = ASTContextSlice(
        slice_code="if user_id > 0:\n    execute(user_id)",
        start_line=1,
        end_line=2,
        language="python",
    )
    conds = translator.translate_conditionals(ast_slice)
    assert len(conds) == 1
    assert str(conds[0]) == "user_id > 0"


def test_z3_translator_array_access():
    translator = Z3ASTTranslator()
    expr = translator.translate_array_access("idx", "10")
    assert isinstance(expr, z3.BoolRef)


def test_z3_translator_string_length():
    translator = Z3ASTTranslator()
    expr = translator.translate_string_length("username", 255)
    assert isinstance(expr, z3.BoolRef)


def test_invariant_verifier_violation_found():
    verifier = SMTInvariantVerifier()
    x = z3.Int("x")
    # Path cond: x >= 0
    # Safety: x < 5
    # Since x can be >= 5, violation is possible!
    inv = verifier.verify([x >= 0], x < 5)
    assert inv.z3_model_status == "VIOLATION_POSSIBLE"
    assert inv.counterexample is not None
    assert inv.counterexample.get("x", 0) >= 5


def test_invariant_verifier_unconditionally_safe():
    verifier = SMTInvariantVerifier()
    x = z3.Int("x")
    # Path cond: x > 0 and x < 4
    # Safety: x < 5
    # Negation is UNSAT -> Unconditionally safe
    inv = verifier.verify([x > 0, x < 4], x < 5)
    assert inv.z3_model_status == "UNCONDITIONALLY_SAFE"
    assert inv.counterexample is None


def test_verify_buffer_bounds():
    verifier = SMTInvariantVerifier()
    safe, details = verifier.verify_buffer_bounds(buffer_max=1024, offset_var_name="idx")
    assert not safe
    assert details["status"] == "VIOLATION_POSSIBLE"
    assert "idx" in details["counter_example"]


def test_boundary_checker():
    checker = BoundaryChecker()
    int_c = checker.check_integer_overflow("count", 32)
    assert int_c.constraint_type == "INTEGER_BOUNDS"
    assert int_c.lower_bound == -2147483648
    assert int_c.upper_bound == 2147483647

    arr_c = checker.check_array_bounds("arr_idx", 50)
    assert arr_c.constraint_type == "ARRAY_INDEX"
    assert arr_c.lower_bound == 0
    assert arr_c.upper_bound == 49

    str_c = checker.check_string_length("payload", 4096)
    assert str_c.constraint_type == "STRING_LENGTH"
    assert str_c.upper_bound == 4096


def test_verify_from_slice():
    verifier = SMTInvariantVerifier()
    ast_slice = ASTContextSlice(
        slice_code="query = 'SELECT * FROM users WHERE id = ' + uid\ncursor.execute(query)",
        start_line=1,
        end_line=2,
        language="python",
    )
    res = verifier.verify_from_slice(ast_slice)
    assert res is not None
    assert any("PARAMETERIZED" in r for r in res.required_invariants)

