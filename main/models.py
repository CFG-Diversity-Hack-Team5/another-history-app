import os
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main.views import db
import flask_sqlalchemy
import flask_whooshalchemy
from whoosh.analysis import StemmingAnalyzer, DoubleMetaphoneFilter


ACCESS = {
    'user': 1,
    'admin': 2
}


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    '''access = db.Column(db.Integer, nullable=False)'''
    liked = db.relationship('CourseLike',
                            foreign_keys='CourseLike.user_id',
                            backref='user', lazy='dynamic')
    enrolled = db.relationship("Enrolment", foreign_keys='Enrolment.user_id',
                               backref='user', lazy='dynamic')
    completions = db.relationship("CourseCompletion", foreign_keys='CourseCompletion.user_id',
                                  backref='user', lazy='dynamic')

    def __init__(self, email, password_hash):
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(os.environ['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(os.environ['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

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

    def enrol(self, course):
        if not self.has_enrolled(course):
            enrolment = Enrolment(user_id=self.id, course_id=course.id)
            db.session.add(enrolment)

    def has_enrolled(self, course):
        return Enrolment.query.filter(Enrolment.user_id == self.id,
                                      Enrolment.course_id == course.id).count() > 0

    def mark_course_completed(self, course):
        if not self.has_marked_completed(course):
            completion = CourseCompletion(user_id=self.id, course_id=course.id)
            db.session.add(completion)

    def has_marked_completed(self, course):
        return CourseCompletion.query.filter(CourseCompletion.user_id == self.id,
                                             Course.Completion.course_id == course.id).count() > 0


class Course(db.Model):
    __tablename__ = 'course'
    '''__searchable__ = ['title', 'summary']  # indexed fields
    __analyzer__ = StemmingAnalyzer() | DoubleMetaphoneFilter()'''

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(), nullable=False)
    summary = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), unique=False, nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    books = db.relationship("Book", back_populates="courses")
    modules = db.relationship("Module", back_populates="courses")
    likes = db.relationship("CourseLike", backref='course', lazy='dynamic')
    enrolments = db.relationship("Enrolment", backref='course', lazy='dynamic')
    completions = db.relationship("CourseCompletion", backref='course', lazy='dynamic')

    def __init__(self, title, category, summary):
        self.title = title
        self.category = category
        self.summary = summary


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)
    book_title = db.Column(db.String(), nullable=False)
    thumbnail = db.Column(db.String(), nullable=False)
    preview_link = db.Column(db.String(), nullable=False)
    courses = db.relationship("Course", back_populates="books")

    def __init__(self, book_title, thumbnail, preview_link, course_id):
        self.book_title = book_title
        self.thumbnail = thumbnail
        self.preview_link = preview_link
        self.course_id = course_id


class CourseLike(db.Model):
    __tablename__ = 'course_like'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id


'''class CommunitySubmission(db.Model):
    __tablename__ = 'community_submission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship("User", back_populates="submissions")
    new_course = db.Column(db.String(), nullable=False)
    select_course = db.Column(db.String(), nullable=False)
    change_course = db.Column(db.String(), nullable=False)

    def __init__(self, user_id, new_course, select_course, change_course):
        self.user_id = user_id
        self.new_course = new_course
        self.select_course = select_course
        self.change_course = change_course'''


class Module(db.Model):
    __tablename__ = 'module'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete="CASCADE"), nullable=False)
    name = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    courses = db.relationship("Course", back_populates="modules")

    def __init__(self, name, content, course_id, week_number):
        self.name = name
        self.content = content
        self.course_id = course_id
        self.week_number = week_number


class Enrolment(db.Model):
    __tablename__ = 'enrolment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id


class CourseCompletion(db.Model):
    __tablename__ = 'course_completion'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, user_id, course_id):
        self.user_id = user_id
        self.course_id = course_id
