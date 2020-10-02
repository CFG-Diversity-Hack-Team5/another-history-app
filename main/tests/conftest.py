import os
import sqlalchemy as sa
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest_postgresql.factories import (init_postgresql_database,
                                         drop_postgresql_database)
import psycopg2
import pytest
from main.views import create_app

TEST_DATABASE_URL = 'postgresql:///test_another_history'

# Retrieve a database connection string from the shell environment
try:
 ##   DB_CONN = os.environ['TEST_DATABASE_URL']
    DB_CONN = TEST_DATABASE_URL

except KeyError:
    raise KeyError('TEST_DATABASE_URL not found. You must export a database ' +
                        'connection string to the environmental variable ' +
                        'TEST_DATABASE_URL in order to run tests.')
else:
    DB_OPTS = sa.engine.url.make_url(DB_CONN).translate_connect_args()
    #pytest_plugins = ['pytest-flask-sqlalchemy']

@pytest.fixture(scope='session')
def database(request):
    '''
    Create a Postgres database for the tests, and drop it when the tests are done.
    '''
    pg_host = DB_OPTS.get("host")
    pg_port = DB_OPTS.get("port")
    pg_user = DB_OPTS.get("username")
    pg_db = DB_OPTS["database"]

    init_postgresql_database(pg_user, pg_host, pg_port, pg_db)

    @request.addfinalizer
    def drop_database():
        drop_postgresql_database(pg_user, pg_host, pg_port, pg_db, 9.6)


@pytest.fixture(scope='session')
def app(database):
    '''
    Create a Flask app context for the tests.
    '''
    app = create_app()

    app.config['SQLALCHEMY_DATABASE_URI'] = DB_CONN

    return app


@pytest.fixture(scope='session')
def _db(app):
    '''
    Provide the transactional fixtures with access to the database via a Flask-SQLAlchemy
    database connection.
    '''
    db = SQLAlchemy(app=app)

    return db


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


