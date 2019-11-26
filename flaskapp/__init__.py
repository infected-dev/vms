from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



db = SQLAlchemy()
login_manager = LoginManager()




app = Flask(__name__)


app.config['SECRET_KEY'] = 'laxmikapatihume'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


db.init_app(app)



login_manager.init_app(app)
login_manager.login_view = 'auth.login_main'
login_manager.login_message = "Please Sign in Before Accessing this page"


from .models import User


@login_manager.user_loader
def load_user(User_id):
     return User.query.get(int(User_id))


from .base import base as base_blueprint
app.register_blueprint(base_blueprint)


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)


from .search import search as search_blueprint
app.register_blueprint(search_blueprint)


from .dataentry import dataentry as dataentry_blueprint
app.register_blueprint(dataentry_blueprint)


from .report import report as report_blueprint
app.register_blueprint(report_blueprint)

from.editdata import edit as edit_blueprint
app.register_blueprint(edit_blueprint)



if __name__ == '__main__':
     app.jinja_env.cache = {}
     app.run()
     
