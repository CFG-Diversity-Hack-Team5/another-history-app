import os


def test_development_config(app):
    app.config.from_object('config.DevelopmentConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')


def test_testing_config(app):
    app.config.from_object('config.TestingConfig')
    assert app.config['DEBUG']
    assert app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'postgresql:///test_another_history'


def test_production_config(app):
    app.config.from_object('config.ProductionConfig')
    assert not app.config['DEBUG']
    assert not app.config['TESTING']
    assert app.config['SQLALCHEMY_DATABASE_URI'] == os.environ.get(
        'DATABASE_URL')