from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Vehicle, Visitor, Department, CompanyTimesheet, CompanyVehicle
from datetime import datetime, timedelta
from flaskapp import db


report = Blueprint('report', __name__)

@report.route('/dashbaord')
def dashboard():
    today = datetime.now().date()
    ## Daily Vehicles and Visitors Count ##
    
    query_visitors_today = Visitor.query.filter_by(entry_date=today).count()
    
    ## All Vheicles and Visitor Count ##
    
    query_visitors_all = Visitor.query.count()
    ## Department Count Queries ##
    query_department_all = Department.query.all()
    query_department_visitor = [(d.department_name, len(d.visitors)) for d in query_department_all]
    ## Date Wise Count Queries ##
    legend = 'Total Visitors by Date'
    dates = [r.entry_date for r in db.session.query(Visitor.entry_date).distinct()]
    total_count = []
    for i in dates: 
        count = Visitor.query.filter_by(entry_date=i).count()
        total_count.append([i.strftime("%d/%m/%Y"), count])

    return render_template('test-dashboard-front.html',legend=legend, total_count=total_count, query_department_visitor=query_department_visitor, 
        query_visitors_all=query_visitors_all, query_visitors_today=query_visitors_today)

@report.route('/dashbaord/vehicles')
def dashboard_vehicle():
    today = datetime.now().date()
    ## Daily Vehicles and Visitors Count ##
    query_vehicles_today = Vehicle.query.filter_by(VeEntryDate=today).count()
    query_vehicles_all = Vehicle.query.count()
    return render_template('dashboard-vehicles.html', query_vehicles_all=query_vehicles_all, query_vehicles_today=query_vehicles_today)


@report.route('/test-dashboard-report/')
def report_main():
    error = None
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    query_visitors_date = Visitor.query.filter_by(entry_date=yesterday).all()
    date = yesterday
    
    if request.args:
        date = request.args['date']
        date = datetime.strptime(date, '%Y-%m-%d').date()
        query_visitors_date = Visitor.query.filter_by(entry_date = date).all()
        

    visitors = Visitor.query.all()
    vehicles = Vehicle.query.all()
    return render_template('test-dashbaord-report_visitor.html', date=date.strftime('%d-%b-%Y')
    , visitors=visitors, vehicles=vehicles, error=error, query_visitors_date=query_visitors_date)

@report.route('/test-dashboard-report/vehicles/')
def report_vehicles():

    if request.args:
        query_vehicles_mill = CompanyTimesheet.query.all()
        query_vehicles_outside = Vehicle.query.all()
        query_comp_vehicles = CompanyVehicle.query.all()    
        comp_veh_id = request.args['comp_vehicle']
        comp_vehicle = CompanyVehicle.query.get(comp_veh_id)
        timesheet= comp_vehicle.timesheet
        return render_template('test-dashbaord-report_vehicle.html',timesheet=timesheet,query_comp_vehicles=query_comp_vehicles,
        query_vehicles_mill=query_vehicles_mill,
        query_vehicles_outside=query_vehicles_outside 
       )
       
    query_vehicles_mill = CompanyTimesheet.query.all()
    query_vehicles_outside = Vehicle.query.all()
    query_comp_vehicles = CompanyVehicle.query.all()

    return render_template('test-dashbaord-report_vehicle.html',query_comp_vehicles=query_comp_vehicles,
        query_vehicles_mill=query_vehicles_mill,
        query_vehicles_outside=query_vehicles_outside 
       )

@report.route('/print-report', methods=['POST'])
def report_print():
    count = 0
    if request.form:
        print_id = request.form.get('printid')
        date = datetime.strptime(
                request.form.get('date'), '%Y-%m-%d').date()
        if print_id == '1':
            title = 'Visitor Records'
            query = Visitor.query.filter_by(entry_date=date).all()
            count = len(query)
            return render_template('report-visitors-print.html',count=count, query=query, date=date, title=title)
        elif print_id == '2':
            title = 'Outside Vehicle Records'
            query = Vehicle.query.filter_by(VeEntryDate=date).all()
            count = len(query)
            return render_template('report-vehicles-print.html', query=query,count=count, title=title, date=date)
        elif print_id == '3':
            title = 'Mill Vehicle Records'
            query = CompanyTimesheet.query.filter_by(date=date).all()
            count = len(query)
            return render_template('report-vehicles-print.html', query=query, title=title,count=count, date=date)


@report.route('/print-slip', methods=['POST'])
def printslip():
    if request.form:
        get_id = int(request.form.get('vi_id'))
        visitor = Visitor.query.filter_by(id=get_id).first()
        return render_template('printformat.html', visitor=visitor)        