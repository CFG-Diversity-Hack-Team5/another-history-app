from main.views import db

from main.models import Course
import pytest


def test_create_course(app):

    test_model_to_insert = Course(title='Maths', category='STEM', summary="brief")
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Course).one()


