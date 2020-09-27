from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required
from main.models import CommunitySubmission, Course, User
from main.views import db
from main.views.forms import CommunitySubmissionForm

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def show_user_dashboard(user_id):
    user = User.query.filter_by(user_id=user_id).one()
    current_courses = user.enrolled
    liked_courses = user.liked
    completed_courses = user.completions
    return render_template('user_dashboard.html', current_courses=current_courses,
                           liked_courses=liked_courses, completed_courses=completed_courses)


@user_bp.route('user/<int:user_id>/community_submission', methods=['GET', 'POST'])
@login_required
def community_submission(user_id):

    form = CommunitySubmissionForm()
    if form.validate_on_submit():
        submission = CommunitySubmission(
            user_id=user_id,
            new_course=form.new_course.data,
            select_course=form.select_course.data,
            change_course=form.change_course.data
        )
        db.session.add(submission)
        db.session.commit()
        flash('Your submission has been recorded.')
        return redirect(url_for('.show_user_dashboard'))

    return render_template('submission.html')


@user_bp.route('user/<int:user_id/like/<int:course_id>/<action>')
@login_required
def like_action(user_id, course_id, action):
    course = Course.query.filter_by(id=course_id).first_or_404()
    user = User.query.filter_by(user_id=user_id).first()
    if action == 'like':
        user.like_course(course)
        db.session.commit()
    if action == 'unlike':
        user.unlike_course(course)
        db.session.commit()
    return redirect(request.referrer)


@user_bp.route('user/<int:user_id/enrol/<int:course_id>/<action>')
@login_required
def enrol_action(user_id, course_id, action):
    course = Course.query.filter_by(id=course_id).first_or_404()
    user = User.query.filter_by(user_id=user_id).first()
    if action == 'enrol':
        user.enrol(course)
        db.session.commit()
    return redirect(request.referrer)


@user_bp.route('user/<int:user_id/complete/<int:course_id>/<action>')
@login_required
def complete_action(user_id, course_id, action):
    course = Course.query.filter_by(id=course_id).first_or_404()
    user = User.query.filter_by(user_id=user_id).first()
    if action == 'like':
        user.mark_course_completed(course)
        db.session.commit()
    return redirect(request.referrer)

