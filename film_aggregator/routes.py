from flask import render_template, url_for, flash, redirect
from film_aggregator.forms import RegistrationForm, LoginForm
from film_aggregator import app
from film_aggregator.models import User, Film

films = [
    {
        "name": "name1",
        "genre": "genre1",
        "year": 2005
    },
    {
        "name": "name2",
        "genre": "genre2",
        "year": 2006
    },
    {
        "name": "name3",
        "genre": "genre3",
        "year": 2005
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", films=films)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@film.com" and form.password.data == "1":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)
