import secrets
import string

import flask_file_upload
from sqlalchemy.exc import SQLAlchemyError

from server import db, login_manager, file_upload
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def to_json(self):
        return {"username": self.username}

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @staticmethod
    def delete_user(username):
        try:
            User.query.filter_by(username=username).delete()
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    @staticmethod
    def get_user(username):
        try:
            return User.query.filter_by(username=username).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(4), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    @staticmethod
    def delete_room(name):
        try:
            Room.query.filter_by(name=name).delete()
            db.session.commit()
            db.session.close()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    @staticmethod
    def get_room(name):
        try:
            return Room.query.filter_by(name=name).first()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)

    @staticmethod
    def add_new_room(username):
        # if user has already added to any group delete the db row
        user_id = User.get_user(username).id
        rooms = Room.query.filter_by(user_id=user_id)
        [Room.delete_room(room.name) for room in rooms if rooms]

        new_room_name = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
        try:
            room_name = Room.query.filter_by(name=new_room_name).first()
            while room_name:
                new_room_name = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(4))
            room_dto = Room(name=new_room_name, user_id=user_id)
            db.session.add(room_dto)
            db.session.commit()
            return new_room_name
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            print(error)


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __ref__(self):
        return f"Film('{self.title}', '{self.year}', '{self.description}')"


class UploadedFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    fileContent = db.Column(db.LargeBinary, nullable=False)


@file_upload.Model
class DemoFileStreamTable1(db.Model):
    __tablename__ = "demoTable"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    my_file = file_upload.Column()


# class ImdbBasicName(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     primaryId = db.Column(db.String(11), unique=False, nullable=False)
#     primaryName = db.Column(db.String(100), unique=False, nullable=True)
#     birthYear = db.Column(db.Integer,  unique=False, nullable=True)
#     deathYear = db.Column(db.Integer, unique=False, nullable=True)
#
#     # @validates("birth_year", "death_year")
#     # def empty_string_to_null(self, key, value):
#     #     if value == '':
#     #         return None
#     #     else:
#     #         return value
#     primaryProfession = db.Column(db.String(300), unique=False, nullable=True)
#     knownForTitles = db.Column(db.String(300), unique=False, nullable=True)
#
#     def __ref__(self):
#         return f"ImdbBasicName('{self.primaryId}', '{self.primaryName}', '{self.primaryProfession}')"
#
#
# class ImdbAkas(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     titleId = db.Column(db.String, unique=False, nullable=True)
#     ordering = db.Column(db.Integer, unique=False, nullable=True)
#     title = db.Column(db.String, unique=False, nullable=True)
#     region = db.Column(db.String, unique=False, nullable=True)
#     language = db.Column(db.String, unique=False, nullable=True)
#     types = db.Column(db.String, unique=False, nullable=True)
#     attributes = db.Column(db.String, unique=False, nullable=True)
#     isOriginalTitle = db.Column(db.Integer, unique=False, nullable=True)
#
#
# class ImdbCrew(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     primaryId = db.Column(db.String, unique=False, nullable=False)
#     directors = db.Column(db.String, unique=False, nullable=True)
#     writers = db.Column(db.String, unique=False, nullable=True)
#
#
# class ImdbEpisode(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     primaryId = db.Column(db.String, unique=False, nullable=False)
#     parentPrimaryId = db.Column(db.String, unique=False, nullable=True)
#     seasonNumber = db.Column(db.Integer, unique=False, nullable=True)
#     episodeNumber = db.Column(db.Integer, unique=False, nullable=True)
#
#
# class ImdbRaitings(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     primaryId = db.Column(db.String, unique=False, nullable=False)
#     averageRating = db.Column(db.Float, unique=False, nullable=True)
#     numVotes = db.Column(db.Float, unique=False, nullable=True)
#
#
# class ImdbTitleBasics(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     primaryId = db.Column(db.String, unique=False, nullable=False)
#     titleType = db.Column(db.String, unique=False, nullable=True)
#     primaryTitle = db.Column(db.String, unique=False, nullable=True)
#     originalTitle = db.Column(db.String, unique=False, nullable=True)
#     isAdult = db.Column(db.Integer, unique=False, nullable=True)
#     startYear = db.Column(db.Integer, unique=False, nullable=True)
#     endYear = db.Column(db.Integer, unique=False, nullable=True)
#     runtimeMinutes = db.Column(db.Integer, unique=False, nullable=True)
#     genres = db.Column(db.String, unique=False, nullable=True)


db.create_all()
