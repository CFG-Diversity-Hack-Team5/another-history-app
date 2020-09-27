import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail, Message


csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    from main.views.auth import auth_bp
    app.register_blueprint(auth_bp)

    from main.views.public import public_bp
    app.register_blueprint(public_bp)

    from main.views.user import user_bp
    app.register_blueprint(user_bp)

    from main.views.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
