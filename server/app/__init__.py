from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

from app.models import User
with app.app_context():
    db.create_all()

from app.views import home
