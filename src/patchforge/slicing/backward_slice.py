"""Backward taint slicing: extracts minimal code slice from sink to source."""
from typing import Set, List, Dict, Any, Optional
import networkx as nx

from patchforge.models.slicing import ASTContextSlice, SlicingResult
from patchforge.slicing.parser import MultiLanguageParser
from patchforge.slicing.cfg_builder import CFGBuilder
from patchforge.slicing.ddg_builder import DDGBuilder
from patchforge.slicing.pdg import PDGBuilder


class BackwardTaintSlicer:
    """
    Computes a minimal backward slice from a taint sink node in a Program
    Dependence Graph (PDG), preserving necessary context (imports, signatures).
    """

    def __init__(self, language: str = "python"):
        self.language = language
        self.parser = MultiLanguageParser(language)
        self.cfg_builder = CFGBuilder()
        self.ddg_builder = DDGBuilder()
        self.pdg_builder = PDGBuilder()

    def slice(self, pdg: nx.DiGraph, sink_id: int, full_code: str) -> ASTContextSlice:
        """Extracts backward slice reachable from sink_id in PDG."""
        if sink_id not in pdg:
            # Fallback if sink_id is not exact: find closest node
            nodes = list(pdg.nodes())
            if not nodes:
                return ASTContextSlice(
                    slice_code=full_code,
                    start_line=1,
                    end_line=len(full_code.splitlines()),
                    sliced_lines=list(range(1, len(full_code.splitlines()) + 1)),
                    language=self.language,
                )
            sink_id = nodes[-1]

        # Backward reachability: ancestors in PDG
        reachable_ids = nx.ancestors(pdg, sink_id) | {sink_id}

        lines = full_code.splitlines()
        total_lines = len(lines)

        # Collect sliced line numbers (1-based)
        sliced_line_set: Set[int] = set()
        target_nodes_info = []

        for nid in reachable_ids:
            data = pdg.nodes[nid]
            start_l = data.get("start_line", 1)
            end_l = data.get("end_line", start_l)
            for l in range(start_l, end_l + 1):
                if 1 <= l <= total_lines:
                    sliced_line_set.add(l)
            target_nodes_info.append({
                "node_id": nid,
                "text": data.get("text", ""),
                "type": data.get("node_type", ""),
                "start_line": start_l,
                "end_line": end_l,
            })

        # Preserve import statements
        tree = self.parser.parse(full_code)
        imports = self.parser.extract_imported_symbols(tree, full_code)
        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from ") or stripped.startswith("const ") and "require(" in stripped:
                sliced_line_set.add(idx)

        # Find enclosing function
        min_line = min(sliced_line_set) if sliced_line_set else 1
        max_line = max(sliced_line_set) if sliced_line_set else total_lines

        enclosing_fn = self.parser.find_enclosing_function(tree, min_line)
        enclosing_fn_name = ""
        if enclosing_fn:
            for c in enclosing_fn.children:
                if c.type in {"identifier", "name"}:
                    enclosing_fn_name = full_code[c.start_byte:c.end_byte]
                    break
            # Add function header line
            sliced_line_set.add(enclosing_fn.start_point[0] + 1)

        # Find enclosing class
        enclosing_cls = self.parser.find_enclosing_class(tree, min_line)
        enclosing_cls_name = None
        if enclosing_cls:
            for c in enclosing_cls.children:
                if c.type in {"identifier", "name"}:
                    enclosing_cls_name = full_code[c.start_byte:c.end_byte]
                    break
            sliced_line_set.add(enclosing_cls.start_point[0] + 1)

        sorted_lines = sorted(list(sliced_line_set))
        sliced_text_lines = [lines[l - 1] for l in sorted_lines if 1 <= l <= total_lines]
        slice_code = "\n".join(sliced_text_lines)

        return ASTContextSlice(
            slice_code=slice_code,
            target_nodes=target_nodes_info,
            enclosing_function=enclosing_fn_name,
            enclosing_class=enclosing_cls_name,
            imported_symbols=imports,
            start_line=min_line,
            end_line=max_line,
            sliced_lines=sorted_lines,
            language=self.language,
        )

    def slice_from_location(
        self, source_code: str, line: int, sink_symbol: str = ""
    ) -> ASTContextSlice:
        """
        Parses source_code, builds CFG+DDG+PDG, identifies sink at line/sink_symbol,
        and computes minimal backward slice.
        """
        tree = self.parser.parse(source_code)
        cfg = self.cfg_builder.build(tree.root_node, source_code)
        ddg = self.ddg_builder.build(tree.root_node, source_code)
        pdg = self.pdg_builder.build(cfg, ddg)

        # Locate sink node closest to line
        best_node_id = None
        min_dist = float("inf")

        for nid, data in pdg.nodes(data=True):
            start_l = data.get("start_line", 0)
            text = data.get("text", "")
            
            # Prioritize matching symbol if given
            if sink_symbol and sink_symbol in text and abs(start_l - line) <= 3:
                best_node_id = nid
                break
                
            dist = abs(start_l - line)
            if dist < min_dist:
                min_dist = dist
                best_node_id = nid

        if best_node_id is None and len(pdg.nodes()) > 0:
            best_node_id = list(pdg.nodes())[0]

        return self.slice(pdg, best_node_id, source_code)

