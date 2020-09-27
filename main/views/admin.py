from flask import Blueprint, redirect, render_template, url_for, g, flash
from main.models import User, Course, Module, Book
from sqlalchemy import desc
from main.views.forms import CourseForm, ModuleForm, BookForm
from main.views import db
import requests
import json
import os

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/courses', methods=['GET', 'POST'])
@login_required
def submit_course_details():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data,
                        category=form.category.data,
                        summary=form.summary.data)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('admin.show_admin_course'))
    return render_template('submit_course_details.html')


@admin_bp.route('/courses/<int:course_id>/modules', methods=['GET', 'POST'])
@login_required
def submit_modules(course_id):
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
        return redirect(url_for('admin.show_admin_course'))
    return render_template('submit_modules.html')


@admin_bp.route('/courses/<int:course_id>/books', methods=['GET', 'POST'])
@login_required
def submit_books(course_id):
    form = BookForm()
    api_key = os.environ['API_KEY']
    if form.validate_on_submit():
        search_url = "https://www.googleapis.com/books/v1/volumes?q={}&key={}".format(form.title.data, api_key)
        response = requests.get(search_url)
        if response.status_code == 200:
            api_response = json.loads(response.text)
            first_book = api_response["items"][0]
            if first_book is None:
                flash('Your book has not been found. Try adding another book.')
                return redirect(url_for('admin.show_course'))
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
                return redirect(url_for('admin.show_admin_course'))
        else:
            flash('Your book has not been found.')

    return render_template('submit_books.html')


@admin_bp.route('/courses/<int:course_id>', methods=['GET', 'POST'])
@login_required
def show_admin_course(course_id):
    course = Course.query.filter_by(id=course_id).first()
    if course is None:
        flash('Course has not been found.')
        return redirect(url_for('admin_dashboard'))
    modules = Module.query.filter(course_id == course_id).all()
    books = course.books
    return render_template('show_course.html', course=course, modules=modules, books=books)

