from flask import Blueprint, redirect, render_template, flash, session, url_for
from main.models import User
from main.views.forms import SignupForm, LoginForm
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user, login_required, logout_user
from main.views import db, login_manager


# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    User sign-up page.

    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    if current_user.is_authenticated:
        flash('You have already registered.')
        if current_user.is_admin():
            return redirect(url_for('admin_bp.show_admin_dashboard'))
        return redirect(url_for('user_bp.show_user_dashboard', uid=current_user.id))
    form = SignupForm()
    print(form.csrf_token)
    if form.validate_on_submit():
        print(form.csrf_token)
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            user = User(
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data)
            )
            if form.email.data == "another.history.team@gmail.com":
                user.access = 2
            db.session.add(user)
            db.session.commit()  # Create new user
            return redirect((url_for('public_bp.index')))
            # login_user(user)  # Log in as newly created user
            # if user.is_admin():
            #    return redirect(url_for('admin_bp.show_admin_dashboard'))
            # else:
                # return redirect(url_for('public_bp.index'))
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
        if current_user.is_admin():
            return redirect(url_for('admin_bp.show_admin_dashboard'))
        else:
            return redirect(url_for('user_bp.show_user_dashboard', uid=current_user.id))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            session['email'] = form.email.data
            if user.access == 1:
                return redirect(url_for('user_bp.show_user_dashboard', uid=user.id))
            else:
                return redirect(url_for('admin_bp.show_admin_dashboard'))
        flash('Invalid email/password combination')
        return redirect(url_for('auth_bp.login'))
    return render_template('sign_in.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    """Check if user is logged-in on every page load."""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users."""
    flash('Please login to view this page.')
    return redirect(url_for('auth_bp.login'))

@auth_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
