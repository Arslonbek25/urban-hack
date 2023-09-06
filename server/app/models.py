import enum
from datetime import datetime

from flask_login import UserMixin

from app import db, login_manager
from app.extensions import db


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20))
    session_id = db.Column(db.String(20), unique=True, nullable=False)
    messages = db.relationship("Message", backref="user", lazy=True)


class MessageType(enum.Enum):
    MESSAGE = "message"
    FILE = "file"


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    type = db.Column(db.Enum(MessageType), nullable=False)
    file_url = db.Column(db.String(64), nullable=False)
    question = db.Column(db.String(256), nullable=True)
    answer = db.Column(db.String(256), nullable=True)
    sended_date = db.Column(db.DateTime, default=datetime.utcnow)


from app import app

with app.app_context() as ctx:
    db.create_all()
