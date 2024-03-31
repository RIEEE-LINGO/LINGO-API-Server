from flask import render_template
import config
from lingo.models import Word
import firebase_admin
from firebase_admin import credentials
from utils import get_current_user

cred = credentials.Certificate("./lingoServiceAccountKey.json")
firebase_admin.initialize_app(cred)

app = config.connex_app
app.add_api(config.specdir / "api.yml")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)