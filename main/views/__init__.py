import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager(app)

    return app
