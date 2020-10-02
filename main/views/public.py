from flask import Blueprint, redirect, render_template, url_for
from main.models import Course, Module, Book
from sqlalchemy import func
from flask_login import current_user

public_bp = Blueprint('public_bp', __name__)


@public_bp.route('/', methods=['GET', 'POST'])
def index():
    '''popular_courses = Course.query.join(
        CourseLike, Course.id == CourseLike.course_id).group_by(Course.id).order_by(func.count().desc()).limit(3).all()
    popular_courses = [course.title for course in popular_courses]'''

    courses = Course.query.all()

    '''if current_user.is_authenticated:
        return redirect(url_for('user_bp.show_user_dashboard'))'''

    return render_template('index.html', courses=courses)


'''@public_bp.route('/courses', methods=['GET', 'POST'])
def browse_courses():
    course = Course.query.all()
    return render_template('course.html', courses=courses)'''


@public_bp.route('/courses/<int:cid>', methods=['GET', 'POST'])
def show_course(cid):
    course = Course.query.filter_by(id=cid).one()
    modules = Module.query.join(Course, Module.course_id == Course.id).filter(Module.course_id == cid).all()
    books = Book.query.join(Course, Book.course_id == Course.id).filter(Book.course_id == cid).all()
    return render_template("course.html", course=course,
                           modules=modules,
                           books=books)


@public_bp.route('/about', methods=['GET'])
def about_us():
    return render_template("about.html")
