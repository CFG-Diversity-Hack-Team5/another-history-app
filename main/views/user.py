from flask import Blueprint, redirect, render_template, url_for, flash
from flask_login import login_required
from main.models import CommunitySubmission
from main.views import db
from main.views.forms import CommunitySubmissionForm

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')

@user_bp.route('user/<int:user_id>/community_submission', methods=['GET','POST'])
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
        return redirect(url_for('user_dashboard'))

    return render_template('submission.html')

