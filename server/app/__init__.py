from flask import Flask
from flask_migrate import Migrate

from app.config import Config
from app.extensions import db
# from app.models import User

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

from app.models import User
with app.app_context():
    db.create_all()

from app.views import home