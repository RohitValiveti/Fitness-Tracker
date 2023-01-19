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

####### ENDPOINTS

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
        return success_response(workout.serialize(), 200)
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass

# Exercises


@app.route('/exercises/<int:exercise_id>/', methods=['GET', 'POST', 'DELETE'])
def exercise(exercise_id):
    """
    Handle retrieving, deleting, or updating a single exercises.

    """
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@app.route('/exercises/', methods=['POST'])
def create_unassigned_exercise():
    """
    Creates exercise that unassigned to a workout
    """


@app.route('/exercises/:workout_id/', methods=['POST'])
def create_assigned_exercise(exercise_id):
    """
    Creates exercise that is assigned to a specified workout.
    """

# Sets


@app.route('/sets/<int:set_id>/', methods=['GET', 'DELETE', 'POST'])
def delete_set(set_id):
    """
    Handles getting, deleting, or updating a specified set.
    """
    if request.metho == 'GET':
        pass
    elif request.method == 'POST':
        pass
    elif request.method == 'DELETE':
        pass


@app.route('/sets/', methods=['POST'])
def create_unassigned_set():
    """
    Creates set that unassigned to a exercise.
    """


@app.route('/sets/:set_id/', methods=['POST'])
def create_assigned_set(set_id):
    """
    Creates set that is assigned to a specified exercise.
    """

# Assigning


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
