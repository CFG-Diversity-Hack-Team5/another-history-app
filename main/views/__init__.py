import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(os.environ['APP_SETTINGS'])

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    from main import models

    with app.app_context():
        db.create_all(bind=None, tables=None, checkfirst=True)

    from main.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    from main.views.public import public_bp
    app.register_blueprint(public_bp)

    from main.views.user import user_bp
    app.register_blueprint(user_bp)

    from main.views.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
