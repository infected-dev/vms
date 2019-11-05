from flask import Blueprint, render_template
from .models import User


base = Blueprint('base', __name__)

@base.route('/')
def index():
    users = User.query.all()
    return render_template('signin.html', users=users) 


    
