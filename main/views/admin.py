from flask import Blueprint, redirect, render_template, url_for, request, flash
from main.models import Course, Module, Book
from sqlalchemy import desc
from main.views.forms import CourseForm, ModuleForm, BookForm
from main.views import db
from main.models import ACCESS
from main.decorators import requires_access_level
from flask_login import login_required
import requests
import json
import os

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/courses', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data,
                        category=form.category.data,
                        summary=form.summary.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('.create_module', course_id=course.id))
    return render_template('course_form.html', form=form)


@admin_bp.route('/courses/<int:course_id>/modules', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def create_module(course_id):
    form = ModuleForm()
    if form.validate_on_submit():
        last_module = Module.query.filter_by(course_id=course_id).order_by(desc(Module.week_number)).first()
        if last_module is None:
            week_number = 1
        else:
            week_number = last_module.week_number + 1

        module = Module(name=form.name.data,
                        content=form.content.data,
                        course_id=course_id,
                        week_number=week_number)

        db.session.add(module)
        db.session.commit()
        return redirect(url_for('.create_book', course_id=course_id))
    return render_template('module_form.html', form=form)


@admin_bp.route('/courses/<int:course_id>/books', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def create_book(course_id):
    form = BookForm()
    if form.validate_on_submit():
        title = form.book_title.data
        #query = title.replace(" ", "%20")
        params = {'q': title, 'key': os.environ['API_KEY']}
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
        if response.status_code == 200:
            api_response = json.loads(response.text)
            first_book = api_response["items"][0]
            if first_book is None:
                flash('Your book has not been found. Try adding another book.')
                return redirect(url_for('.show_admin_course'))
            else:
                volume_info = first_book["volumeInfo"]
                title = volume_info["title"]
                thumbnail = volume_info["imageLinks"]["thumbnail"]
                preview_link = volume_info["previewLink"]
                book = Book(book_title=title,
                            thumbnail=thumbnail,
                            preview_link=preview_link,
                            course_id=course_id)
                db.session.add(book)
                db.session.commit()
                flash('Your book has been added to the course.')
                return redirect(url_for('.show_admin_dashboard'))
        flash('Your book has not been found.')
        return redirect(url_for('.show_admin_dashboard'))

    return render_template('book_form.html', form=form)


'''@admin_bp.route('/courses/<int:course_id>', methods=['GET', 'POST'])
@requires_access_level(ACCESS['admin'])
def show_admin_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        flash('Course has not been found.')
        return redirect(url_for('.show_admin_dashboard'))
    modules = Module.query.filter(course_id == course_id).all()
    books = course.books
    return render_template('course.html', course=course, modules=modules, books=books)'''


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def show_admin_dashboard():
    courses = Course.query.all()
    return render_template('admin_login.html', courses=courses)


@admin_bp.route('/courses/<int:course_id>/delete', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def delete_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('.show_admin_dashboard'))


@admin_bp.route('/courses/<int:course_id>/update', methods=['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def update_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    form = CourseForm()
    if form.validate_on_submit():
        course.title = form.title.data
        course.summary = form.summary.data
        course.category = form.category.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('.show_admin_dashboard'))
    elif request.method == 'GET':
        form.title.data = course.title
        form.summary.data = course.summary
        form.category.data = course.category
    return render_template('course_form.html', form=form)




