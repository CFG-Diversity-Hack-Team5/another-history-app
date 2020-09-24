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
    courses = relationship("Course", back_populates="user")

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

        if email not in os.environ['ADMINS']:
            self.access = ACCESS['user']
        else:
            self.access = ACCESS['admin']

    def __repr__(self):
        return '<username {}>'.format(self.username)


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="courses")
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    category = db.Column("""TO DO""")
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    books = relationship("Book", back_populates="course")
    rating = db.Column(db.Integer)

    def __init__(self, title, body, author_id):
        self.title = title
        self.body = body
        self.author_id = author_id


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    course = relationship("Course", back_populates="books")
    book_title = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=False)

    def __init__(self, book_title, image_url, course_id):
        self.book_title = book_title
        self.image_url = image_url
        self.course_id = course_id



