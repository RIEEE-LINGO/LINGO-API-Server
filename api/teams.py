from flask import abort
from config import db
from lingo.models import Team, team_schema, teams_schema, TeamMember, User
from sqlalchemy import select
from utils.utils import get_current_user
from utils.auth import check_is_team_owner, check_is_team_member, check_user, check_is_site_owner


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Team.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Team.is_active == False)
    else:
        return query


def get_all(filter = "onlyActive"):
    check_is_site_owner()

    query = add_filter(select(Team), filter)
    result = db.session.scalars(query).all()
    return teams_schema.dump(result)


def get(team_id):
    check_is_team_member()

    query = select(Team).where(Team.id == team_id)
    result = db.session.execute(query).one_or_none()

    if result is not None:
        return team_schema.dump(result[0])
    else:
        abort(
            404, f"Team with id {team_id} not found"
        )


def get_teams_for_user(user_id, filter = "onlyActive"):
    check_user()

    query = add_filter(select(Team).join(Team.team_members).where(TeamMember.user_id == user_id), filter)
    result = db.session.scalars(query).all()
    return teams_schema.dump(result)


def get_my_teams(filter = "onlyActive"):
    user = check_user()

    query = add_filter(select(Team).join(Team.team_members).where(TeamMember.user_id == user.id), filter)
    result = db.session.scalars(query).all()
    return teams_schema.dump(result)


def create(team):
    check_is_site_owner()

    new_team = team_schema.load(team, session=db.session)
    db.session.add(new_team)
    db.session.commit()
    return team_schema.dump(new_team), 201


def update(team_id, team):
    check_is_team_owner()

    existing_team = Team.query.where(Team.id == team_id).one_or_none()
    if existing_team:
        update_team = team_schema.load(team, session=db.session)
        existing_team.team_name = update_team.team_name
        existing_team.team_owner = update_team.team_owner
        existing_team.is_active = update_team.is_active
        db.session.merge(existing_team)
        db.session.commit()
        return team_schema.dump(existing_team), 201
    else:
        abort(
            404,
            f"Team with id {team_id} not found"
        )


def delete(team_id):
    check_is_team_owner()

    existing_team = Team.query.where(Team.id == team_id).one_or_none()
    if existing_team:
        existing_team.active = False
        db.session.merge(existing_team)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Team with id {team_id} not found"
        )