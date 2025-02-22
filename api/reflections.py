from datetime import datetime, UTC

from flask import abort
from config import db
from lingo.models import Reflection, reflection_schema, reflections_schema, Word, reflection_update_schema
from sqlalchemy import select
from utils.auth import check_is_team_owner, check_is_team_member


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Reflection.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Reflection.is_active == False)
    else:
        return query


def get_all(word_id, filter="onlyActive"):
    word_id = int(word_id)
    word_query = select(Word).where(Word.id == word_id)
    word_result = db.session.scalar(word_query)

    check_is_team_member(word_result.team_id)

    query = add_filter(select(Reflection).where(Reflection.word_id == word_id), filter)
    result = db.session.scalars(query).all()
    return reflections_schema.dump(result)


def get(reflection_id):
    query = select(Reflection).where(Reflection.id == reflection_id)
    result = db.session.scalar(query)

    if result is not None:
        word_query = select(Word).where(Word.id == result.word_id)
        word_result = db.session.scalar(word_query)
        check_is_team_member(word_result.team_id)
        return reflection_schema.dump(result)
    else:
        abort(
            404,
            f"Meaning with id {reflection_id} not found"
        )


def create(word_id, reflection):
    word_id = int(word_id)
    word_query = select(Word).where(Word.id == word_id)
    word_result = db.session.scalar(word_query)

    check_is_team_member(word_result.team_id)

    if "word_id" not in reflection:
        reflection["word_id"] = word_id
    new_reflection = reflection_schema.load(reflection, session=db.session)
    new_reflection.created_at = datetime.now(UTC)
    new_reflection.updated_at = datetime.now(UTC)
    db.session.add(new_reflection)
    db.session.commit()

    reflection_update = reflection_update_schema.load({
        "reflection_id": new_reflection.id,
        "update_type": "C",
        "value": new_reflection.reflection}, session=db.session)
    reflection_update.created_at = datetime.now(UTC)
    db.session.add(reflection_update)
    db.session.commit()

    return reflection_schema.dump(new_reflection), 201


def update(reflection_id, reflection):
    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_reflection = Reflection.query.where(Reflection.id == reflection_id).one_or_none()
    if existing_reflection:
        word_id = int(existing_reflection.word_id)
        word_query = select(Word).where(Word.id == word_id)
        word_result = db.session.scalar(word_query)

        check_is_team_owner(word_result.team_id)

        update_reflection = reflection_schema.load(reflection, session=db.session)
        existing_reflection.updated_at = datetime.now(UTC)
        db.session.merge(existing_reflection)
        db.session.commit()

        reflection_update = reflection_update_schema.load({
            "reflection_id": update_reflection.id,
            "update_type": "U",
            "value": update_reflection.reflection}, session=db.session)
        reflection_update.created_at = datetime.now(UTC)
        db.session.add(reflection_update)
        db.session.commit()

        return reflection_schema.dump(existing_reflection), 201
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} not found"
        )


def delete(reflection_id):
    existing_reflection = Reflection.query.where(Reflection.id == reflection_id).one_or_none()
    if existing_reflection:
        word_id = int(existing_reflection.word_id)
        word_query = select(Word).where(Word.id == word_id)
        word_result = db.session.scalar(word_query)

        check_is_team_owner(word_result.team_id)

        existing_reflection.is_active = False
        existing_reflection.updated_at = datetime.now(UTC)
        db.session.merge(existing_reflection)
        db.session.commit()

        reflection_update = reflection_update_schema.load({
            "reflection_id": existing_reflection.id,
            "update_type": "D",
            "value": existing_reflection.reflection}, session=db.session)
        reflection_update.created_at = datetime.now(UTC)
        db.session.add(reflection_update)
        db.session.commit()

        return reflection_schema.dump(existing_reflection), 200
    else:
        abort(
            404,
            f"Reflection with id {reflection_id} not found"
        )
