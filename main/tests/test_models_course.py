from main.models import Course
import pytest
import unittest
from main.views.forms import CourseForm
from main.views import db

def test_create_course(app):

    test_model_to_insert = Course(title='Maths', category='STEM', summary="brief")
    db.session.add(test_model_to_insert)
    db.session.commit()

    assert db.session.query(Course).one()

'''
def create_course(title="Course 1", category="STEM", summary="WOWZ"):
    return Course.objects.create(title=title, category=category, summary=summary)


class CourseTest(unittest.TestCase):

    def test_course(self):
        c = create_course()
        self.assertTrue(isinstance(c, Course))
        self.assertEqual(c.title.__unicode__(), c.title)
        self.assertEqual(c.category.__unicode__(), c.category())
        self.assertEqual(c.summary.__unicode__(), c.summary())
'''




