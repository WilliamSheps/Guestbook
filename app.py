from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)