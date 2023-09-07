import enum
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
    # image_file = db.Column(db.String(20))  # remove
    # messages = db.relationship("Message", backref="user", lazy=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    @property
    def dict(self):
        return {
            "username": self.username,
            "email": self.email,
        }


# from app import app

# with app.app_context() as ctx:
#     db.create_all()
