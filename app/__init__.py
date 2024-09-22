# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'front.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login.init_app(app)

    @login.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    with app.app_context():
        from . import models
        db.create_all()

        from .admin_views import admin_bp
        from .front_views import front_bp
        from .escrow_views import escrow_bp

        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(front_bp)
        app.register_blueprint(escrow_bp, url_prefix='/escrow')

        print("Registered blueprints: ", app.blueprints)

    return app