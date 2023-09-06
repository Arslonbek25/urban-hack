from functools import wraps
from http import HTTPStatus

from flask_login import current_user


def login_required(view):
    @wraps(view)
    def protected(*args, **kwargs):
        if current_user.is_authenticated:
            return view(*args, **kwargs)
        return (
            {"error": "You must login to view this page"},
            HTTPStatus.UNAUTHORIZED,
        )

    return protected
