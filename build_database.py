from config import app, db
from lingo.models import Word

with app.app_context():
    db.drop_all()
    db.create_all()
    db.session.commit()
