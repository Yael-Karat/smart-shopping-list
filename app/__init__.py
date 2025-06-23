from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models import User  # חשוב לייבא את המודל

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from app import routes, models
