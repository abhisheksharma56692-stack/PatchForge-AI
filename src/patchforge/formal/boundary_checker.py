"""Boundary checker for integer bounds, array bounds, and string length limits."""
from typing import Optional, List
import z3

from patchforge.models.formal import BoundaryConstraint


class BoundaryChecker:
    """Specialized SMT prover for bounds safety checks."""

    def __init__(self):
        self.solver = z3.Solver()

    def check_integer_overflow(self, var: str, bit_width: int = 32) -> BoundaryConstraint:
        """
        Generates boundary constraint for integer overflow:
        -(2^(bit_width-1)) <= var <= 2^(bit_width-1) - 1
        """
        min_val = -(2 ** (bit_width - 1))
        max_val = (2 ** (bit_width - 1)) - 1
        expr = f"{min_val} <= {var} <= {max_val}"

        return BoundaryConstraint(
            variable_name=var,
            constraint_type="INTEGER_BOUNDS",
            lower_bound=min_val,
            upper_bound=max_val,
            z3_expression=expr,
        )

    def check_array_bounds(self, index_var: str, array_size: int) -> BoundaryConstraint:
        """
        Generates boundary constraint for array indexing:
        0 <= index_var < array_size
        """
        expr = f"0 <= {index_var} < {array_size}"
        return BoundaryConstraint(
            variable_name=index_var,
            constraint_type="ARRAY_INDEX",
            lower_bound=0,
            upper_bound=array_size - 1,
            z3_expression=expr,
        )

    def check_string_length(self, str_var: str, max_len: int = 4096) -> BoundaryConstraint:
        """
        Generates boundary constraint for string input lengths:
        0 <= len(str_var) <= max_len
        """
        expr = f"0 <= len({str_var}) <= {max_len}"
        return BoundaryConstraint(
            variable_name=str_var,
            constraint_type="STRING_LENGTH",
            lower_bound=0,
            upper_bound=max_len,
            z3_expression=expr,
        )

