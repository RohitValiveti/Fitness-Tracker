import json
from flask import Flask, request
from db import db, Workout, Exercise, Set

app = Flask(__name__)

db_filename = "excercises.db"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///%s" % db_filename
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
with app.app_context():
    db.create_all()


def success_response(data, code=200):
    return json.dumps(data), code


def failure_response(msg, code):
    return json.dumps({"error": msg}), code

# ENDPOINTS

# Workouts


@app.route("/workouts/", methods=['POST', 'GET'])
def get_create_workouts():
    """
    Retrieves all workouts if GET request.
    Creates new workout if POST reqeust. Request body should contain muscle group
    of exercises.
    """
    if request.method == 'GET':
        workouts = [w.simple_serialize() for w in Workout.query.all()]
        return success_response({'workouts': workouts})
    elif request.method == 'POST':
        body = json.loads(request.data)
        muscle_group = body.get('muscle_group')
        if muscle_group is None:
            return failure_response('Please specify muscle group.', 400)

        workout = Workout(muscle_group)
        db.session.add(workout)
        db.session.commit()

        return success_response(workout.serialize(), 201)


@app.route('/workouts/<int:workout_id>/', methods=['GET', 'POST', 'DELETE'])
def workout(workout_id):
    """
    Handle retrieving, deleting, or updating a single workout.
    """
    workout = Workout.query.filter_by(id=workout_id).first()
    if workout is None:
        return failure_response('Workout does not exist', 400)

    if request.method == 'GET':
        return success_response(workout.serialize())
    elif request.method == 'POST':
        body = json.loads(request.data)
        workout.muscle_group = body.get('muscle_group', workout.muscle_group)
        db.session.commit()
        return success_response(workout.serialize())
    elif request.method == 'DELETE':
        db.session.delete(workout)
        db.session.commit()
        return success_response(workout.serialize())


# Exercises


@app.route('/exercises/<int:exercise_id>/', methods=['GET', 'POST', 'DELETE'])
def exercise(exercise_id):
    """
    Handle retrieving, deleting, or updating a single exercises.

    """
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if exercise is None:
        return failure_response('Exercise does not exist', 400)

    if request.method == 'GET':
        return success_response(exercise.serialize())
    elif request.method == 'POST':
        body = json.loads(request.data)
        exercise.exercise_name = body.get(
            'exercise_name', exercise.exercise_name)
        exercise.muscle = body.get('muscle', exercise.muscle)
        db.session.commit()
        return success_response(exercise.serialize())
    elif request.method == 'DELETE':
        db.session.delete(exercise)
        db.session.commit()
        return success_response(exercise.serialize())


@app.route('/exercises/')
def get_exercises():
    """
    Get all Exercises (used for testing.)
    """
    exercises = [e.serialize() for e in Exercise.query.all()]
    return success_response({'exercises': exercises})


@app.route('/exercises/', methods=['POST'])
def create_unassigned_exercise():
    """
    Creates exercise that unassigned to a workout
    """
    body = json.loads(request.data)

    exercise_name = body.get("exercise_name")
    muscle = body.get('muscle')

    if exercise_name is None or muscle is None:
        return failure_response("Did not supply Exercise Name and/or Muscle.", 400)

    exercise = Exercise(exercise_name, muscle)
    db.session.add(exercise)
    db.session.commit()

    return success_response(exercise.serialize(), 201)


@app.route('/assign/exercises/<int:workout_id>/', methods=['POST'])
def create_assigned_exercise(workout_id):
    """
    Creates exercise that is assigned to a specified workout.
    """
    workout = Workout.query.filter_by(id=workout_id).first()

    if workout is None:
        return failure_response("Workout does Not Exist.", 400)

    body = json.loads(request.data)

    exercise_name = body.get("exercise_name")
    muscle = body.get('muscle')

    if exercise_name is None or muscle is None:
        return failure_response("Did not supply Exercise Name and/or Muscle.", 400)

    exercise = Exercise(exercise_name, muscle, workout_id)
    db.session.add(exercise)
    db.session.commit()

    return success_response(exercise.serialize(), 201)

# Sets


@app.route('/sets/<int:set_id>/', methods=['GET', 'DELETE', 'POST'])
def delete_set(set_id):
    """
    Handles getting, deleting, or updating a specified set.
    """
    set = Set.query.filter_by(id=set_id).first()
    if set is None:
        return failure_response("Set does not exist.", 400)

    if request.method == 'GET':
        return success_response(set.serialize())
    elif request.method == 'POST':
        body = json.loads(request.data)
        set.weight = body.get('weight', set.weight)
        set.repetitions = body.get('reps', set.repetitions)
        db.session.commit()
        return success_response(set.serialize())
    elif request.method == 'DELETE':
        db.session.delete(set)
        db.session.commit()
        return success_response(set.serialize())


@app.route('/sets/', methods=['POST'])
def create_unassigned_set():
    """
    Creates set that unassigned to a exercise.
    """
    body = json.loads(request.data)

    weight = body.get('weight')
    reps = body.get('reps')

    if weight is None or reps is None:
        return failure_response('Did not supply weight and/or number of reps.', 400)

    set = Set(weight, reps)
    db.session.add(set)
    db.session.commit()

    return success_response(set.serialize(), 201)


@app.route('/assign/sets/<int:exercise_id>/', methods=['POST'])
def create_assigned_set(exercise_id):
    """
    Creates set that is assigned to a specified exercise.
    """
    exercise = Exercise.query.filter_by(id=exercise_id).first()
    if exercise is None:
        return failure_response("Exercise does not exist.")

    body = json.loads(request.data)

    weight = body.get('weight')
    reps = body.get('reps')

    if weight is None or reps is None:
        return failure_response('Did not supply weight and/or number of reps.', 400)

    set = Set(weight, reps, exercise_id)
    db.session.add(set)
    db.session.commit()

    return success_response(set.serialize(), 201)

# Assigning


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
