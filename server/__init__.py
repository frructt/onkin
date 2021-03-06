from os.path import join, dirname, realpath

from flask import Flask
from flask_file_upload import FileUpload
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["SESSION_TYPE"] = "filesystem"
# app.config['CORS_HEADER'] = 'Content-Type'
app.config['CORS_ALLOW_HEADERS'] = "*"
app.config["SECRET_KEY"] = '7104ba209f0cf2e63b28982f7b8782e8'
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://admin:12345@83.167.115.245/TestFileStream?driver=SQL Server?Trusted_Connection=yes"
api = Api(app)
db = SQLAlchemy(app)
socketio = SocketIO(app, manage_session=False, cors_allowed_origins='*')
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#     return response


ROOMS = ["Room1", "Room2", "Room3"]

# Environment variables
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
UPLOAD_FOLDER = join(dirname(realpath(__file__)), "uploads")
ALLOWED_EXTENSIONS = ["jpg", "png", "mov", "mp4", "mpg"]
MAX_CONTENT_LENGTH = 1000 * 1024 * 1024  # 1000mb
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://admin:12345@83.167.115.245/TestFileStream?driver=SQL Server?Trusted_Connection=yes"

file_upload = FileUpload(
    app,
    db,
    upload_folder=UPLOAD_FOLDER,
    allowed_extensions=ALLOWED_EXTENSIONS,
    max_content_length=MAX_CONTENT_LENGTH,
    sqlalchemy_database_uri=SQLALCHEMY_DATABASE_URI,
)


# An example using the Flask factory pattern
def create_app():
    # Dynamically set config variables:
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
    app.config["ALLOWED_EXTENSIONS"] = ALLOWED_EXTENSIONS
    app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI

    file_upload.init_app(app, db)


from server import routes  # , import_imdb_dataset
# import_imdb_dataset.run_db_imports()
