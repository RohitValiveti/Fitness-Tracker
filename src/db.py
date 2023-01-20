from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


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

    def __init__(self, muscle_group, time_started=datetime.now()) -> None:
        self.muscle_group = muscle_group
        self.time_started = time_started

    def serialize(self):
        """
        Serialize all columns to Json Format.
        """

        return {
            "id": self.id,
            "time_started": self.time_started.strftime("%m/%d/%Y, %H:%M:%S"),
            "time_ended": self.time_ended.strftime("%m/%d/%Y, %H:%M:%S") if self.time_ended else None,
            "muscle_group": self.muscle_group,
            "exercises": [e.simple_serialize() for e in self.exercises]
        }

    def simple_serialize(self):
        """
        Serializes all columns except for exercies
        """

        return {
            "id": self.id,
            "time_started": self.time_started.strftime("%m/%d/%Y, %H:%M:%S"),
            "time_ended": self.time_ended.strftime("%m/%d/%Y, %H:%M:%S") if self.time_ended else None,
            "muscle_group": self.muscle_group,
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
