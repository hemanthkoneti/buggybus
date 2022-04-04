import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
# from datetime import timedelta

app =Flask(__name__)
login_manager = LoginManager()

app.config["SECRET_KEY"] = "SECRET_KEY"
app.config["SESSION_PERMANENT"] = False
# app.permanent_session_lifetime=timedelta(minutes=2)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "core.login"

from buggybus.error_pages.handlers import error_pages
from buggybus.views import core
app.register_blueprint(error_pages)
app.register_blueprint(core)