from flask import abort
from config import enable_api_security, db
from lingo.models import Reflection, reflection_schema, reflections_schema
from utils.utils import get_current_user
from sqlalchemy import select


def check_reflection_security():
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
        return query.where(Reflection.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Reflection.is_active == False)
    else:
        return query


def get_all(word_id, filter="onlyActive"):
    check_reflection_security()

    query = add_filter(select(Reflection).where(Reflection.word_id == word_id), filter)
    result = db.session.scalars(query).all()
    return reflections_schema.dump(result)


def get(reflection_id):
    check_reflection_security()

    query = select(Reflection).where(Reflection.id == reflection_id)
    result = db.session.scalar(query)

    if result is not None:
        return reflection_schema.dump(result)
    else:
        abort(
            404,
            f"Meaning with id {reflection_id} not found"
        )


def create(word_id, reflection):
    check_reflection_security()

    if "word_id" not in reflection:
        reflection["word_id"] = word_id
    new_reflection = reflection_schema.load(reflection, session=db.session)
    db.session.add(new_reflection)
    db.session.commit()
    return reflection_schema.dump(new_reflection), 201


def update(reflection_id, reflection):
    check_reflection_security()

    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_reflection = Reflection.query.where(Reflection.id == reflection_id).one_or_none()
    if existing_reflection:
        update_reflection = reflection_schema.load(reflection, session=db.session)
        db.session.merge(existing_reflection)
        db.session.commit()
        return reflection_schema.dump(existing_reflection), 201
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} not found"
        )


def delete(reflection_id):
    check_reflection_security()

    existing_reflection = Reflection.query.where(Reflection.id == reflection_id).one_or_none()
    if existing_reflection:
        existing_reflection.active = False
        db.session.merge(existing_reflection)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} not found"
        )
