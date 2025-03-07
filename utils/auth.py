from utils.utils import get_current_user
from flask import abort


def check_user():
    user = get_current_user()
    if user is None:
        abort(
            401,
            "Unauthorized"
        )
    return user


def check_is_site_owner():
    user = check_user()
    if not user.is_admin:
        abort(
            401,
            "Unauthorized"
        )


def check_is_team_member(team_id):
    user = check_user()
    matching_teams = [ t for t in user.teams if t.team_id == team_id ]
    if len(matching_teams) == 0:
        abort(401, "Unauthorized")
    return user


def check_is_team_owner(team_id):
    user = get_current_user()
    matching_teams = [ t for t in user.teams if t.team_id == team_id and t.is_owner ]
    if len(matching_teams) == 0:
        abort(401, "Unauthorized")
    return user

def check_is_team_or_site_owner(team_id):
    user = get_current_user()

    if not user.is_admin:
        matching_teams = [ t for t in user.teams if t.team_id == team_id and t.is_owner ]
        if len(matching_teams) == 0:
            abort(401, "Unauthorized")
        return user
    else:
        return user
