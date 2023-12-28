from flask import abort
from config import db
from lingo.models import Word, word_schema, words_schema


def get_all():
    words = Word.query.all()
    return words_schema.dump(words)


def get(word_id):
    word = Word.query.filter(Word.id == word_id).one_or_none()

    if word is not None:
        return word_schema.dump(word)
    else:
        abort(
            404, f"Word with id {word_id} not found"
        )


def create(word):
    new_word = word_schema.load(word, session=db.session)
    db.session.add(new_word)
    db.session.commit()
    return word_schema.dump(new_word), 201


def update(word_id, word):
    existing_word = Word.query.filter(Word.id == word_id).one_or_none()
    if existing_word:
        update_word = word_schema.load(word, session=db.session)
        existing_word.word = update_word.word
        db.session.merge(existing_word)
        db.session.commit()
        return word_schema.dump(existing_word), 201
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )
