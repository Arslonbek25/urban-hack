from datetime import datetime
import enum

from app import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(13), unique=True, nullable=False)
    image_file_url = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)


class MessageType(enum.Enum):
    MESSAGE = 'message'
    FILE = 'file'


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.relationship('User', lazy=True)
    type = db.Column(db.Enum(MessageType), nullable=False)
    file_url = db.Column(db.String(64), nullable=False) 
    question = db.Column(db.String(256), nullable=True)
    answer = db.Column(db.String(256), nullable=True)
    sended_date = db.Column(db.DateTime, default=datetime.utcnow)

from app import app

with app.app_context() as ctx:
    db.create_all()