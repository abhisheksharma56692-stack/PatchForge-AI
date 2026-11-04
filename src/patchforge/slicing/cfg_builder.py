"""Control Flow Graph (CFG) builder for AST."""
from typing import List, Dict, Any, Optional, Tuple
import networkx as nx
from tree_sitter import Node


class CFGBuilder:
    """
    Constructs a directed Control Flow Graph (CFG) where nodes are statements
    and edges represent possible execution paths (branches, loops, sequential).
    """

    STATEMENT_TYPES = {
        "expression_statement",
        "assignment",
        "augmented_assignment",
        "return_statement",
        "if_statement",
        "for_statement",
        "while_statement",
        "try_statement",
        "with_statement",
        "raise_statement",
        "pass_statement",
        "break_statement",
        "continue_statement",
        "variable_declaration",
        "lexical_declaration",
    }

    def __init__(self):
        self._next_id = 1

    def build(self, root_node: Node, code: str) -> nx.DiGraph:
        """Builds a CFG DiGraph from an AST root node."""
        cfg = nx.DiGraph()
        self._next_id = 1

        # Collect statements in a structured manner
        entry_id = 0
        cfg.add_node(entry_id, node_type="ENTRY", text="ENTRY", start_line=0, end_line=0)

        # Recursively build flow for blocks
        last_nodes = self._build_subgraph(cfg, root_node, code, [entry_id])

        exit_id = self._next_id
        self._next_id += 1
        cfg.add_node(exit_id, node_type="EXIT", text="EXIT", start_line=999999, end_line=999999)

        for src in last_nodes:
            cfg.add_edge(src, exit_id, edge_type="control_flow")

        return cfg

    def _build_subgraph(
        self,
        cfg: nx.DiGraph,
        ast_node: Node,
        code: str,
        incoming: List[int],
    ) -> List[int]:
        """Processes an AST node and returns list of exit node IDs from this node/block."""
        current_incoming = list(incoming)

        # Iterate over direct statement-like children if this is a container/block
        children = self._get_statement_children(ast_node)
        if not children and ast_node.type in self.STATEMENT_TYPES:
            children = [ast_node]

        for child in children:
            if child.type == "if_statement":
                current_incoming = self._handle_if(cfg, child, code, current_incoming)
            elif child.type in {"while_statement", "for_statement"}:
                current_incoming = self._handle_loop(cfg, child, code, current_incoming)
            elif child.type == "try_statement":
                current_incoming = self._handle_try(cfg, child, code, current_incoming)
            elif child.type in self.STATEMENT_TYPES:
                node_id = self._add_statement_node(cfg, child, code)
                for src in current_incoming:
                    cfg.add_edge(src, node_id, edge_type="control_flow")
                
                if child.type in {"return_statement", "raise_statement"}:
                    current_incoming = []
                else:
                    current_incoming = [node_id]
            else:
                # Recurse for nested wrappers (e.g. block, function_definition)
                current_incoming = self._build_subgraph(cfg, child, code, current_incoming)

        return current_incoming

    def _get_statement_children(self, node: Node) -> List[Node]:
        """Extracts child nodes that correspond to statements or compound blocks."""
        stmts = []
        for c in node.children:
            if c.type in self.STATEMENT_TYPES or c.type in {
                "block", "suite", "statement_block", "compound_statement",
                "function_definition", "function_declaration"
            }:
                stmts.append(c)
        return stmts

    def _add_statement_node(self, cfg: nx.DiGraph, ast_node: Node, code: str) -> int:
        nid = self._next_id
        self._next_id += 1
        snippet = code[ast_node.start_byte:ast_node.end_byte].strip()
        # 1-based line indexing
        start_line = ast_node.start_point[0] + 1
        end_line = ast_node.end_point[0] + 1

        cfg.add_node(
            nid,
            node_id=nid,
            node_type=ast_node.type,
            text=snippet,
            start_line=start_line,
            end_line=end_line,
            ast_node=ast_node,
        )
        return nid

    def _handle_if(
        self, cfg: nx.DiGraph, if_node: Node, code: str, incoming: List[int]
    ) -> List[int]:
        """Builds CFG branches for if / else blocks."""
        condition_id = self._add_statement_node(cfg, if_node, code)
        for src in incoming:
            cfg.add_edge(src, condition_id, edge_type="control_flow")

        # Find then branch and else branch
        then_children = []
        else_children = []
        is_else = False

        for c in if_node.children:
            if c.type == "else" or c.type == "else_clause":
                is_else = True
            elif is_else:
                else_children.append(c)
            elif c.type in {"block", "suite", "statement_block"} or c.type in self.STATEMENT_TYPES:
                then_children.append(c)

        then_exits = []
        for tc in then_children:
            then_exits.extend(self._build_subgraph(cfg, tc, code, [condition_id]))

        else_exits = []
        if else_children:
            for ec in else_children:
                else_exits.extend(self._build_subgraph(cfg, ec, code, [condition_id]))
        else:
            # If no else, condition directly can fall through (false branch)
            else_exits = [condition_id]

        return list(set(then_exits + else_exits))

    def _handle_loop(
        self, cfg: nx.DiGraph, loop_node: Node, code: str, incoming: List[int]
    ) -> List[int]:
        """Builds CFG for loops."""
        loop_header_id = self._add_statement_node(cfg, loop_node, code)
        for src in incoming:
            cfg.add_edge(src, loop_header_id, edge_type="control_flow")

        body_nodes = []
        for c in loop_node.children:
            if c.type in {"block", "suite", "statement_block"} or c.type in self.STATEMENT_TYPES:
                body_nodes.append(c)

        body_exits = []
        for bn in body_nodes:
            body_exits.extend(self._build_subgraph(cfg, bn, code, [loop_header_id]))

        # Back edge to loop header
        for be in body_exits:
            cfg.add_edge(be, loop_header_id, edge_type="back_edge")

        # Exit edge when loop finishes
        return [loop_header_id]

    def _handle_try(
        self, cfg: nx.DiGraph, try_node: Node, code: str, incoming: List[int]
    ) -> List[int]:
        """Builds CFG for try / except blocks."""
        try_header_id = self._add_statement_node(cfg, try_node, code)
        for src in incoming:
            cfg.add_edge(src, try_header_id, edge_type="control_flow")

        exits = []
        for c in try_node.children:
            if c.type in {"block", "suite", "statement_block", "except_clause"}:
                exits.extend(self._build_subgraph(cfg, c, code, [try_header_id]))
        return exits if exits else [try_header_id]

