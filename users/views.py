from flask import Blueprint, request, redirect, flash, g, render_template

from .models import User

blueprint = Blueprint("users", __name__, url_prefix="/user")

@blueprint.route("/login/", methods=["GET", "POST"])
def login():
    # if g.user:
    #     return redirect("index")
    if request.method == "POST":
        error = False
        try:
            u = User.get(User.email == request.form.get("email", ""))
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

@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    # if g.user:
    #     return redirect("index")
    if request.method == "POST":
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        confirm = request.form.get("confirm", None)
        if not email or not password:
            flash("Please fill out all of the fields!", "error")
            return redirect(".register")
        if password != confirm:
            flash("Confirmation does not match password!", "error")
            return redirect(".register")
        try:
            u = User.get(User.email == email)
            flash("An account with this email already exists!", "error")
            return redirect(".register")
        except User.DoesNotExist:
            pass
        User.create(email=email, password=password)
        flash("Your account has been created!", "success")
        return redirect("index")
    else:
        return render_template("register.html")
