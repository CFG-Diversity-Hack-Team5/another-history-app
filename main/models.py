import os
from main.views import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from flask_login import UserMixin

ACCESS = {
    'user': 1,
    'admin': 2
}

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    access = db.Column(db.Integer, nullable=False)

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

        if email not in os.environ['ADMINS']:
            self.access = ACCESS['user']
        else:
            self.access = ACCESS['admin']

    def __repr__(self):
        return '<username {}>'.format(self.username)
