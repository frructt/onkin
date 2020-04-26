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
    primaryId = db.Column(db.String(11), unique=False, nullable=False)
    primaryName = db.Column(db.String(100), unique=False, nullable=True)
    birthYear = db.Column(db.Integer,  unique=False, nullable=True)
    deathYear = db.Column(db.Integer, unique=False, nullable=True)

    # @validates("birth_year", "death_year")
    # def empty_string_to_null(self, key, value):
    #     if value == '':
    #         return None
    #     else:
    #         return value
    primaryProfession = db.Column(db.String(300), unique=False, nullable=True)
    knownForTitles = db.Column(db.String(300), unique=False, nullable=True)

    def __ref__(self):
        return f"ImdbBasicName('{self.primaryId}', '{self.primaryName}', '{self.primaryProfession}')"


class ImdbAkas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titleId = db.Column(db.String, unique=False, nullable=True)
    ordering = db.Column(db.Integer, unique=False, nullable=True)
    title = db.Column(db.String, unique=False, nullable=True)
    region = db.Column(db.String, unique=False, nullable=True)
    language = db.Column(db.String, unique=False, nullable=True)
    types = db.Column(db.String, unique=False, nullable=True)
    attributes = db.Column(db.String, unique=False, nullable=True)
    isOriginalTitle = db.Column(db.Integer, unique=False, nullable=True)


class ImdbCrew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primaryId = db.Column(db.String, unique=False, nullable=False)
    directors = db.Column(db.String, unique=False, nullable=True)
    writers = db.Column(db.String, unique=False, nullable=True)


class ImdbEpisode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primaryId = db.Column(db.String, unique=False, nullable=False)
    parentPrimaryId = db.Column(db.String, unique=False, nullable=True)
    seasonNumber = db.Column(db.Integer, unique=False, nullable=True)
    episodeNumber = db.Column(db.Integer, unique=False, nullable=True)


class ImdbRaitings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primaryId = db.Column(db.String, unique=False, nullable=False)
    averageRating = db.Column(db.Float, unique=False, nullable=True)
    numVotes = db.Column(db.Float, unique=False, nullable=True)


class ImdbTitleBasics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primaryId = db.Column(db.String, unique=False, nullable=False)
    titleType = db.Column(db.String, unique=False, nullable=True)
    primaryTitle = db.Column(db.String, unique=False, nullable=True)
    originalTitle = db.Column(db.String, unique=False, nullable=True)
    isAdult = db.Column(db.Integer, unique=False, nullable=True)
    startYear = db.Column(db.Integer, unique=False, nullable=True)
    endYear = db.Column(db.Integer, unique=False, nullable=True)
    runtimeMinutes = db.Column(db.Integer, unique=False, nullable=True)
    genres = db.Column(db.String, unique=False, nullable=True)


db.create_all()
