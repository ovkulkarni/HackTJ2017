#!/usr/bin/env python3

from flask import Flask, render_template
import settings

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(threaded=True, debug=settings.DEBUG)
