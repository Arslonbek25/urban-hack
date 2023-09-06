from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

from app.config import Config
from app.extensions import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

from app.models import User
from app.views import auth, home

with app.app_context():
    db.create_all()
