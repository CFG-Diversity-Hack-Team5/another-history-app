from flask import Blueprint, redirect, render_template, flash, request, session, url_for
from main.models import User
from main.views.forms import SignupForm, LoginForm, RequestResetForm, ResetPasswordForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, logout_user, current_user, login_user
from main.views import db, login_manager, Mail, Message


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()  # Create new user
            login_user(user, remember=form.remember_me.data)  # Log in as newly created user

            if user.access == 1:
                return redirect(url_for('user_bp.show_user_dashboard', uid=user.user_id))
            else:
                return redirect(url_for('admin_bp.show_admin_dashboard'))
        flash('A user already exists with that email address.')
    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET requests serve Log-in page.
    POST requests validate and redirect user to dashboard.
    """
    # Bypass if user is logged in
    if current_user.is_authenticated:
        return redirect(url_for('user_bp.show_user_dashboard', uid=current_user.user_id))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('user_bp.show_user_dashboard', uid=user.user_id))
        flash('Invalid email/password combination')
        return redirect(url_for('.login'))
    return render_template('sign_in.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to homepage."""
    flash('Please login to view this page.')
    return redirect(url_for('.login'))


@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('.login'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@anotherhistory.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    Mail.send(msg)


@auth_bp.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        flash('Please logout before resetting your password.')
        return redirect(url_for('public_bp.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.')
        return redirect(url_for('.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@auth_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash('Please logout before resetting your password.')
        return redirect(url_for('public_bp.index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

