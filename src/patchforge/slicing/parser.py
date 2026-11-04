"""Tree-sitter multi-language parser wrapper."""
from typing import Optional, List, Dict, Any
from tree_sitter import Language, Parser, Tree, Node

# Pre-load available grammars
LANGUAGES = {}

try:
    import tree_sitter_python
    LANGUAGES["python"] = Language(tree_sitter_python.language())
    LANGUAGES["py"] = LANGUAGES["python"]
except ImportError:
    pass

try:
    import tree_sitter_javascript
    LANGUAGES["javascript"] = Language(tree_sitter_javascript.language())
    LANGUAGES["js"] = LANGUAGES["javascript"]
    LANGUAGES["typescript"] = LANGUAGES["javascript"]
    LANGUAGES["ts"] = LANGUAGES["javascript"]
except ImportError:
    pass

try:
    import tree_sitter_go
    LANGUAGES["go"] = Language(tree_sitter_go.language())
except ImportError:
    pass


class MultiLanguageParser:
    """Multi-language AST parser wrapper powered by Tree-sitter."""

    def __init__(self, language: str = "python"):
        self.language_name = language.lower()
        if self.language_name in LANGUAGES:
            self.language = LANGUAGES[self.language_name]
            self.parser = Parser(self.language)
        elif "python" in LANGUAGES:
            # Fallback to python
            self.language = LANGUAGES["python"]
            self.parser = Parser(self.language)
        else:
            raise RuntimeError(f"No Tree-sitter grammar available for {language}")

    def parse(self, code: str) -> Tree:
        """Parses a string into a Tree-sitter Tree."""
        code_bytes = code.encode("utf-8")
        return self.parser.parse(code_bytes)

    def get_node_at_position(self, tree: Tree, line: int, col: int = 1) -> Optional[Node]:
        """
        Finds the deepest AST node spanning line and col.
        Assumes 1-based indexing for line and col from SARIF/external tools.
        """
        target_point = (max(0, line - 1), max(0, col - 1))
        root = tree.root_node

        def search(node: Node) -> Optional[Node]:
            # Check if point is within node
            start_p = node.start_point
            end_p = node.end_point

            # Point comparison: start_p <= target_point <= end_p
            if (start_p[0] < target_point[0] or (start_p[0] == target_point[0] and start_p[1] <= target_point[1])) and \
               (end_p[0] > target_point[0] or (end_p[0] == target_point[0] and end_p[1] >= target_point[1])):
                # Check children for a tighter match
                for child in node.children:
                    res = search(child)
                    if res is not None:
                        return res
                return node
            return None

        matched = search(root)
        return matched if matched is not None else root

    def extract_function_body(self, tree: Tree, func_name: str, code: str) -> str:
        """Extracts the source text of the function with name func_name."""
        root = tree.root_node

        def find_func(node: Node) -> Optional[Node]:
            if node.type in {"function_definition", "function_declaration", "method_definition"}:
                for child in node.children:
                    if child.type in {"identifier", "name"}:
                        name_text = code[child.start_byte:child.end_byte]
                        if name_text == func_name:
                            return node
            for child in node.children:
                res = find_func(child)
                if res:
                    return res
            return None

        fn_node = find_func(root)
        if fn_node:
            return code[fn_node.start_byte:fn_node.end_byte]
        return ""

    def find_enclosing_function(self, tree: Tree, line: int) -> Optional[Node]:
        """Finds the enclosing function node for a given 1-based line."""
        target_line = max(0, line - 1)
        root = tree.root_node

        enclosing = None
        def traverse(node: Node):
            nonlocal enclosing
            if node.type in {"function_definition", "function_declaration", "method_definition"}:
                if node.start_point[0] <= target_line <= node.end_point[0]:
                    enclosing = node
            for child in node.children:
                traverse(child)

        traverse(root)
        return enclosing

    def find_enclosing_class(self, tree: Tree, line: int) -> Optional[Node]:
        """Finds the enclosing class node for a given 1-based line."""
        target_line = max(0, line - 1)
        root = tree.root_node

        enclosing = None
        def traverse(node: Node):
            nonlocal enclosing
            if node.type in {"class_definition", "class_declaration"}:
                if node.start_point[0] <= target_line <= node.end_point[0]:
                    enclosing = node
            for child in node.children:
                traverse(child)

        traverse(root)
        return enclosing

    def extract_imported_symbols(self, tree: Tree, code: str) -> List[str]:
        """Extracts all imported library/symbol statements."""
        imports = []
        root = tree.root_node

        for child in root.children:
            if child.type in {"import_statement", "import_from_statement", "import_declaration"}:
                imports.append(code[child.start_byte:child.end_byte].strip())

        return imports

