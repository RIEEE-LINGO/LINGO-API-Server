import os
import pathlib
import connexion
from os import environ, path
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./lingoServiceAccountKey.json")
firebase_admin.initialize_app(cred)

basedir = pathlib.Path(__file__).parent.resolve()
dbdir = basedir.joinpath("db")
specdir = basedir.joinpath("spec")

connex_app = connexion.App(__name__, specification_dir=specdir)
app = connex_app.app
enable_api_security = not app.config["DEBUG"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

if app.config["DEBUG"]:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{dbdir / 'lingo.db'}"
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Add the API specification into the server
connex_app.add_api(specdir / "api.yml")

