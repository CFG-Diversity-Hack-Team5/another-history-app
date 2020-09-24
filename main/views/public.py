from flask import Blueprint, redirect, render_template
from main.models import Course

public_bp = Blueprint('public_bp', __name__)

@public_bp.route('/', methods=['GET', 'POST'])
def homepage():
    popular_courses = Course.query.filter_by(rating=5).limit(3)
    popular_courses = [course.title for course in popular_courses]
    featured_course = Course.query.filter(Course.body.like('%Featured_Person_Name%'))
    featured_category = featured_course.category
    related_courses = Course.query.filter_by(category=featured_category).limit(3)
    related_courses = [course.title for course in related_courses]

    return render_template('placeholder.html', popular_courses=popular_courses, features_course=featured_course, related_courses=related_courses)

@public_bp.route('/courses', methods=['GET','POST'])
def browse_courses():

    return render_template()


@public_bp.route('/course', methods=['GET','POST'])
def show_course():
    return render_template()


@public_bp.route('/about', methods=['GET','POST'])
def about_us():
    return render_template()
