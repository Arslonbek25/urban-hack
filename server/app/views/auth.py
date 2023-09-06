import secrets
from http import HTTPStatus

from flask import request, session
from flask_login import current_user, login_user, logout_user

from app import app, bcrypt, db
from app.models import User
from app.utils import login_required
from app.validation import LoginSchema, RegisterSchema, UpdateAccountSchema


@app.before_request
def load_user():
    if "user_id" not in session:
        session["user_id"] = secrets.token_hex(8)
        user = User(
            session_id=session["user_id"],
        )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)


@app.get("/account")
def account():
    return "current_user.session_id"


@app.post("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
        return {"message": "Logout successful"}
    return {"message": "You are not logged in"}
