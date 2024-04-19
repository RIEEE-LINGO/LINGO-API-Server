from config import app, db
from utils.base_data import create_teams, create_users, create_words, create_projects


def create_and_load_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = create_users(db)
        projects = create_projects(db)
        teams = create_teams(db)
        words = create_words(db, projects[0].id)


print("Run build_database.create_and_load_db() to create the DB schema and load sample data")
