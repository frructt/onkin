import functools
import jwt

from flask import render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, \
    make_response
# from server.forms import RegistrationForm, LoginForm
from server import app, db, bcrypt, file_upload, socketio, ROOMS
from server.models import User, Film, UploadedFile, DemoFileStreamTable1
from flask_login import login_user, current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room, disconnect
from time import strftime
import datetime
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


# decorator for verifying the JWT
def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if "HTTP_AUTHORIZATION" in request.headers.environ.keys():
            token = request.headers.environ["HTTP_AUTHORIZATION"][7:]
            # return 401 if token is not passed
        # return 401 if token is not passed
        if not token:
            return jsonify({"error": "unauthorized",
                            "errorMessage": "Authorization has been denied for this request."}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data["user"]).first()
            if not current_user:
                return jsonify({"error": "unauthorized",
                                "errorMessage": 'Token is invalid.'}), 401
        except:
            return jsonify({"error": "unauthorized",
                            "errorMessage": 'Token is invalid.'}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/")
@app.route("/home")
@login_required
def home():
    return jsonify({"result": True})


@app.route("/api/users", methods=["GET"])
@token_required
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
    send({"msg": data["msg"], "username": data["username"], "time_stamp": datetime.datetime.now().strftime("%b-%d %H:%M%S.%f")},
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


@app.route("/api/login", methods=["GET", "POST"])
def login():
    json_data = request.json
    user = User.query.filter_by(username=json_data["username"]).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data["password"]):
        # login_user(user)
        # session['logged_in'] = True
        token = jwt.encode({"user": user.username,
                            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                           app.config["SECRET_KEY"])
        return jsonify({"token": token, "user": user.username})
    else:
        return make_response("Could not verify!", 401, {"WWW-Authenticate": "Basic realm: Login Required"})


@app.route("/api/logout", methods=["POST"])
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
