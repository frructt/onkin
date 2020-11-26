from flask import render_template, url_for, flash, redirect, request
from film_aggregator.forms import RegistrationForm, LoginForm
from film_aggregator import app, db, bcrypt, file_upload
from film_aggregator.models import User, Film, UploadedFile, DemoFileStreamTable1
from flask_login import login_user, current_user, logout_user, login_required
import base64

# films = [
#     {
#         "name": "name1",
#         "genre": "genre1",
#         "year": 2005
#     },
#     {
#         "name": "name2",
#         "genre": "genre2",
#         "year": 2006
#     },
#     {
#         "name": "name3",
#         "genre": "genre3",
#         "year": 2005
#     }
# ]


@app.route("/")
@app.route("/home")
def home():
    files = UploadedFile.query.all()
    # image = base64.b64encode(files[0].fileContent).decode("utf-8")
    return render_template("home.html", films=files, base64=base64)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Now you can log in", "success")
        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["upload"]
        new_file = DemoFileStreamTable1(filename=file.filename)
        new_file = file_upload.update_files(new_file, files={
            "upload": file.read()
        })
        db.session.add(new_file)
        db.session.commit()
        flash("Your file {} has been uploaded!".format(file.filename), "success")
        return redirect(url_for("home"))
    return render_template("upload.html", title="Upload")
