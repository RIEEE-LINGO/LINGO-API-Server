from flask import abort
from config import db
from lingo.models import Meaning, meaning_schema, meanings_schema


def get_all(word_id):
    meanings_for_word = Meaning.query.filter(Meaning.word_id == word_id).all()
    return meanings_schema.dump(meanings_for_word)


def get(word_id, meaning_id):
    meaning = Meaning.query.filter(Meaning.word_id == word_id and Meaning.id == meaning_id).one_or_none()

    if meaning is not None:
        return meaning_schema.dump(meaning)
    else:
        abort(
            404, f"Meaning with id {meaning_id} for word with id {word_id} not found"
        )


def create(meaning):
    new_meaning = meaning_schema.load(meaning, session=db.session)
    db.session.add(new_meaning)
    db.session.commit()
    return meaning_schema.dump(new_meaning), 201


def update(word_id, meaning_id, meaning):
    # TODO: It may make sense to check to ensure the word ID has not changed.
    existing_meaning = Meaning.query.filter(Meaning.word_id == word_id and Meaning.id == meaning_id).one_or_none()
    if existing_meaning:
        update_meaning = meaning_schema.load(meaning, session=db.session)
        existing_meaning.meaning = update_meaning.meaning
        db.session.merge(existing_meaning)
        db.session.commit()
        return meaning_schema.dump(existing_meaning), 201
    else:
        abort(
            404, f"Meaning with id {meaning_id} for word with id {word_id} not found"
        )
