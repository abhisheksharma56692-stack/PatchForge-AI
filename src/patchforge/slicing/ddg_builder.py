"""Data Dependence Graph (DDG) and Def-Use chain builder."""
import re
from typing import Set, Dict, List, Any
import networkx as nx
from tree_sitter import Node


class DDGBuilder:
    """
    Constructs a Data Dependence Graph (DDG) linking definition and use
    sites of variables across AST statements.
    """

    STATEMENT_TYPES = {
        "expression_statement",
        "assignment",
        "augmented_assignment",
        "return_statement",
        "if_statement",
        "for_statement",
        "while_statement",
        "variable_declaration",
        "lexical_declaration",
    }

    def __init__(self):
        self._next_id = 1

    def get_definitions(self, node: Node, code: str) -> Set[str]:
        """Extracts variable names defined/assigned by this statement node."""
        defs = set()

        if node.type in {"assignment", "augmented_assignment"}:
            # Left side is defined
            left = node.child_by_field_name("left")
            if left:
                defs.update(self._extract_identifiers(left, code))
            elif node.children:
                # First child or before '='
                defs.update(self._extract_identifiers(node.children[0], code))
        elif node.type in {"for_statement"}:
            # Loop var
            left = node.child_by_field_name("left")
            if left:
                defs.update(self._extract_identifiers(left, code))
        elif node.type in {"variable_declarator"}:
            name = node.child_by_field_name("name")
            if name:
                defs.update(self._extract_identifiers(name, code))
        else:
            # Check for assignments inside expression statement
            for child in node.children:
                if child.type in {"assignment", "augmented_assignment", "variable_declarator"}:
                    defs.update(self.get_definitions(child, code))

        return defs

    def get_uses(self, node: Node, code: str) -> Set[str]:
        """Extracts variable names read/used by this statement node."""
        all_ids = self._extract_identifiers(node, code)
        defs = self.get_definitions(node, code)
        # Uses are identifiers in the statement that are not being defined on the LHS
        return all_ids - defs

    def _extract_identifiers(self, node: Node, code: str) -> Set[str]:
        """Collects all identifier names under a node."""
        ids = set()
        if node.type in {"identifier", "property_identifier"}:
            name = code[node.start_byte:node.end_byte].strip()
            # Exclude keywords and builtins
            if name and not name.startswith("__") and name not in {"self", "cls", "None", "True", "False"}:
                ids.add(name)
        for child in node.children:
            ids.update(self._extract_identifiers(child, code))
        return ids

    def build(self, root_node: Node, code: str) -> nx.DiGraph:
        """Builds a DDG with Def-Use edges between statements."""
        ddg = nx.DiGraph()
        self._next_id = 1

        # Flatten statements in source order
        stmts: List[Dict[str, Any]] = []

        def collect_statements(curr: Node):
            if curr.type in self.STATEMENT_TYPES:
                nid = self._next_id
                self._next_id += 1
                snippet = code[curr.start_byte:curr.end_byte].strip()
                defs = self.get_definitions(curr, code)
                uses = self.get_uses(curr, code)
                
                stmt_info = {
                    "node_id": nid,
                    "ast_node": curr,
                    "text": snippet,
                    "start_line": curr.start_point[0] + 1,
                    "end_line": curr.end_point[0] + 1,
                    "defs": defs,
                    "uses": uses,
                }
                stmts.append(stmt_info)
                ddg.add_node(
                    nid,
                    node_id=nid,
                    node_type=curr.type,
                    text=snippet,
                    start_line=stmt_info["start_line"],
                    end_line=stmt_info["end_line"],
                    variables_defined=list(defs),
                    variables_used=list(uses),
                    ast_node=curr,
                )
            
            # Recurse into children
            for child in curr.children:
                collect_statements(child)

        collect_statements(root_node)

        # Connect Def -> Use edges
        # For each statement that uses var 'x', link from the most recent preceding statement that defines 'x'
        active_defs: Dict[str, int] = {}
        for s in stmts:
            sid = s["node_id"]
            for u in s["uses"]:
                if u in active_defs:
                    def_node_id = active_defs[u]
                    ddg.add_edge(def_node_id, sid, edge_type="data_dependence", variable=u)
            for d in s["defs"]:
                active_defs[d] = sid

        return ddg

