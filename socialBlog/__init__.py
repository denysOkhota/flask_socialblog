""" socialBlog/__init__.py """
import os.path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret'


###############################################################################
######DATABASE CONFIGURATION#####################################################
###############################################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'socialBlog.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

###############################################################################
# LOG IN CONFIGURATION#############################################################

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'

###############################################################################
# REGISTER BLUEPRINTS###########################################################

from socialBlog.core.views import core
from socialBlog.users.views import users
from socialBlog.error_pages.handlers import error_pages
from socialBlog.blog_posts.views import blog_posts

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)