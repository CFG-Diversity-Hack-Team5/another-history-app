import pytest
from main.models import User
from unittest import mock
from flask_login import current_user
from main.tests.test_models_course import create_course
from main.views import db
from main.views.public import index


def test_index_page(self):

    response = self.client.get('/')
    assert 'http://localhost/' == response.headers['Location']
    assert response.status_code == 200
    assert b'Another History' in response.data
    assert b'A brighter future is built on Another History' in response.data
    assert b'Browse all courses' in response.data
    assert b'Join today and begin your unlearning journey' in response.data
    assert b'Another History was made for Code First Girls Diversity hackathon' in response.data
    if current_user.is_active():
        assert b'Log Out' in response.data
    else:
        assert b'Sign in' in response.data


    '''@mock.patch('app.dal.connection')
    def test_course_connection(self, mock_conn):
        mock_conn.execute.return_fetchall.return_value = self.create_course
        results = index()
        self.assertEqual(results, self.create_course)

    is_database_working = True
    output = 'database connection is fine'
    try:
        db.session.execute('SELECT 1')
    except Exception as e:
        output = str(e)
        is_database_working = False
        raise Exception("Database connection failed")

    return is_database_working, output'''


def test_index_course(self, test_course):
    response = self.get('/courses/<int:cid>')
    assert 'http://localhost/courses/<int:cid>' == response.headers['Location']
    assert response.status_code == 200
    assert b'Another History' in response.data
    assert b'Another History was made for Code First Girls Diversity hackathon' in response.data
    assert bytes('/courses/{}'.format(test_course.id).encode()) in response.data
    if current_user.is_active():
        assert b'Log Out' in response.data
    else:
        assert b'Sign in' in response.data


def test_index_about(self):
    response = self.get('/about')
    assert 'http://localhost/about' == response.headers['Location']
    assert response.status_code == 200


