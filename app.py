#!/usr/bin/env python3

from flask import Flask, render_template
import settings

from utils import init_blueprints
from decorators import login_required

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY

init_blueprints(app)

@app.route("/")
@login_required
def index():
    return render_template("index.html")
