from flask import abort
from config import db
from lingo.models import User, user_schema, users_schema


def get_all():
    users = User.query.all()
    return users_schema.dump(users)


def get(user_id):
    user = User.query.where(User.id == user_id).one_or_none()

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(
            404, f"User with id {user_id} not found"
        )


def create(user):
    new_user = user_schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


def update(user_id, user):
    existing_user = User.query.where(User.id == user_id).one_or_none()
    if existing_user:
        update_user = user_schema.load(user, session=db.session)
        existing_user.first_name = update_user.first_name
        existing_user.last_name = update_user.last_name
        existing_user.email = update_user.email
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(
            404,
            f"User with id {user_id} not found"
        )
