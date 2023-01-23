from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import bcrypt
import os
import hashlib


db = SQLAlchemy()

friends_table = db.Table(
    "friends_table",
    db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey('user.id')),
    db.Column("friend_id", db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    """
    ORM representing a User Model.
    """

    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    session_token = db.Column(db.String, nullable=False, unique=True)
    update_token = db.Column(db.String, nullable=False, unique=True)
    session_expiration = db.Column(db.DateTime, nullable=False)
    workouts = db.relationship('Workout', cascade='delete')
    friends = db.relationship(
        'User', secondary=friends_table, back_populates='friends')

    def __init__(self, email, password_raw) -> None:
        self.email = email
        self.password = bcrypt.hashpw(
            password_raw.encode("utf8"), bcrypt.gensalt(rounds=13))
        self.renew_session()

    def _urlsafe_base_64(self):
        """
        Randomly generates hashed tokens (used for session/update tokens)
        """
        return hashlib.sha1(os.urandom(64)).hexdigest()

    def renew_session(self):
        """
        Renews the sessions by:
        1. Creates a new session token
        2. Sets the expiration time of the session to be a day from now
        3. Creates a new update token
        """
        self.session_token = self._urlsafe_base_64()
        self.session_expiration = datetime.now() + datetime.timedelta(days=1)
        self.update_token = self._urlsafe_base_64()

    def verify_password(self, password):
        """
        Verifies the password of a user
        """
        return bcrypt.checkpw(password.encode("utf8"), self.password)

    def verify_session_token(self, session_token):
        """
        Verifies the session token of a user
        """
        return session_token == self.session_token and datetime.now() < self.session_expiration

    def verify_update_token(self, update_token):
        """
        Verifies the update token of a user
        """
        return update_token == update_token

    def simple_serialize(self):
        """
        Returns simple serialized model of user.
        """

        return {
            'id': self.id,
            'email': self.email
        }

    def serialize(self):
        """
        Returns serialized model of user.
        """

        return {
            'id': self.id,
            'email': self.email,
            'workouts': [w.simple_serialize() for w in self.workouts],
            'friends': [f.simple_serialize() for f in self.friends]
        }


class Workout(db.Model):
    """
    ORM representing a Workout Model.
    """

    __tablename__ = 'workout'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_started = db.Column(db.DateTime, nullable=False)
    time_ended = db.Column(db.DateTime)
    muscle_group = db.Column(db.String, nullable=False)
    exercises = db.relationship('Exercise', cascade='delete')
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, muscle_group, time_started=datetime.now()) -> None:
        self.muscle_group = muscle_group
        self.time_started = time_started

    def serialize(self):
        """
        Serialize all columns to Json Format.
        """

        return {
            "id": self.id,
            "time_started": str(self.time_started),
            "time_ended": str(self.time_ended) if self.time_ended else None,
            "muscle_group": self.muscle_group,
            "exercises": [e.simple_serialize() for e in self.exercises],
            "user_id": self.user_id
        }

    def simple_serialize(self):
        """
        Serializes all columns except for exercies
        """

        return {
            "id": self.id,
            "time_started": str(self.time_started),
            "time_ended": str(self.time_ended) if self.time_ended else None,
            "muscle_group": self.muscle_group,
            "user_id": self.user_id
        }


class Exercise(db.Model):
    """
    ORM representing an Exercise Model.
    """

    __tablename__ = 'exercise'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exercise_name = db.Column(db.String, nullable=False)
    muscle = db.Column(db.String, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey(Workout.id))
    sets = db.relationship('Set', cascade='delete')

    def __init__(self, exercise_name, muscle, workout_id=None) -> None:
        self.muscle = muscle
        self.exercise_name = exercise_name
        self.workout_id = workout_id

    def serialize(self):
        """
        Serialize.
        """
        return {
            "id": self.id,
            "exercise_name": self.exercise_name,
            "muslce": self.muscle,
            "workout_id": self.workout_id,
            "sets": [s.serialize() for s in self.sets]
        }

    def simple_serialize(self):
        """
        Serialize all columns except for sets.
        """
        return {
            "id": self.id,
            "exercise_name": self.exercise_name,
            "muslce": self.muscle,
            "workout_id": self.workout_id,
        }


class Set(db.Model):
    """
    ORM representing a Set Model.
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    weight = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey(Exercise.id))

    def __init__(self, weight, repetitions, exercise_id=None) -> None:
        self.weight = weight
        self.repetitions = repetitions
        self.exercise_id = exercise_id

    def serialize(self):
        """
        Serialize Set.
        """
        return {
            "id": self.id,
            "weight": self.weight,
            "repetitions": self.repetitions,
            "exercise_id": self.exercise_id
        }
