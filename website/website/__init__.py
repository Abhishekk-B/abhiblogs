from ensurepip import bootstrap
import imp
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap





app = Flask(__name__)
app.config['SECRET_KEY'] = 'MySecretKey'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ckeditor = CKEditor(app)
Bootstrap(app)


from website import routes

from .models import User

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))







