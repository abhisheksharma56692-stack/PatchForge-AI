"""Program Dependence Graph (PDG) merging CFG and DDG."""
from typing import Dict, Any, List
import networkx as nx


class PDGBuilder:
    """
    Merges Control Flow Graph (CFG) and Data Dependence Graph (DDG)
    into a unified Program Dependence Graph: G = (V, E_control ∪ E_data).
    """

    def build(self, cfg: nx.DiGraph, ddg: nx.DiGraph) -> nx.DiGraph:
        """
        Builds a unified PDG where nodes are unified by statement boundaries / line ranges.
        """
        pdg = nx.DiGraph()

        # Map DDG nodes by line range to correlate with CFG nodes
        line_to_pdg_id: Dict[int, int] = {}

        # First add all nodes from DDG
        for nid, data in ddg.nodes(data=True):
            pdg.add_node(nid, **data)
            start_l = data.get("start_line")
            if start_l:
                line_to_pdg_id[start_l] = nid

        # Add nodes from CFG that might not be in DDG
        for nid, data in cfg.nodes(data=True):
            start_l = data.get("start_line")
            if start_l and start_l not in line_to_pdg_id and data.get("node_type") not in {"ENTRY", "EXIT"}:
                pdg.add_node(nid, **data)
                line_to_pdg_id[start_l] = nid

        # Add data dependence edges from DDG
        for u, v, data in ddg.edges(data=True):
            if u in pdg and v in pdg:
                pdg.add_edge(u, v, **data)

        # Map CFG edges onto PDG nodes using line correlation
        cfg_to_pdg_map: Dict[int, int] = {}
        for cfg_id, data in cfg.nodes(data=True):
            start_l = data.get("start_line")
            if start_l in line_to_pdg_id:
                cfg_to_pdg_map[cfg_id] = line_to_pdg_id[start_l]
            elif cfg_id in pdg:
                cfg_to_pdg_map[cfg_id] = cfg_id

        for u, v, data in cfg.edges(data=True):
            mapped_u = cfg_to_pdg_map.get(u)
            mapped_v = cfg_to_pdg_map.get(v)
            if mapped_u is not None and mapped_v is not None and mapped_u != mapped_v:
                if not pdg.has_edge(mapped_u, mapped_v):
                    edge_data = dict(data)
                    edge_data["edge_type"] = "control"
                    pdg.add_edge(mapped_u, mapped_v, **edge_data)

        return pdg

