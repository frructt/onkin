import datetime
import functools

import jwt
from flask import render_template, url_for, flash, redirect, request, jsonify, make_response
from flask_login import current_user, logout_user, login_required
from flask_socketio import send, emit, join_room, leave_room, disconnect
# from server.forms import RegistrationForm, LoginForm
from sqlalchemy.exc import SQLAlchemyError

from server import app, db, file_upload, socketio, ROOMS
from server.models import User, DemoFileStreamTable1


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
        if not token:
            return jsonify({"error": "unauthorized",
                            "errorMessage": "Authorization has been denied for this request."}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(username=data["username"]).first()
            if not current_user:
                return jsonify({"error": "unauthorized",
                                "errorMessage": 'Token is invalid or user is not found.'}), 401
        except:
            return jsonify({"error": "unauthorized",
                            "errorMessage": 'Token is invalid.'}), 401
        return f(*args, **kwargs)

    return decorated


@socketio.on('connect', namespace='/test')
def test_connect():
    print('Client connected')


@app.route("/")
@app.route("/home")
@token_required
def home():
    return jsonify({"result": True})


@app.route("/api/users", methods=["GET"])
@token_required
def users():
    users_ = User.query.all()
    return jsonify([{"username": user.username} for user in users_])


# @app.route("/watch_video")
# @token_required
# def watch_video():
#     video_list = DemoFileStreamTable1.query.all()
#     return render_template("watch_video.html", video_list=video_list, rooms=ROOMS)


@app.route("/api/getVideoName")
@token_required
def get_video_name():
    video = DemoFileStreamTable1.query.first()
    return jsonify({"video_name": video.name})


@socketio.on('message')
@token_required
def message(data):
    print(f"\n\n{data}\n\n")
    send({"msg": data["msg"], "username": data["username"], "time_stamp": datetime.datetime.now().strftime("%b-%d %H:%M%S.%f")},
         room=data["room"])


@socketio.on("join")
@token_required
def join(data):
    join_room(data["room"])
    msg_value = "{0} has joined the {1} room".format(data["username"], data["room"])
    send({"msg": msg_value}, room=data["room"])


@socketio.on("leave")
@token_required
def leave(data):
    leave_room(data["room"])
    msg_value = "{0} has left the {1} room".format(data["username"], data["room"])
    send({"msg": msg_value}, room=data["room"])


@socketio.on('play-video')
@token_required
def play_video(data):
    print(f"\n\n{data}\n\n")
    emit("onplay event", {"username": data["username"], "room": data["room"]}, broadcast=True)


@socketio.on('pause-video')
@token_required
def pause_video(data):
    print(f"\n\n{data}\n\n")
    emit("onpause event", {"username": data["username"], "room": data["room"]}, broadcast=True)


@socketio.on('change-video-position')
@token_required
def change_video_position(data):
    emit("change video position event",
         {"current_position": data["current_position"], "username": data["username"], "room": data["room"]},
         broadcast=True)


@app.route('/api/uploads/<filename>')
def uploads(filename):
    file = DemoFileStreamTable1.query.filter_by(my_file__file_name=filename).first()
    return file_upload.stream_file(file, filename="my_file")


@app.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")


@app.route("/api/login", methods=["POST"])
def login():
    json_data = request.json
    user = User.query.filter_by(username=json_data["username"]).first()
    if user:
        return make_response({"message": "Login is already exist"}, 401)
    # create new user
    else:
        user = User(
            username=json_data["username"],
            password=json_data["password"]
        )
        try:
            # add new user to db
            db.session.add(user)
            db.session.commit()
            status = True
        except SQLAlchemyError as e:
            db.session.close()
            error = str(e.__dict__['orig'])
            return make_response({"message": error}, 498)
        try:
            token = jwt.encode({"username": user.username,
                                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)},
                               app.config["SECRET_KEY"])
            db.session.close()
            return jsonify({"token": token, "username": user.username})
        except:
            user.delete_user(json_data["username"])
            return make_response({"message": "Cannot create token"}, 498)


@app.route("/api/logout", methods=["POST"])
def logout():
    logout_user()
    json_data = request.json
    User.delete_user(json_data["username"])
    return make_response(jsonify({}), 204)


@app.route("/upload", methods=["GET", "POST"])
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
