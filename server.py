from flask import render_template, Response
from config import connex_app as app, dbdir, db
from os import path, makedirs
from utils.base_data import create_words, create_teams, create_users, create_team_members


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/health")
def health():
    return Response("OK", status=200)

# If we run this file directly, that means we are in debug mode.
# Otherwise, this is being loaded by gunicorn and we don't want
# to call run.
if __name__ == "__main__":
    # If we are running in debug mode, set up the database if it
    # hasn't already been configured.
    if not path.exists(dbdir):
        makedirs(dbdir)
        with app.app.app_context():
            db.create_all()
            teams = create_teams(db)
            users = create_users(db, teams[0].id)
            create_team_members(db, users, teams[0].id)
            words = create_words(db, teams[0].id)

    app.run(host="0.0.0.0", port=8000)

