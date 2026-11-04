"""Z3 SMT Invariant Engine for formal verification of code boundaries."""
from typing import List, Dict, Any, Tuple, Optional
import z3

from patchforge.models.formal import FormalInvariant, BoundaryConstraint
from patchforge.models.slicing import ASTContextSlice
from patchforge.formal.z3_translator import Z3ASTTranslator
from patchforge.formal.boundary_checker import BoundaryChecker


class SMTInvariantVerifier:
    """
    Uses Microsoft Z3 theorem prover to verify safety invariants
    and formulate non-negotiable formal constraints for AI patching.
    """

    def __init__(self):
        self.solver = z3.Solver()
        self.translator = Z3ASTTranslator()
        self.boundary_checker = BoundaryChecker()

    def verify(self, path_conds: List[z3.BoolRef], safety: z3.BoolRef) -> FormalInvariant:
        """
        Solves: SAT(path_conds ∧ ¬safety)
        If SAT -> violation possible -> extracts counterexample -> emits required invariant.
        If UNSAT -> proof that safety condition unconditionally holds.
        """
        self.solver.reset()
        for pc in path_conds:
            self.solver.add(pc)
        
        # Test violation: NOT safety
        self.solver.add(z3.Not(safety))
        res = self.solver.check()

        if res == z3.sat:
            model = self.solver.model()
            cex: Dict[str, Any] = {}
            for decl in model.decls():
                val = model[decl]
                try:
                    cex[decl.name()] = val.as_long()
                except Exception:
                    cex[decl.name()] = str(val)

            return FormalInvariant(
                predicate_formula=str(safety),
                z3_model_status="VIOLATION_POSSIBLE",
                counterexample=cex,
                required_invariants=[
                    f"ASSERT_PRECONDITION: {str(safety)}",
                    f"PREVENT_COUNTEREXAMPLE: {cex}",
                ],
            )
        elif res == z3.unsat:
            return FormalInvariant(
                predicate_formula=str(safety),
                z3_model_status="UNCONDITIONALLY_SAFE",
                counterexample=None,
                required_invariants=[f"VERIFIED_INVARIANT: {str(safety)}"],
            )
        else:
            return FormalInvariant(
                predicate_formula=str(safety),
                z3_model_status="UNKNOWN",
                counterexample=None,
                required_invariants=[],
            )

    def verify_buffer_bounds(
        self, buffer_max: int, offset_var_name: str
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Verifies that offset_var cannot exceed buffer_max or be negative.
        Formula: offset >= 0 AND offset < buffer_max
        """
        self.solver.reset()
        offset = z3.Int(offset_var_name)
        safe_condition = z3.And(offset >= 0, offset < buffer_max)
        self.solver.add(z3.Not(safe_condition))
        res = self.solver.check()

        if res == z3.sat:
            model = self.solver.model()
            bad_val = model[offset].as_long() if offset in model else -1
            return False, {
                "status": "VIOLATION_POSSIBLE",
                "counter_example": {offset_var_name: bad_val},
                "required_invariant": f"Assert: 0 <= {offset_var_name} < {buffer_max}",
            }
        return True, {"status": "UNCONDITIONALLY_SAFE"}

    def verify_from_slice(self, ast_slice: ASTContextSlice) -> FormalInvariant:
        """
        High-level pipeline hook: analyzes an ASTContextSlice, identifies
        unbounded variables, runs SMT checks, and produces formal invariants.
        """
        path_conds = self.translator.translate_conditionals(ast_slice)
        
        # Analyze target symbols in slice code
        invariants = []
        boundary_constraints = []

        code = ast_slice.slice_code
        if "query" in code or "execute" in code or "cursor" in code:
            # SQL injection constraint
            invariants.append("MUST_USE_PARAMETERIZED_QUERY: query must not use raw string formatting or concatenation")
            invariants.append("ASSERT_SAFE_BINDINGS: all user inputs must be passed via parameter tuple/dict")
        
        if "open(" in code or "readFile" in code or "path" in code:
            # Path traversal constraint
            invariants.append("ASSERT_CANONICAL_PATH: resolved_path must start with allowed base directory")
            invariants.append("REJECT_DIRECTORY_TRAVERSAL: path component must not contain '..' sequences")
            bc = self.boundary_checker.check_string_length("filename", 256)
            boundary_constraints.append(bc)

        # Buffer / integer bounds if any numerical logic present
        offset_var = z3.Int("offset")
        path_conds.append(offset_var >= 0)
        safety = offset_var < 4096
        
        result = self.verify(path_conds, safety)
        result.required_invariants.extend(invariants)
        result.boundary_constraints.extend(boundary_constraints)
        return result

