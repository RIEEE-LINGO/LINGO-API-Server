from config import app, db
from lingo.models import User, Word, Project, Team, TeamMember
from datetime import datetime

def get_timestamp():
    return datetime.utcnow

USERS = [
    {
        "first_name": "Mark",
        "last_name": "Hills",
        "email": "hillsma@appstate.edu",
    },
    {
        "first_name": "Elle",
        "last_name": "Russell",
        "email": "russellem@appstate.edu",
    },
    {
        "first_name": "Kim",
        "last_name": "Bourne",
        "email": "bournekd@appstate.edu",
    }
]

PROJECTS = [
    {
        "name": "Prototype Project"
    }
]

TEAMS = [
    {
        "name": "Prototype Team"
    }
]

TEAM_MEMBERS = [
    {
        "id": 1,
        "email": "hillsma@appstate.edu"
    },
    {
        "id": 2,
        "email": "russellem@appstate.edu"
    },
    {
        "id": 3,
        "email": "bournekd@appstate.edu",
    }
]

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    for data in USERS:
        new_user = User(
            first_name = data.get("first_name"), 
            last_name = data.get("last_name"),
            email = data.get("email")
        )
        users.append(new_user)
        db.session.add(new_user)
    db.session.commit()

    # NOTE: We need to update this to use the actual IDs
    # This is fragile to changes in IDs assigned by the db.
    for data in PROJECTS:
        new_project = Project(
            project_name = data.get("name"),
            project_owner = 1,
            is_active = True
        )
        db.session.add(new_project)

    for data in TEAMS:
        new_team = Team(
            project_id = 1,
            team_name = data.get("name"),
            is_active = True
        )
        db.session.add(new_team)

    for data in TEAM_MEMBERS:
        new_member = TeamMember(
            team_id = 1,
            user_id = data.get("id"),
            email = data.get("email"),
            is_owner = True
        )
        db.session.add(new_member)

    db.session.commit()

