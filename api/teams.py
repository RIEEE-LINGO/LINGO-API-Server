from flask import abort
from config import enable_api_security, db
from lingo.models import Team, team_schema, teams_schema, TeamMember, User
from sqlalchemy import select
from utils.utils import get_current_user


def check_team_security():
    if enable_api_security:
        user = get_current_user()
        if not user:
            abort(
                401,
                "Unauthorized"
            )

        # Add other rules for user checking here
        # TODO


def get_all():
    check_team_security()

    query = select(Team)
    result = db.session.scalars(query).all()
    return teams_schema.dump(result)


def get(team_id):
    check_team_security()

    query = select(Team).where(Team.id == team_id)
    result = db.session.execute(query).one_or_none()

    if result is not None:
        return team_schema.dump(result[0])
    else:
        abort(
            404, f"Team with id {team_id} not found"
        )


def get_teams_for_user(user_id):
    check_team_security()

    query = select(Team).join(Team.team_members).where(TeamMember.user_id == user_id)
    result = db.session.scalars(query).all()
    return teams_schema.dump(result)


def create(team):
    check_team_security()

    new_team = team_schema.load(team, session=db.session)
    db.session.add(new_team)
    db.session.commit()
    return team_schema.dump(new_team), 201


def update(team_id, team):
    check_team_security()

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
    check_team_security()

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