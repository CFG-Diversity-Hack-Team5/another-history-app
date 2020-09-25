from flask import Blueprint, redirect, render_template
from main.models import Course, CourseLike
from sqlalchemy import func

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/', methods=['GET', 'POST'])
def homepage():
    popular_courses = Course.query.join(
        CourseLike, Course.id == CourseLike.course_id).group_by(Course.id).order_by(func.count().desc()).limit(3).all()
    popular_courses = [course.title for course in popular_courses]
    featured_course = Course.query.filter(Course.body.like('%Featured_Person_Name%')).first()
    featured_category = featured_course.category
    related_courses = Course.query.filter_by(category=featured_category).limit(3).all()
    related_courses = [course.title for course in related_courses]

    return render_template('placeholder.html',
                           popular_courses=popular_courses,
                           featured=featured_course.title,
                           related_courses=related_courses)

@public_bp.route('/courses', methods=['GET','POST'])
def browse_courses():
    courses = Course.query.all()
    return render_template('html', courses=courses)


@public_bp.route('/course/<int:course_id>', methods=['GET','POST'])
def show_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    return render_template("placeholder.html", course=course)


@public_bp.route('/about', methods=['GET','POST'])
def about_us():
    return render_template()
