from datetime import datetime, UTC

from flask import abort
from config import db
from lingo.models import Word, word_schema, words_schema, word_update_schema
from sqlalchemy import select
from utils.auth import check_is_team_owner, check_is_team_member


def add_filter(query, filter):
    if filter.lower() == "onlyactive":
        return query.where(Word.is_active == True)
    elif filter.lower() == "onlydeleted":
        return query.where(Word.is_active == False)
    else:
        return query


def get_all_for_team(team_id, filter = "onlyActive"):
    team_id = int(team_id)
    check_is_team_member(team_id)

    query = add_filter(select(Word).where(Word.team_id == team_id), filter)
    result = db.session.scalars(query).all()
    return words_schema.dump(result), 200


def get(word_id):
    word_id = int(word_id)
    query = select(Word).where(Word.id == word_id)
    result = db.session.scalar(query)

    if result is not None:
        check_is_team_member(result.team_id)
        return word_schema.dump(result), 200
    else:
        abort(
            404, f"Word with id {word_id} not found"
        )


def create(word):
    new_word = word_schema.load(word, session=db.session)
    new_word.created_at = datetime.now(UTC)
    new_word.updated_at = datetime.now(UTC)
    check_is_team_member(new_word.team_id)

    db.session.add(new_word)
    db.session.commit()

    word_update = word_update_schema.load({
        "word_id": new_word.id,
        "update_type": "C",
        "value": new_word.word}, session=db.session)
    word_update.created_at = datetime.now(UTC)
    db.session.add(word_update)
    db.session.commit()

    return word_schema.dump(new_word), 201


def create_for_team(team_id, word):
    team_id = int(team_id)
    check_is_team_member(team_id)

    if "team_id" not in word:
        word["team_id"] = team_id

    new_word = word_schema.load(word, session=db.session)
    new_word.created_at = datetime.now(UTC)
    new_word.updated_at = datetime.now(UTC)
    db.session.add(new_word)
    db.session.commit()

    word_update = word_update_schema.load({
        "word_id": new_word.id,
        "update_type": "C",
        "value": new_word.word}, session=db.session)
    word_update.created_at = datetime.now(UTC)
    db.session.add(word_update)
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
        check_is_team_owner(existing_word.team_id)
        existing_word.updated_at = datetime.now(UTC)
        db.session.merge(existing_word)
        db.session.commit()

        word_update = word_update_schema.load({
            "word_id": update_word.id,
            "update_type": "U",
            "value": update_word.word}, session=db.session)
        word_update.created_at = datetime.now(UTC)
        db.session.add(word_update)
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
        check_is_team_owner(existing_word.team_id)
        existing_word.is_active = False
        existing_word.updated_at = datetime.now(UTC)
        db.session.merge(existing_word)
        db.session.commit()

        word_update = word_update_schema.load({
            "word_id": existing_word.id,
            "update_type": "D",
            "value": existing_word.word}, session=db.session)
        word_update.created_at = datetime.now(UTC)
        db.session.add(word_update)
        db.session.commit()

        return word_schema.dump(existing_word), 200
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )
