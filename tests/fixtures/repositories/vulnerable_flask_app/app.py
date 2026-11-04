"""Intentionally vulnerable Flask application for testing SQL injection (CWE-89)."""
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, email TEXT)")
    cursor.execute("INSERT INTO users (username, email) VALUES ('admin', 'admin@example.com')")
    cursor.execute("INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com')")
    conn.commit()
    return conn


db = init_db()


@app.route("/user", methods=["GET"])
def get_user():
    username = request.args.get("username", "")
    cursor = db.cursor()
    # Vulnerable sink: Raw string concatenation into SQL statement (CWE-89)
    query = "SELECT id, username, email FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    rows = cursor.fetchall()
    return jsonify({"users": rows})


if __name__ == "__main__":
    app.run(port=5000)

