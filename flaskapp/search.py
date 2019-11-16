from flask import Blueprint, render_template, redirect, url_for, request, flash
from flaskapp.models import Visitor, Vehicle, CompanyTimesheet, CompanyVehicle
from flaskapp import db
from datetime import datetime

search = Blueprint('search', __name__)

@search.route('/search')
def search_main():
    if request.args:
       text_search = request.args['text-search'].upper()
       

       if text_search == '':
            flash('enter valid text')
            redirect(url_for('dataentry.post_format'))
       else:
            if text_search[-1] == '+':
                text_search = text_search.strip('+')
                search_visitor = Visitor.query.filter((Visitor.visitor_name == text_search) | (Visitor.visitor_contact == text_search)).all()
                search_vehicle = Vehicle.query.filter_by(VeNO=text_search).first()
                search_mill = CompanyVehicle.query.filter_by(comp_vehicle_no=text_search.upper()).first()
                return render_template('search-results.html',text_search=text_search, 
                    search_visitor=search_visitor, search_vehicle=search_vehicle, 
                    search_mill=search_mill)
            else:
                search_visitor = Visitor.query.filter((Visitor.visitor_name == text_search) | (Visitor.visitor_contact == text_search)).all()
                search_vehicle = Vehicle.query.filter_by(VeNO=text_search).first()
                search_mill = CompanyVehicle.query.filter_by(comp_vehicle_no=text_search.upper()).all()
                count = 0
                if search_visitor:
                    count = len(search_visitor)
                elif search_vehicle:
                    count = len(search_vehicle)
                elif search_mill:
                    count = len(search_mill)
                
                return render_template('search-results.html', count=count,text_search=text_search, 
                    search_visitor=search_visitor, search_vehicle=search_vehicle, 
                    search_mill=search_mill)  
    return render_template('search-results.html', text_search=text_search)


@search.route('/clear')
def search_clear():
    return redirect(url_for('dataentry.post_format'))
