from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import os

app = Flask(__name__)

GUESTBOOK_FILE = os.path.join(os.path.dirname(__file__), "guestbook.txt")
ENTRY_SEPARATOR = "\n===\n"

@app.route("/")
def index():
    return render_template("index.html")

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