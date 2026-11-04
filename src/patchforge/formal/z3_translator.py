"""Translates AST conditions, array bounds, and string constraints into Z3 expressions."""
import re
from typing import List, Optional
import z3

from patchforge.models.slicing import ASTContextSlice


class Z3ASTTranslator:
    """
    Translates programming language conditions and constraints into
    Z3 First-Order Logic (FOL) BoolRef expressions.
    """

    def __init__(self):
        self._vars = {}

    def get_int_var(self, name: str) -> z3.ArithRef:
        if name not in self._vars:
            self._vars[name] = z3.Int(name)
        return self._vars[name]

    def translate_conditionals(self, ast_slice: ASTContextSlice) -> List[z3.BoolRef]:
        """Extracts simple conditional logic from the slice code and converts to Z3 BoolRefs."""
        z3_conds: List[z3.BoolRef] = []
        lines = ast_slice.slice_code.splitlines()

        for line in lines:
            line_str = line.strip()
            # Match if condition: e.g. "if user_id > 0:" or "if offset < max_len:"
            match = re.search(r"if\s+([a-zA-Z_]\w*)\s*(>|<|>=|<=|==|!=)\s*(\d+|[a-zA-Z_]\w*)", line_str)
            if match:
                var_name, op, rhs = match.groups()
                lhs_z3 = self.get_int_var(var_name)
                rhs_z3 = int(rhs) if rhs.isdigit() else self.get_int_var(rhs)

                if op == ">":
                    z3_conds.append(lhs_z3 > rhs_z3)
                elif op == "<":
                    z3_conds.append(lhs_z3 < rhs_z3)
                elif op == ">=":
                    z3_conds.append(lhs_z3 >= rhs_z3)
                elif op == "<=":
                    z3_conds.append(lhs_z3 <= rhs_z3)
                elif op == "==":
                    z3_conds.append(lhs_z3 == rhs_z3)
                elif op == "!=":
                    z3_conds.append(lhs_z3 != rhs_z3)

        return z3_conds

    def translate_array_access(self, index_expr: str, array_len: str) -> z3.BoolRef:
        """
        Translates array index bounds check into Z3:
        0 <= index < array_len
        """
        idx = int(index_expr) if index_expr.isdigit() else self.get_int_var(index_expr)
        alen = int(array_len) if array_len.isdigit() else self.get_int_var(array_len)
        return z3.And(idx >= 0, idx < alen)

    def translate_string_length(self, var: str, max_len: int) -> z3.BoolRef:
        """
        Translates string length constraint into Z3:
        0 <= len(var) <= max_len
        """
        str_len_var = self.get_int_var(f"len_{var}")
        return z3.And(str_len_var >= 0, str_len_var <= max_len)

