from datetime import datetime, UTC

from flask import abort
from config import db
from lingo.models import Meaning, meaning_schema, meanings_schema, Word, meaning_update_schema
from sqlalchemy import select
from utils.auth import check_is_team_owner, check_is_team_member


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Meaning.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Meaning.is_active == False)
    else:
        return query


def get_all(word_id, filter="onlyActive"):
    word_id = int(word_id)
    word_query = select(Word).where(Word.id == word_id)
    word_result = db.session.scalar(word_query)

    check_is_team_member(word_result.team_id)

    query = add_filter(select(Meaning).where(Meaning.word_id == word_id), filter)
    result = db.session.scalars(query).all()
    return meanings_schema.dump(result), 200


def get(meaning_id):
    query = select(Meaning).where(Meaning.id == meaning_id)
    result = db.session.scalar(query)

    if result is not None:
        word_query = select(Word).where(Word.id == result.word_id)
        word_result = db.session.scalar(word_query)
        check_is_team_member(word_result.team_id)

        return meaning_schema.dump(result), 200
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} not found"
        )


def create(word_id, meaning):
    word_id = int(word_id)
    word_query = select(Word).where(Word.id == word_id)
    word_result = db.session.scalar(word_query)

    check_is_team_member(word_result.team_id)

    if "word_id" not in meaning:
        meaning["word_id"] = word_id
    new_meaning = meaning_schema.load(meaning, session=db.session)
    new_meaning.created_at = datetime.now(UTC)
    new_meaning.updated_at = datetime.now(UTC)
    db.session.add(new_meaning)
    db.session.commit()

    meaning_update = meaning_update_schema.load({
        "meaning_id": new_meaning.id,
        "update_type": "C",
        "value": new_meaning.meaning}, session=db.session)
    meaning_update.created_at = datetime.now(UTC)
    db.session.add(meaning_update)
    db.session.commit()

    return meaning_schema.dump(new_meaning), 201


def update(meaning_id, meaning):
    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_meaning = Meaning.query.where(Meaning.id == meaning_id).one_or_none()
    if existing_meaning:
        word_id = int(existing_meaning.word_id)
        word_query = select(Word).where(Word.id == word_id)
        word_result = db.session.scalar(word_query)

        check_is_team_owner(word_result.team_id)

        update_meaning = meaning_schema.load(meaning, session=db.session)
        existing_meaning.updated_at = datetime.now(UTC)
        db.session.merge(existing_meaning)
        db.session.commit()

        meaning_update = meaning_update_schema.load({
            "meaning_id": update_meaning.id,
            "update_type": "U",
            "value": update_meaning.meaning}, session=db.session)
        meaning_update.created_at = datetime.now(UTC)
        db.session.add(meaning_update)
        db.session.commit()

        return meaning_schema.dump(existing_meaning), 201
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} not found"
        )


def delete(meaning_id):
    existing_meaning = Meaning.query.where(Meaning.id == meaning_id).one_or_none()
    if existing_meaning:
        word_id = int(existing_meaning.word_id)
        word_query = select(Word).where(Word.id == word_id)
        word_result = db.session.scalar(word_query)

        check_is_team_owner(word_result.team_id)

        existing_meaning.is_active = False
        existing_meaning.updated_at = datetime.now(UTC)
        db.session.merge(existing_meaning)
        db.session.commit()

        meaning_update = meaning_update_schema.load({
            "meaning_id": existing_meaning.id,
            "update_type": "D",
            "value": existing_meaning.meaning}, session=db.session)
        meaning_update.created_at = datetime.now(UTC)
        db.session.add(meaning_update)
        db.session.commit()

        return meaning_schema.dump(existing_meaning), 200
    else:
        abort(
            404,
            f"Meaning with id {meaning_id} not found"
        )
