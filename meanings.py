from flask import abort
from config import db
from lingo.models import Meaning, meaning_schema, meanings_schema

def get_all():
    words = Meaning.query.all()
    return meanings_schema.dump(words)

def get(id):
    meaning = Meaning.query.filter(Meaning.id == id).one_or_none()

    if meaning is not None:
        return meaning_schema.dump(meaning)
    else:
        abort(
            404, f"Meaning with id {id} not found"
        )

def create(meaning):
    new_meaning = meaning_schema.load(meaning, session=db.session)
    db.session.add(new_meaning)
    db.session.commit()
    return meaning_schema.dump(new_meaning), 201

def update(id,meaning):
    existing_meaning = Meaning.query.filter(Meaning.id == id).one_or_none()
    if existing_meaning:
        update_meaning = meaning_schema.load(meaning, session=db.session)
        existing_meaning.meaning = update_meaning.meaning
        db.session.merge(existing_meaning)
        db.session.commit()
        return meaning_schema.dump(existing_meaning), 201
    else:
        abort(
            404,
            f"Meaning with id {id} not found"
        )
