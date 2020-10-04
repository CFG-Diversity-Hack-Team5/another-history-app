
import pytest
from main.views import create_app, db
from main.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('config.TestingConfig')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_user():
    user = User(email='test@example.com', password_hash=generate_password_hash('test456'))
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_course():
    course = Course(title='Women in Science', category='STEM', summary='Meet women in science')
    db.session.add(course)
    db.session.commit()
    return course







