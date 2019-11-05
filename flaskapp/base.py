from flask import Blueprint, render_template
from .models import User
from . import db
from flaskapp import excel

base = Blueprint('base', __name__)

@base.route('/')
def index():
    users = User.query.all()
    return render_template('signin.html', users=users) 

@base.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1,2], [3, 4]], "csv",
                                          file_name="export_data")
    
