import hashlib
from datetime import datetime

from flask import url_for
from flask_login import UserMixin

from app import db, login_manager
from app.extensions import db


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    chats = db.relationship("Chat", backref="user", lazy=True)

    @property
    def dict(self):
        return {
            "username": self.username,
            "email": self.email,
        }

    @property
    def gravatar_url(self, size=100):
        digest = hashlib.md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text_messages = db.relationship("TextMessage", backref="chat", lazy=True)
    image_messages = db.relationship("ImageMessage", backref="chat", lazy=True)

    @property
    def dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }


class TextMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.Column(db.String(20), nullable=False)

    @property
    def dict(self):
        return {
            "type": "text",
            "text": self.text,
            "timestamp": self.timestamp,
            "sender": self.sender,
        }


class ImageMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey("chat.id"), nullable=False)
    image_path = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender = db.Column(db.String(20), nullable=False)
    prediction = db.Column(db.String(20))

    @property
    def dict(self):
        return {
            "type": "image",
            "path": url_for(
                "static", filename=f"x-rays/{self.image_path}", _external=True
            ),
            "timestamp": self.timestamp,
            "sender": self.sender,
            "prediction": self.prediction,
        }


# from app import app

# with app.app_context() as ctx:
#     db.create_all()
