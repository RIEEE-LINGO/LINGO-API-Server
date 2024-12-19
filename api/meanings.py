from flask import abort
from config import enable_api_security, db
from lingo.models import Meaning, meaning_schema, meanings_schema
from utils.utils import get_current_user
from sqlalchemy import select

def check_meaning_security():
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
        return query.where(Meaning.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Meaning.is_active == False)
    else:
        return query


def get_all(word_id, filter="onlyActive"):
    check_meaning_security()

    query = add_filter(select(Meaning).where(Meaning.word_id == word_id), filter)
    result = db.session.scalars(query).all()
    return meanings_schema.dump(result)


def get(meaning_id):
    check_meaning_security()

    query = select(Meaning).where(Meaning.id == meaning_id)
    result = db.session.scalar(query)

    if result is not None:
        return meaning_schema.dump(result)
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} not found"
        )


def create(word_id, meaning):
    check_meaning_security()

    if "word_id" not in meaning:
        meaning["word_id"] = word_id
    new_meaning = meaning_schema.load(meaning, session=db.session)
    db.session.add(new_meaning)
    db.session.commit()
    return meaning_schema.dump(new_meaning), 201


def update(word_id, meaning_id, meaning):
    check_meaning_security()

    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_meaning = Meaning.query.where(Meaning.id == meaning_id, Meaning.word_id == word_id).one_or_none()
    if existing_meaning:
        update_meaning = meaning_schema.load(meaning, session=db.session)
        db.session.merge(existing_meaning)
        db.session.commit()
        return meaning_schema.dump(existing_meaning), 201
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} for word with id {word_id} not found"
        )


def delete(word_id, meaning_id):
    check_meaning_security()

    existing_meaning = Meaning.query.where(Meaning.id == meaning_id, Meaning.word_id == word_id).one_or_none()
    if existing_meaning:
        existing_meaning.active = False
        db.session.merge(existing_meaning)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} for word with id {word_id} not found"
        )
