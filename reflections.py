from flask import abort
from config import db
from lingo.models import Reflection, reflection_schema, reflections_schema

def get_all():
    words = Reflection.query.all()
    return reflections_schema.dump(words)

def get(id):
    reflection = Reflection.query.filter(Reflection.id == id).one_or_none()

    if reflection is not None:
        return reflection_schema.dump(reflection)
    else:
        abort(
            404, f"Reflection with id {id} not found"
        )

def create(reflection):
    new_reflection = reflection_schema.load(reflection, session=db.session)
    db.session.add(new_reflection)
    db.session.commit()
    return reflection_schema.dump(new_reflection), 201

def update(id,reflection):
    existing_reflection = Reflection.query.filter(Reflection.id == id).one_or_none()
    if existing_reflection:
        update_reflection = reflection_schema.load(reflection, session=db.session)
        existing_reflection.reflection = update_reflection.reflection
        db.session.merge(existing_reflection)
        db.session.commit()
        return reflection_schema.dump(existing_reflection), 201
    else:
        abort(
            404,
            f"Reflection with id {id} not found"
        )
