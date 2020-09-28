from flask_wtf import FlaskForm
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
from main.models import User


class SignupForm(FlaskForm):

    email = StringField('Email address', [
        Email(message='Not a valid email address.'),
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired(message="Please enter a password."),
        Length(min=6, message='Select a stronger password.')
    ])

    remember_me = BooleanField('Remember Me', default=False)
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
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
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Select a stronger password.')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


'''class CommunitySubmissionForm(FlaskForm):
    new_course = StringField(validators=[DataRequired()])

    course_choices = Course.query.all()
    course_choices = [course.title for course in course_choices]
    select_course = SelectField(u'Course Name', choices=course_choices, validators=[DataRequired()])

    change_course = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')'''


class CourseForm(FlaskForm):
    title = StringField('Course Title', validators=[DataRequired()])
    choices = ['STEM', 'Arts & Humanities', 'Culture & Society', 'Politics']
    category = SelectField('Category', choices=choices, validators=[DataRequired()])
    summary = StringField('Summary', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ModuleForm(FlaskForm):
    name = StringField('Module Name', validators=[DataRequired()])
    content = StringField('Module Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


class BookForm(FlaskForm):
    book_title = StringField('Book Title', validators=[DataRequired(message='Please enter a book title.')])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    search = StringField('Search courses', validators=[DataRequired()])
    submit = SubmitField('Submit')
