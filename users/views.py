from flask import Blueprint, request, redirect, flash, g, render_template, url_for

from .models import User

blueprint = Blueprint("users", __name__, url_prefix="/user")

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    if hasattr(g, "user"):
        return redirect(url_for("index"))
    if request.method == "POST":
        error = False
        try:
            u = User.get(User.email == request.form.get("email", ""))
            if not u.password.check_password(request.form.get("password", "")):
                error = True
        except User.DoesNotExist:
            error = True
        if error:
            flash("Failed login!", "error")
            return redirect(url_for(".login"))
        else:
            g.user = u
            print(g)
            return redirect(url_for("index"))
    else:
        return render_template("login.html")

@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    if hasattr(g, "user"):
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        confirm = request.form.get("confirm", None)
        if not name or not email or not password:
            flash("Please fill out all of the fields!", "error")
            return redirect(url_for(".register"))
        if password != confirm:
            flash("Confirmation does not match password!", "error")
            return redirect(url_for(".register"))
        try:
            u = User.get(User.email == email)
            flash("An account with this email already exists!", "error")
            return redirect(url_for(".login"))
        except User.DoesNotExist:
            pass
        u = User.create(name=name, email=email, password=password)
        flash("Your account has been created!", "success")
        g.user = u
        return redirect(url_for(".login"))
    else:
        return render_template("register.html")
