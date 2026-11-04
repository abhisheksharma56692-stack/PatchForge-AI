"""Mock Z3 SMT Formal Invariant Engine stub for Member 2 development."""
from patchforge.models.formal import FormalInvariant, BoundaryConstraint
from patchforge.models.slicing import ASTContextSlice


class SMTInvariantVerifier:
    """Mock Z3 engine returning formal invariant constraints."""

    def verify_from_slice(self, ast_slice: ASTContextSlice) -> FormalInvariant:
        return FormalInvariant(
            predicate_formula="And(offset >= 0, offset < 4096)",
            z3_model_status="VIOLATION_POSSIBLE",
            counterexample={"offset": 4096},
            required_invariants=[
                "MUST_USE_PARAMETERIZED_QUERY: query must not use raw string formatting or concatenation",
                "ASSERT_SAFE_BINDINGS: all user inputs must be passed via parameter tuple/dict",
            ],
            boundary_constraints=[
                BoundaryConstraint(
                    variable_name="username",
                    constraint_type="STRING_LENGTH",
                    lower_bound=0,
                    upper_bound=255,
                    z3_expression="0 <= len(username) <= 255",
                )
            ],
        )

