from typing import Optional
from flask import request
from firebase_admin.auth import verify_id_token, get_user, UserRecord
from lingo.models import User, TeamMember
from config import db


# Note: Based on code from https://pradyothkukkapalli.com/tech/firebase-auth-client-and-backend/
# The original code just made sure the token was proper, but here we also load
# the associated user so we can tell which user is accessing this data. This is
# needed to ensure the user has permission to access the data they are trying to
# retrieve, e.g., that the words are from a project they are part of.
def get_current_user(create_missing_user=True, add_to_default_team=True) -> Optional[str]:
    # Return None if no Authorization header.
    if "Authorization" not in request.headers:
        return None
    authorization = request.headers["Authorization"]

    # Authorization header format is "Bearer <token>".
    # This matches OAuth 2.0 spec:
    # https://www.rfc-editor.org/rfc/rfc6750.txt.
    if not authorization.startswith("Bearer "):
        return None

    token = authorization.split("Bearer ")[1]
    try:
        # Verify that the token is valid.
        result = verify_id_token(token)

        # Return the user info object for the authenticated user.
        user_info = get_user(result["uid"])

        # Retrieve this user from the database
        user = User.query.where(User.email == user_info.email).one_or_none()

        if not user:
            if create_missing_user:
                user = User(email=user_info.email)
                db.session.add(user)
                db.session.commit()

                if add_to_default_team:
                    teammate = TeamMember(user_id=user.id, team_id=1, email=user.email, is_owner=False)
                    db.session.add(teammate)
                    db.session.commit()

        # Return the user object, or None if there is no associated user
        return user
    except:
        return None