from flask import Blueprint, request, redirect, flash, g

from .models import User

blueprint = Blueprint("users", __name__, url_prefix="/user")

@blueprint.route("/login/")
def login():
    if g.user:
        return redirect("index")
    if request.method == "POST":
        error = False
        try:
            u = User.get(email == request.form.get("email", ""))
        except User.DoesNotExist:
            error = True
            return redirect(".login")
        if not u.password.check_password(request.form.get("password", "")):
            error = True
        if error:
            flash("Failed login!", "error")
        else:
            g.user = u
        return redirect("index")
    else:
        return render_template("login.html")

@blueprint.route("/register/")
def register():
    return "Not yet implemented"
