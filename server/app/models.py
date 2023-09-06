from datetime import datetime
from app import db
import enum

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(13), unique=True, nullable=False)
    image_file_url = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PostField(db.Model):
    __tablename__ = 'postfield'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))

class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('postfield.id'), nullable=False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class PostImage(db.Model):
    __tablename__ = "postimage"

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    image_url = db.Column(db.String(60), nullable=False)

class MessageType(enum.Enum):
    MESSAGE = "message"
    FILE = "file"
    AUDIO = "audio"

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.String(256), nullable=False)
    answer = db.Column(db.String(256), nullable=False)
    type = db.Column(db.Enum(MessageType), default=MessageType.MESSAGE)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

from app import app

with app.app_context() as ctx:
    db.create_all()
