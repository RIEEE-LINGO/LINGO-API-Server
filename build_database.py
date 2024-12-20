from config import app, db
from utils.base_data import create_teams, create_users, create_words


def create_and_load_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = create_users(db)
        teams = create_teams(db, users)
        words = create_words(db, teams[0].id)


print("Run build_database.create_and_load_db() to create the DB schema and load sample data")
