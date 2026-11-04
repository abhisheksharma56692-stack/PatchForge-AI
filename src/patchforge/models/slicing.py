"""AST and Program Dependence Graph (PDG) slicing models."""
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class PDGNode(BaseModel):
    """Represents a statement/expression node in CFG / DDG / PDG."""
    node_id: int
    node_type: str
    text: str
    line_start: int
    line_end: int
    col_start: int = 0
    col_end: int = 0
    variables_defined: List[str] = Field(default_factory=list)
    variables_used: List[str] = Field(default_factory=list)


class ASTContextSlice(BaseModel):
    """Contextual slice extracted around a taint sink."""
    slice_code: str
    target_nodes: List[Dict[str, Any]] = Field(default_factory=list)
    enclosing_function: str = ""
    enclosing_class: Optional[str] = None
    imported_symbols: List[str] = Field(default_factory=list)
    start_line: int
    end_line: int
    sliced_lines: List[int] = Field(default_factory=list)
    language: str = "python"


# Alias for backward compatibility with ARCHITECTURE.md naming
ASTSliceContext = ASTContextSlice


class SlicingResult(BaseModel):
    """Metadata report of the backward taint slicing operation."""
    slice_context: ASTContextSlice
    total_original_lines: int
    total_sliced_lines: int
    reduction_percentage: float
    sink_node_id: Optional[int] = None

