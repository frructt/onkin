from sqlalchemy.orm import validates
from wtforms.validators import DataRequired

from film_aggregator import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)

    def __ref__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __ref__(self):
        return f"Film('{self.title}', '{self.year}', '{self.description}')"


class ImdbBasicName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nconst = db.Column(db.String(9), unique=False, nullable=False)
    primary_name = db.Column(db.String(100), unique=False, nullable=False)
    birth_year = db.Column(db.Integer,  unique=False, nullable=True)
    death_year = db.Column(db.Integer, unique=False, nullable=True)

    # @validates("birth_year", "death_year")
    # def empty_string_to_null(self, key, value):
    #     if value == '':
    #         return None
    #     else:
    #         return value
    primary_profession = db.Column(db.String(100), unique=False, nullable=True)
    known_for_titles = db.Column(db.String(200), unique=False, nullable=True)

    def __ref__(self):
        return f"ImdbBasicName('{self.nconst}', '{self.primary_name}', '{self.primary_profession}')"


db.create_all()
