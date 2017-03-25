#!/usr/bin/env python3

from flask import Flask, render_template
import settings

from utils import init_blueprints

app = Flask(__name__)

init_blueprints(app)

@app.route("/")
def index():
    return render_template("login.html")
