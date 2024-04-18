from flask import render_template, Response
from config import connex_app as app, dbdir, db
from os import path, makedirs
from utils.base_data import create_projects, create_words, create_teams, create_users

# If we run this file directly, that means we are in debug mode.
# Otherwise, this is being loaded by gunicorn and we don't want
# to call run.
if __name__ == "__main__":
    if not path.exists(dbdir):
        makedirs(dbdir)
        with app.app.app_context():
            db.create_all()
            users = create_users(db)
            projects = create_projects(db)
            teams = create_teams(db)
            words = create_words(db, projects[0].id)

    app.run(host="0.0.0.0", port=8000, debug=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/health")
def health():
    return Response("OK", status=200)