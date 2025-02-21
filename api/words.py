from flask import abort
from config import enable_api_security, db
from lingo.models import Word, word_schema, words_schema
from utils.utils import get_current_user
from sqlalchemy import select

def check_word_security():
    user = get_current_user()
    if user is None:
        abort(
            401,
            "Unauthorized"
        )

    # Add other rules for user checking here
    # TODO

    return user



def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Word.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Word.is_active == False)
    else:
        return query


def get_all(filter = "onlyActive"):
    check_word_security()

    query = add_filter(select(Word), filter)
    result = db.session.scalars(query).all()
    return words_schema.dump(result)


def get_all_for_team(team_id, filter = "onlyActive"):
    check_word_security()

    query = add_filter(select(Word).where(Word.team_id == team_id), filter)
    result = db.session.scalars(query).all()
    return words_schema.dump(result)


def get(word_id):
    check_word_security()

    query = select(Word).where(Word.id == word_id)
    result = db.session.scalar(query)

    if result is not None:
        return word_schema.dump(result)
    else:
        abort(
            404, f"Word with id {word_id} not found"
        )


def create(word):
    check_word_security()

    new_word = word_schema.load(word, session=db.session)
    db.session.add(new_word)
    db.session.commit()
    return word_schema.dump(new_word), 201


def create_for_team(team_id, word):
    check_word_security()

    if "team_id" not in word:
        word["team_id"] = team_id

    new_word = word_schema.load(word, session=db.session)
    db.session.add(new_word)
    db.session.commit()
    return word_schema.dump(new_word), 201


def update(word_id, word):
    check_word_security()

    existing_word = Word.query.where(Word.id == word_id).one_or_none()
    if existing_word:
        if "id" not in word:
            word["id"] = word_id
        update_word = word_schema.load(word, session=db.session)
        db.session.merge(existing_word)
        db.session.commit()
        return word_schema.dump(existing_word), 201
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )


def delete(word_id):
    check_word_security()

    existing_word = Word.query.where(Word.id == word_id).one_or_none()
    if existing_word:
        existing_word.is_active = False
        db.session.merge(existing_word)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )
