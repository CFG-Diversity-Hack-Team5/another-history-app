from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import login_required
from main.models import Course, User, Enrolment, CourseLike, CourseCompletion
from main.views import db
from main.models import ACCESS
from main.decorators import requires_access_level

user_bp = Blueprint('user_bp', __name__)


@user_bp.route('/user/<int:uid>', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['user'])
def show_user_dashboard(uid):
    user = User.query.filter_by(id=uid).one()
    current_courses = Course.query.join(Enrolment, Course.id == Enrolment.course_id).join(
        User, Enrolment.user_id == User.id).filter(User.id == uid).all()
    liked_courses = Course.query.join(CourseLike, Course.id == CourseLike.course_id).join(
        User, CourseLike.user_id == User.id).filter(User.id == uid).all()
    completed_courses = Course.query.join(CourseCompletion, Course.id == CourseCompletion.course_id).join(
        User, CourseCompletion.user_id == User.id).filter(User.id == uid).all()
    return render_template('login.html', current_courses=current_courses,
                           liked_courses=liked_courses, completed_courses=completed_courses)


'''@user_bp.route('user/<int:user_id>/community_submission', methods=['GET', 'POST'])
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

    return render_template('submission.html')'''


@user_bp.route('/user/<int:uid>/like/<int:cid>/<action>')
@login_required
@requires_access_level(ACCESS['user'])
def like_action(uid, cid, action):
    course = Course.query.filter_by(id=cid).first_or_404()
    user = User.query.filter_by(id=uid).first()
    if action == 'like':
        user.like_course(course)
        db.session.commit()
    if action == 'unlike':
        user.unlike_course(course)
        db.session.commit()
    return redirect(request.referrer)


@user_bp.route('/user/<int:uid>/enrol/<int:cid>/<action>')
@login_required
@requires_access_level(ACCESS['user'])
def enrol_action(uid, cid, action):
    course = Course.query.filter_by(id=cid).first_or_404()
    user = User.query.filter_by(id=uid).first()
    if action == 'enrol':
        user.enrol(course)
        db.session.commit()
    return redirect(request.referrer)


@user_bp.route('/user/<int:uid>/complete/<int:cid>/<action>')
@login_required
@requires_access_level(ACCESS['user'])
def complete_action(uid, cid, action):
    course = Course.query.filter_by(id=cid).first_or_404()
    user = User.query.filter_by(id=uid).first()
    if action == 'complete':
        user.mark_course_completed(course)
        db.session.commit()
    return redirect(request.referrer)

