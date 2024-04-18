from flask import abort
from config import enable_api_security, db
from lingo.models import Word, word_schema, words_schema
from utils.utils import get_current_user


def check_word_security():
    if enable_api_security:
        user = get_current_user()
        if not user:
            abort(
                401,
                "Unauthorized"
            )

        # Add other rules for user checking here
        # TODO


def get_all(filter = "onlyActive"):
    check_word_security()

    if filter.lower() == "onlyactive":
        words = Word.query.where(Word.active == True).all()
        return words_schema.dump(words)
    elif filter.lower() == "onlydeleted":
        words = Word.query.where(Word.active == False).all()
        return words_schema.dump(words)
    else:
        words = Word.query.all()
        return words_schema.dump(words)


def get(word_id):
    check_word_security()

    word = Word.query.where(Word.id == word_id).one_or_none()

    if word is not None:
        return word_schema.dump(word)
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


def update(word_id, word):
    check_word_security()

    existing_word = Word.query.where(Word.id == word_id).one_or_none()
    if existing_word:
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
        existing_word.active = False
        db.session.merge(existing_word)
        db.session.commit()
        return True
    else:
        abort(
            404,
            f"Word with id {word_id} not found"
        )
