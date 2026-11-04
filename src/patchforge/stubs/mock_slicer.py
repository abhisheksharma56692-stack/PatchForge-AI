"""Mock AST and taint slicer stub for Member 2 development."""
from patchforge.models.slicing import ASTContextSlice


class BackwardTaintSlicer:
    """Mock implementation returning a focused 35-line code slice."""

    def __init__(self, language: str = "python"):
        self.language = language

    def slice_from_location(
        self, source_code: str, line: int, sink_symbol: str = ""
    ) -> ASTContextSlice:
        mock_slice_code = (
            "import sqlite3\n"
            "from flask import Flask, request, jsonify\n\n"
            "def get_user():\n"
            "    username = request.args.get('username', '')\n"
            "    cursor = db.cursor()\n"
            "    # Tainted sink:\n"
            "    query = 'SELECT id, username FROM users WHERE username = ' + username\n"
            "    cursor.execute(query)\n"
            "    return jsonify({'users': cursor.fetchall()})\n"
        )
        return ASTContextSlice(
            slice_code=mock_slice_code,
            target_nodes=[{"node_id": 1, "text": "cursor.execute(query)", "line": line}],
            enclosing_function="get_user",
            enclosing_class=None,
            imported_symbols=["import sqlite3", "from flask import Flask, request, jsonify"],
            start_line=max(1, line - 10),
            end_line=line + 5,
            sliced_lines=list(range(max(1, line - 10), line + 6)),
            language=self.language,
        )

