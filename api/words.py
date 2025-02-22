from flask import abort
from config import enable_api_security, db
from lingo.models import Word, word_schema, words_schema
from utils.utils import get_current_user
from sqlalchemy import select

def check_user():
    user = get_current_user()
    if user is None:
        abort(
            401,
            "Unauthorized"
        )
    return user


def check_word_security_view(team_id):
    user = check_user()
    # To view a word, the user should be a member of the team
    matching_teams = [ t for t in user.teams if t.team_id == team_id ]
    if len(matching_teams) == 0:
        abort(401, "Unauthorized")
    return user


def check_word_security_add(team_id):
    # To add a word, the user should be a member of the team
    # Since this is the same rule as viewing words, we just use that function
    return check_word_security_view(team_id)


def check_word_security_update(team_id):
    user = get_current_user()
    # To change a word, the user should be the owner of the team
    matching_teams = [ t for t in user.teams if t.team_id == team_id and t.is_owner ]
    if len(matching_teams) == 0:
        abort(401, "Unauthorized")
    return user


def check_word_security_delete(team_id):
    # To delete a word, the user should be the owner of the team
    # Since this is the same rule as updating words, we just use that function
    return check_word_security_update(team_id)


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Word.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Word.is_active == False)
    else:
        return query


def get_all_for_team(team_id, filter = "onlyActive"):
    team_id = int(team_id)
    check_word_security_view(team_id)

    query = add_filter(select(Word).where(Word.team_id == team_id), filter)
    result = db.session.scalars(query).all()
    return words_schema.dump(result)


def get(word_id):
    word_id = int(word_id)
    query = select(Word).where(Word.id == word_id)
    result = db.session.scalar(query)

    if result is not None:
        check_word_security_view(result.team_id)
        return word_schema.dump(result)
    else:
        abort(
            404, f"Word with id {word_id} not found"
        )


def create(word):
    new_word = word_schema.load(word, session=db.session)

    check_word_security_add(new_word.team_id)

    db.session.add(new_word)
    db.session.commit()
    return word_schema.dump(new_word), 201


def create_for_team(team_id, word):
    team_id = int(team_id)
    check_word_security_add(team_id)

    if "team_id" not in word:
        word["team_id"] = team_id

    new_word = word_schema.load(word, session=db.session)
    db.session.add(new_word)
    db.session.commit()
    return word_schema.dump(new_word), 201


def update(word_id, word):
    word_id = int(word_id)
    existing_word = Word.query.where(Word.id == word_id).one_or_none()
    if existing_word:
        if "id" not in word:
            word["id"] = word_id
        if "team_id" not in word:
            word["team_id"] = existing_word.team_id
        update_word = word_schema.load(word, session=db.session)
        check_word_security_update(existing_word.team_id)
        db.session.merge(existing_word)
        db.session.commit()
        return word_schema.dump(existing_word), 201
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )


def delete(word_id):
    word_id = int(word_id)
    existing_word = Word.query.where(Word.id == word_id).one_or_none()
    if existing_word:
        check_word_security_delete(existing_word.team_id)
        existing_word.is_active = False
        db.session.merge(existing_word)
        db.session.commit()
        return True, 200
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )
