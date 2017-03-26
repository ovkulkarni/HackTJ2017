from flask import Blueprint, request, redirect, flash, g, render_template, url_for, session

from decorators import login_required

blueprint = Blueprint("programs", __name__, url_prefix="/program")

@blueprint.route("/editor/")
@login_required
def editor():
    return render_template("editor.html")
