from flask import abort
from config import db
from lingo.models import User, Team, user_schema, users_schema
from sqlalchemy import select
from utils.auth import check_is_team_owner, check_is_team_member, check_user, check_is_site_owner, \
    check_is_team_or_site_owner


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(User.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(User.is_active == False)
    else:
        return query


def get_all(filter = "onlyActive"):
    check_is_site_owner()

    query = add_filter(select(User).order_by(User.email), filter)
    result = db.session.scalars(query).all()
    return users_schema.dump(result)


def get_all_for_team(team_id, filter = "onlyActive"):
    check_is_team_owner(team_id)

    query = add_filter(select(User).join(User.teams).where(Team.id == team_id).order_by(User.email), filter)
    result = db.session.scalars(query).all()
    return users_schema.dump(result)


def get(user_id):
    query = select(User).where(User.id == user_id)
    result = db.session.scalar(query)

    if result is not None:
        check_is_team_or_site_owner(result.team_id)
        return user_schema.dump(result)
    else:
        abort(
            404, f"User with id {user_id} not found"
        )


def get_my_user_info():
    user = check_user()
    return user_schema.dump(user)


def update_current_team(body):
    existing_user = check_user()

    if existing_user:
        existing_user.current_team_id = body['current_team_id']
        check_is_team_member(existing_user.current_team_id)
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(
            404,
            f"User with id {existing_user.id} not found"
        )


def create(user):
    new_user = user_schema.load(user, session=db.session)
    check_is_team_or_site_owner(new_user.team_id)
    db.session.add(new_user)
    db.session.commit()
    return user_schema.dump(new_user), 201


def update(user_id, user):
    existing_user = User.query.where(User.id == user_id).one_or_none()
    if existing_user:
        check_is_team_or_site_owner(existing_user.team_id)
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
