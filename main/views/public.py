from flask import Blueprint, redirect, render_template, url_for
from main.models import Course, CourseLike, Module
from sqlalchemy import func
from flask_login import current_user

public_bp = Blueprint('public_bp', __name__)


@public_bp.route('/', methods=['GET', 'POST'])
def index():
    popular_courses = Course.query.join(
        CourseLike, Course.id == CourseLike.course_id).group_by(Course.id).order_by(func.count().desc()).limit(3).all()
    popular_courses = [course.title for course in popular_courses]
    featured_course = Course.query.filter(Course.body.like('%Featured_Person_Name%')).first()  # to do
    featured_category = featured_course.category
    related_courses = Course.query.filter_by(category=featured_category).limit(3).all()
    related_courses = [course.title for course in related_courses]

    if current_user.is_authenticated:
        if current_user.access == 1:
            return redirect(url_for('user_bp.show_user_dashboard'))  # to do
        else:
            return redirect(url_for('admin_bp.show_admin_dashboard'))

    return render_template('index.html',
                           popular_courses=popular_courses,
                           featured=featured_course.title,
                           related_courses=related_courses)


@public_bp.route('/courses', methods=['GET', 'POST'])
def browse_courses():
    courses = Course.query.all()
    return render_template('html', courses=courses)


@public_bp.route('/courses/<int:course_id>', methods=['GET', 'POST'])
def show_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    modules = Module.query.join(Course, Module.course_id == Course.id).filter(course_id == course_id).all()
    books = course.books
    return render_template("placeholder.html", course=course,
                           modules=modules,
                           books=books)


@public_bp.route('/about', methods=['GET'])
def about_us():
    return render_template("about.html")
