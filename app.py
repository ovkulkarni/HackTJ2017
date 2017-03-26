#!/usr/bin/env python3

from flask import Flask, render_template, g, redirect, url_for
import settings

from utils import init_blueprints
from decorators import login_required

app = Flask(__name__)

app.secret_key = settings.SECRET_KEY

init_blueprints(app)

@app.route("/")
def index():
    if g.user is None:
        return redirect(url_for("users.login"))
    return render_template("index.html", user=g.user)
