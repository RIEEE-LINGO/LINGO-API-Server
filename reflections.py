from flask import abort
from config import db
from lingo.models import Reflection, reflection_schema, reflections_schema
from utils import get_current_user

def check_reflection_security(user):
    if not user:
        abort(
            401,
            "Unauthorized"
        )

    # Add other rules for user checking here
    # TODO


def get_all(word_id, filter = "onlyActive"):
    check_reflection_security(get_current_user())

    if filter.lower() == "onlyactive":
        reflections_for_word = Reflection.query.where(Reflection.word_id == word_id, Reflection.active == True).all()
        return reflections_schema.dump(reflections_for_word)
    elif filter.lower() == "onlydeleted":
        reflections_for_word = Reflection.query.where(Reflection.word_id == word_id, Reflection.active == False).all()
        return reflections_schema.dump(reflections_for_word)
    else:
        reflections_for_word = Reflection.query.where(Reflection.word_id == word_id).all()
        return reflections_schema.dump(reflections_for_word)


def get(word_id, reflection_id):
    check_reflection_security(get_current_user())

    reflection = Reflection.query.where(Reflection.id == reflection_id, Reflection.word_id == word_id).one_or_none()

    if reflection is not None:
        return reflection_schema.dump(reflection)
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} for word with id {word_id} not found"
        )


def create(reflection):
    check_reflection_security(get_current_user())

    new_reflection = reflection_schema.load(reflection, session=db.session)
    db.session.add(new_reflection)
    db.session.commit()
    return reflection_schema.dump(new_reflection), 201


def update(word_id, reflection_id, reflection):
    check_reflection_security(get_current_user())

    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_reflection = Reflection.query.where(Reflection.id == reflection_id, Reflection.word_id == word_id).one_or_none()
    if existing_reflection:
        update_reflection = reflection_schema.load(reflection, session=db.session)
        db.session.merge(existing_reflection)
        db.session.commit()
        return reflection_schema.dump(existing_reflection), 201
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} for word with id {word_id} not found"
        )


def delete(word_id, reflection_id):
    check_reflection_security(get_current_user())

    existing_reflection = Reflection.query.where(Reflection.id == reflection_id, Reflection.word_id == word_id).one_or_none()
    if existing_reflection:
        existing_reflection.active = False
        db.session.merge(existing_reflection)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} for word with id {word_id} not found"
        )
