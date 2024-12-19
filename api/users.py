from flask import abort
from config import enable_api_security, db
from lingo.models import User, Team, user_schema, users_schema
from utils.utils import get_current_user
from sqlalchemy import select

def check_user_security():
    if enable_api_security:
        user = get_current_user()
        if not user:
            abort(
                401,
                "Unauthorized"
            )

        # Add other rules for user checking here
        # TODO


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(User.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(User.is_active == False)
    else:
        return query


def get_all(filter = "onlyActive"):
    check_user_security()

    query = add_filter(select(User).order_by(User.email), filter)
    result = db.session.scalars(query).all()
    return users_schema.dump(result)


def get_all_for_team(team_id, filter = "onlyActive"):
    check_user_security()

    query = add_filter(select(User).join(User.teams).where(Team.id == team_id).order_by(User.email), filter)
    result = db.session.scalars(query).all()
    return users_schema.dump(result)


def get(user_id):
    check_user_security()

    query = select(User).where(User.id == user_id)
    result = db.session.scalar(query)

    if result is not None:
        return user_schema.dump(result)
    else:
        abort(
            404, f"User with id {user_id} not found"
        )


def create(user):
    check_user_security()

    new_user = user_schema.load(user, session=db.session)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


def update(user_id, user):
    check_user_security()

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
