from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = '7104ba209f0cf2e63b28982f7b8782e8'
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://admin:12345@83.167.115.245/test?driver=SQL Server?Trusted_Connection=yes"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


from film_aggregator import routes  # , import_imdb_dataset
# import_imdb_dataset.run_db_imports()
