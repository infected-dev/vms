from flask import Blueprint, render_template, redirect, url_for, request, flash
from flaskapp.models import Visitor, Vehicle, CompanyTimesheet, CompanyVehicle, Timesheet_Visitor
from flaskapp import db
from datetime import datetime

search = Blueprint('search', __name__)

@search.route('/search')
def search_main():
    if request.args:
       text_search = request.args['text-search'].upper().rstrip()
       
      
       if text_search == '':
            flash('enter valid text')
            redirect(url_for('dataentry.post_format'))
       else:
                error = ''
                search_visitor = Visitor.query.filter((Visitor.name.like('%{}%'.format(text_search)))| (Visitor.contact == text_search)).first()
                search_visitor_timesheet = ''
                if search_visitor == None:
                    error = 'No Result Found'
                else:
                    search_visitor_timesheet = Timesheet_Visitor.query.filter_by(visitor_id=search_visitor.id).all()
                    
                search_vehicle = Vehicle.query.filter_by(VeNO=text_search).first()
                search_mill = CompanyVehicle.query.filter_by(comp_vehicle_no=text_search.upper()).first()
                return render_template('search-results.html',text_search=text_search, 
                    search_visitor=search_visitor, search_vehicle=search_vehicle, 
                    search_mill=search_mill, search_visitor_timesheet=search_visitor_timesheet, error=error)
    return render_template('search-results.html', text_search=text_search)


@search.route('/clear')
def search_clear():
    return redirect(url_for('dataentry.post_format'))
