import json
import os
import datetime
from flask import Flask, request
from db import db, User, Workout, Exercise, Set, Health_File
import users_dao
import boto3
from werkzeug.utils import secure_filename

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


def authenticate(request):
    """
    Authenticates a user via their session token.
    Returns False if unable to authenticate.
    """
    success, token = extract_token(request)

    if not success:
        return failure_response('Could not extract token.', 400)

    user = users_dao.get_user_by_session_token(token)
    if user is None or not user.verify_session_token(token):
        return failure_response('Invalid session token.', 400)

    return


def extract_token(request):
    """
    Helper function that extracts the token from the header of a request
    """
    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return False, "Missing Authorization header"

    # Header formats as "Authorization": Bearer <Token>
    bearer_token = auth_header.replace("Bearer ", "").strip()
    if bearer_token is None or not bearer_token:
        return False, "Invalid authorization header"

    return True, bearer_token

# ENDPOINTS

# Admin


@app.route('/admin/delete/')
def delete_tables():
    """
    Reset all table content to empty.
    """
    Workout.__table__.drop(db.engine)
    Exercise.__table__.drop(db.engine)
    Set.__table__.drop(db.engine)
    db.create_all()
    return success_response({"message": "deleted all tables."})


@app.route('/admin/users/')
def get_users():
    """
    Return all registered users. 
    """
    users = [u.simple_serialize() for u in User.query.all()]
    return success_response({'users': users})

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

        workout_id = body.get('workout_id')
        if workout_id is not None:
            workout = Workout.query.filter_by(id=workout_id).first()
            if workout is None:
                return failure_response('Workout does not exist', 400)
            exercise.workout_id = workout_id

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

        exercise_id = body.get('exercise_id')
        if exercise_id is not None:
            exercise = Exercise.query.filter_by(id=exercise_id).first()
            if exercise is None:
                return failure_response("Exercise does not exist.", 400)
            set.exercise_id = exercise_id
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

# User Management


@app.route("/register/", methods=["POST"])
def register():
    """
    Register User with given email and password in body.
    """
    body = json.loads(request.data)

    email = body.get('email')
    password = body.get('password')

    if email is None or password is None:
        return failure_response('Did not supply email and/or password.', 400)

    success, user = users_dao.create_user(email, password)

    if not success:
        return failure_response('This email is already associated with a created account.', 400)

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    }, 201)


@app.route("/login/", methods=["POST"])
def login():
    """
    Log user in with given email and password in body.
    Returns session token, expiration, and update token.
    """
    body = json.loads(request.data)

    email = body.get('email')
    password = body.get('password')

    if email is None or password is None:
        return failure_response('Did not supply email and/or password.')

    success, user = users_dao.verify_credentials(email, password)
    if user is None:
        return failure_response('Email is not assocated with account', 400)

    if not success:
        return failure_response('password not correct for entered email.', 400)

    if user.session_token == "":
        user.renew_session()
        db.session.commit()

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })


@app.route("/logout/", methods=["POST"])
def logout():
    """
    Log user out.
    """
    success, response = extract_token(request)
    if not success:
        return failure_response(response, 400)

    user = users_dao.get_user_by_session_token(response)

    if user is None or not user.verify_session_token(response):
        return failure_response('Invalid session token.', 400)

    user.session_token = ''
    user.session_expiration = datetime.datetime.now()
    user.update_token = ''
    db.session.commit()

    return success_response({'message': 'you have been logged out'})


@app.route("/session/", methods=["POST"])
def update_session():
    """
    Update user session. Return session token, expiration, and update token.
    """
    success, response = extract_token(request)

    if not success:
        return failure_response(response, 400)

    renew_success, user = users_dao.renew_session(response)

    if not renew_success or not user.verify_update_token(response):
        return failure_response('Invalid update token.', 400)

    return success_response({
        "session_token": user.session_token,
        "session_expiration": str(user.session_expiration),
        "update_token": user.update_token
    })


# Users


@app.route('/users/<int:user_id>/')
def get_user(user_id):
    """
    Get user with specified id.
    The user requested must be logged in (have proper session token).
    """
    success, token = extract_token(request)

    if not success:
        return failure_response('Could not extract token.', 400)

    user = users_dao.get_user_by_session_token(token)
    if user is None or not user.verify_session_token(token):
        return failure_response('Invalid session token.', 400)

    return success_response(user.serialize())


@app.route('/users/friend/<int:friend_id>/', methods=['POST'])
def friend_user(friend_id):
    """
    Friend users together
    """

    success, token = extract_token(request)

    if not success:
        return failure_response('Could not extract token.', 400)

    user = users_dao.get_user_by_session_token(token)
    if user is None or not user.verify_session_token(token):
        return failure_response('Invalid session token.', 400)

    friend = User.query.filter_by(id=friend_id).first()

    if friend is None:
        return failure_response('user with this id does not exist', 400)

    user.friends.append(friend)
    db.session.commit()

    return success_response(friend.simple_serialize())


@app.route('/users/files/', methods=['GET', 'POST'])
def files():
    """
    Gets all files of user or uploads files for a user.
    """
    success, token = extract_token(request)

    if not success:
        return failure_response('Could not extract token.', 400)

    user = users_dao.get_user_by_session_token(token)
    if user is None or not user.verify_session_token(token):
        return failure_response('Invalid session token.', 400)

    if request.method == 'GET':
        files = [f.basic_serialize() for f in user.health_files]
        return success_response({'health_files': files})
    elif request.method == 'POST':
        name = request.form.get("name")
        file = request.files.get("content")
        user_id = user.id
        if name is None or file is None:
            return failure_response('Did not supply data.', 400)

        s3 = boto3.resource("s3")
        bucket = s3.Bucket("rv-fitness-tracker")
        filename = secure_filename(file.filename)
        bucket.put_object(Key=filename, Body=file)
        s3_client = boto3.client("s3")
        url = s3_client.generate_presigned_url(
            "get_object", Params={"Bucket": "rv-fitness-tracker", "Key": filename}, ExpiresIn=300
        )

        health_file = Health_File(name, url, user_id)
        db.session.add(health_file)
        db.session.commit()
        return success_response(health_file.serialize(), 201)


@app.route('/users/files/<int:file_id>/')
def get_file(file_id):
    """
    Gets specified file of a user.
    """

    success, token = extract_token(request)

    if not success:
        return failure_response('Could not extract token.', 400)

    user = users_dao.get_user_by_session_token(token)
    if user is None or not user.verify_session_token(token):
        return failure_response('Invalid session token.', 400)

    file = Health_File.query.filter_by(id=file_id).first()

    if file is None:
        return failure_response('File does not exist.', 400)

    if file.user_id != user.id:
        return failure_response('Denied Access.', 400)

    return success_response(file.simple_serialize())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
