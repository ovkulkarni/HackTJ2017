import json

from flask import Blueprint, request, redirect, flash, g, render_template, url_for, session, jsonify

from decorators import login_required

blueprint = Blueprint("programs", __name__, url_prefix="/program")

@blueprint.route("/editor/")
@login_required
def editor():
    return render_template("editor.html", user=g.user)


@blueprint.route("/save/", methods=["POST"])
@login_required
def save():
    pgrm = json.loads(request.form.get("program"))
    print(pgrm)
    return jsonify({"success": True})
