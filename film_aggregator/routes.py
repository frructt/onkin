import functools

from flask import render_template, url_for, flash, redirect, request, send_from_directory
from film_aggregator.forms import RegistrationForm, LoginForm
from film_aggregator import app, db, bcrypt, file_upload, socketio, ROOMS
from film_aggregator.models import User, Film, UploadedFile, DemoFileStreamTable1
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room, disconnect
from time import strftime
from datetime import datetime
import base64


@app.route("/")
@app.route("/home")
@login_required
def home():
    files = DemoFileStreamTable1.query.first()
    # image = base64.b64encode(files[0].fileContent).decode("utf-8")
    return render_template("home.html", films=[files.my_file__file_name])


@app.route("/watch_video")
@login_required
def watch_video():
    video_list = DemoFileStreamTable1.query.all()
    return render_template("watch_video.html", video_list=video_list, rooms=ROOMS)


# decorator
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('message')
@authenticated_only
def message(data):
    print(f"\n\n{data}\n\n")
    send({"msg": data["msg"], "username": data["username"], "time_stamp": datetime.now().strftime("%b-%d %H:%M%S.%f")},
         room=data["room"])


@socketio.on("join")
@authenticated_only
def join(data):
    join_room(data["room"])
    msg_value = "{0} has joined the {1} room".format(data["username"], data["room"])
    send({"msg": msg_value}, room=data["room"])


@socketio.on("leave")
@authenticated_only
def leave(data):
    leave_room(data["room"])
    msg_value = "{0} has left the {1} room".format(data["username"], data["room"])
    send({"msg": msg_value}, room=data["room"])


@socketio.on('play-video')
@authenticated_only
def play_video(data):
    print(f"\n\n{data}\n\n")
    emit("onplay event", {"username": data["username"], "room": data["room"]}, broadcast=True)


@socketio.on('pause-video')
@authenticated_only
def pause_video(data):
    print(f"\n\n{data}\n\n")
    emit("onpause event", {"username": data["username"], "room": data["room"]}, broadcast=True)


@socketio.on('change-video-position')
@authenticated_only
def change_video_position(data):
    emit("change video position event",
         {"current_position": data["current_position"], "username": data["username"], "room": data["room"]},
         broadcast=True)


@app.route('/uploads/<filename>')
@login_required
def uploads(filename):
    file = DemoFileStreamTable1.query.filter_by(my_file__file_name=filename).first()
    return file_upload.stream_file(file, filename="my_file")


@app.route("/about")
@login_required
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
    return redirect(url_for("login"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files["upload"]
        model_instance = DemoFileStreamTable1()
        videos = DemoFileStreamTable1.query.all()
        if videos:
            model_instance.id = videos[-1].id + 1
            model_instance.name = file.filename
        else:
            model_instance.id = 1
            model_instance.name = file.filename
        file_upload.update_files(model_instance,
                                 files={
                                     "my_file": file
                                 })
        flash("Your file {} has been uploaded!".format(file.filename), "success")
        return redirect(url_for("home"))
    return render_template("upload.html", title="Upload")
