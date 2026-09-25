from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)

GUESTBOOK_FILE = os.path.join(os.path.dirname(__file__), "guestbook.txt")
ENTRY_SEPARATOR = "\n===\n"


def load_entries():
    if not os.path.exists(GUESTBOOK_FILE):
        return []

    with open(GUESTBOOK_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return []

    entries = []
    for block in content.split(ENTRY_SEPARATOR):
        block = block.strip("\n")
        if not block.strip():
            continue

        lines = block.split("\n")
        entry = {"name": "", "time": "", "comment": ""}

        if len(lines) >= 1 and lines[0].startswith("name:"):
            entry["name"] = lines[0][len("name:"):].strip()
        if len(lines) >= 2 and lines[1].startswith("time:"):
            entry["time"] = lines[1][len("time:"):].strip()
        if len(lines) >= 3:
            rest = lines[3:] if lines[2].strip() == "comment:" else lines[2:]
            entry["comment"] = "\n".join(rest).strip()

        entries.append(entry)

    entries.reverse()  # nyaste inlägget överst
    return entries


@app.route("/")
def index():
    entries = load_entries()
    return render_template("index.html", entries=entries)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name", "").strip()
    comment = request.form.get("comment", "").strip()

    if not name:
        name = "Anonym"
    comment = comment[:200]

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry_text = f"name:{name}\ntime:{timestamp}\ncomment:\n{comment}"

    file_exists_and_has_content = (
        os.path.exists(GUESTBOOK_FILE) and os.path.getsize(GUESTBOOK_FILE) > 0
    )

    with open(GUESTBOOK_FILE, "a", encoding="utf-8") as f:
        if file_exists_and_has_content:
            f.write(ENTRY_SEPARATOR)
        f.write(entry_text)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)