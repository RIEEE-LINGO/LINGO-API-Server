from flask import abort
from config import enable_api_security, db
from lingo.models import Team, team_schema, teams_schema


def get_all():
    teams = Team.query.all()
    return teams_schema.dump(teams)


def get(team_id):
    team = Team.query.where(Team.id == team_id).one_or_none()

    if team is not None:
        return team_schema.dump(team)
    else:
        abort(
            404, f"Team with id {team_id} not found"
        )


def create(team):
    new_team = team_schema.load(team, session=db.session)
    db.session.add(new_team)
    db.session.commit()
    return team_schema.dump(new_team), 201


def update(team_id, team):
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
