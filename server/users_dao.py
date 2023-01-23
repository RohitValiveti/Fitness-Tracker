"""
Data Access Object File for User Model.
"""
from db import db, User


def get_user_by_email(email):
    """
    Returns a user object from the database given an email
    """
    return User.query.filter(User.email == email).first()


def get_user_by_session_token(session_token):
    """
    Returns a user object from the database given a session token
    """
    return User.query.filter(User.session_token == session_token).first()


def get_user_by_update_token(update_token):
    """
    Returns a user object from the database given an update token
    """
    return User.query.filter(User.update_token == update_token).first()


def verify_credentials(email, password):
    """
    Returns true if the credentials match, otherwise returns false.
    If there is a match, also return the user.
    """
    user = get_user_by_email(email)

    if user is None:
        return False, None

    # If password is not correct, first return element is False
    return user.verify_password(password), user


def create_user(email, password):
    """
    Creates a User object in the database, if User with email does not exist yet.

    Returns if creation was successful, and the User object
    """
    user = get_user_by_email(email)
    if user is not None:
        return False, user

    new_user = User(email, password)
    db.session.add(new_user)
    db.session.commit()

    return True, new_user


def renew_session(update_token):
    """
    Renews a user's session token

    Returns the User object
    """
    opt_user = get_user_by_update_token(update_token)

    if opt_user is None:
        return False, None

    opt_user.renew_session()
    db.session.commit()

    return True, opt_user
