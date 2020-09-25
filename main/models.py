import os
from main.views import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from flask_login import UserMixin

ACCESS = {
    'user': 1,
    'admin': 2
}

association_table = Table('association', Base.metadata,
    Column('left_id', Integer, ForeignKey('left.id')),
    Column('right_id', Integer, ForeignKey('right.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    access = db.Column(db.Integer, nullable=False)
    courses = relationship("Course", back_populates="user")
    liked = db.relationship(
        'CourseLike',
        foreign_keys='CourseLike.user_id',
        backref='user', lazy='dynamic')

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

        if email not in os.environ['ADMINS']:
            self.access = ACCESS['user']
        else:
            self.access = ACCESS['admin']

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def like_course(self, course):
        if not self.has_liked_post(course):
            like = CourseLike(user_id=self.id, course_id=course.id)
            db.session.add(like)

    def unlike_course(self, course):
        if self.has_liked_post(course):
            CourseLike.query.filter_by(
                user_id=self.id,
                course_id=course.id).delete()

    def has_liked_course(self, course):
        return CourseLike.query.filter(
            CourseLike.user_id == self.id,
            CourseLike.course_id == course.id).count() > 0


class Course(db.Model):
    __tablename__ = 'course'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    user = relationship("User", back_populates="courses")
    title = db.Column(db.String(), nullable=False)
    body = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), unique=False, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    books = relationship("Book", secondary=association_table, back_populates="courses")
    is_approved = db.Column(db.Boolean, default=False, unique=False)
    likes = db.relationship('CourseLike', backref='course', lazy='dynamic')


    def __init__(self, title, body, author_id, category):
        self.title = title
        self.body = body
        self.author_id = author_id
        self.category = category


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    courses = relationship("Course", secondary=association_table, back_populates="books")
    book_title = db.Column(db.String(), nullable=False)
    image_url = db.Column(db.String(), nullable=False)

    def __init__(self, book_title, image_url, course_id):
        self.book_title = book_title
        self.image_url = image_url
        self.course_id = course_id

class CourseLike(db.Model):
    __tablename__ = 'course_like'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id


