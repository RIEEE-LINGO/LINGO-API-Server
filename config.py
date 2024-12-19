import pathlib
import connexion
from os import environ
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("./lingoServiceAccountKey.json")
firebase_admin.initialize_app(cred)

basedir = pathlib.Path(__file__).parent.resolve()
dbdir = basedir.joinpath("db")
specdir = basedir.joinpath("spec")

default_team = 1

connex_app = connexion.App(__name__, specification_dir=specdir)
app = connex_app.app

# By default, API security is enabled.
enable_api_security = True
enable_security_var = environ.get("ENABLE_SECURITY")
if enable_security_var:
    security_flag = enable_security_var.strip()
    if len(security_flag) > 0:
        if security_flag.upper() == "NO":
            enable_api_security = False

# Default user ID, for when security is not enabled.
default_user_id = 1
default_user_id_var = environ.get("DEFAULT_USER_ID")
if default_user_id_var:
    try:
        default_user_id = int(default_user_id_var.strip())
    except ValueError:
        default_user_id = 1

# "mysql+pymysql://lingo:lingo@localhost/lingo"
# By default, we will use SQLite if another database is not given
database_uri = f"sqlite:///{dbdir / 'lingo.db'}"
db_url_var = environ.get("DATABASE_URL")
if db_url_var:
    uri_input = db_url_var.strip()
    if len(uri_input) > 0:
        database_uri = uri_input
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = SQLAlchemy(app)
ma = Marshmallow(app)

# Add the API specification into the server
connex_app.add_api(specdir / "api.yml")
