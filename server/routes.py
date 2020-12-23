import functools

from flask import render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session
# from server.forms import RegistrationForm, LoginForm
from server import app, db, bcrypt, file_upload, socketio, ROOMS
from server.models import User, Film, UploadedFile, DemoFileStreamTable1
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room, disconnect
from time import strftime
from datetime import datetime
from flask_restful import Resource


import base64


# decorator
def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@app.route("/")
@app.route("/home")
@login_required
def home():
    return jsonify({"result": True})


@app.route("/users", methods=["GET"])
def users():
    users_ = User.query.all()
    return jsonify([{"username": user.username} for user in users_])


@app.route("/watch_video")
@login_required
def watch_video():
    video_list = DemoFileStreamTable1.query.all()
    return render_template("watch_video.html", video_list=video_list, rooms=ROOMS)


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


@app.route('/register', methods=["POST"])
def register():
    json_data = request.json
    user = User(
        username=json_data["username"],
        password=json_data["password"]
    )
    try:
        db.session.add(user)
        db.session.commit()
        status = "success"
    except:
        status = "this user is already registered"
    db.session.close()
    return jsonify({"result": status})


@app.route("/login", methods=["GET", "POST"])
def login():
    json_data = request.json
    user = User.query.filter_by(username=json_data["username"]).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data["password"]):
        login_user(user)
        # session['logged_in'] = True
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify(**{"result": 200,
                      "data": {"message": "logout success"}})


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
