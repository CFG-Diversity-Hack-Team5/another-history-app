from functools import wraps
from flask import url_for, redirect, session
from main.models import User


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('email'):
                return redirect(url_for('auth_bp.login'))
            user = User.query.filter_by(email=session['email']).one()

            if not user.allowed(access_level):
                return redirect(url_for('public_bp.index', message="You do not have access to that page. Sorry!"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
