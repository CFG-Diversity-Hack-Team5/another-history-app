from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField,
                     BooleanField,
                     SubmitField,
                     SelectField,
                     PasswordField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                ValidationError)
from main.models import User, Course

class SignupForm(FlaskForm):
    """Sign up for a user account."""

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        Length(min=6, message='Select a stronger password.')
    ])
    confirmPassword = PasswordField('Repeat Password', [
            EqualTo(password, message='Passwords must match.')
            ])

    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    """User Log-in Form."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Enter a valid email.')
        ]
    )
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Log In')

class RequestResetForm(FlaskForm):
    '''User Request New Password Form'''
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    '''User Reset Password Form'''
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class CommunitySubmissionForm(FlaskForm):
    '''User Submission Form'''
    new_course = StringField(validators=[DataRequired()])

    course_choices = Course.query.all()
    course_choices = [course.title for course in course_choices]
    select_course = SelectField(u'Course Name', choices=course_choices, validators=[DataRequired()])

    change_course = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')

