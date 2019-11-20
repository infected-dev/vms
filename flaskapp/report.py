from flask import Blueprint, render_template, request, url_for, redirect, flash
from .models import Vehicle, Visitor, Department, CompanyTimesheet, CompanyVehicle, Timesheet_Visitor, Activity
from datetime import datetime, timedelta
from flaskapp import db


report = Blueprint('report', __name__)

@report.route('/dashbaord')
def dashboard():
    today = datetime.now().date()
    ## Daily Vehicles and Visitors Count ##
    
    query_visitors_today = Timesheet_Visitor.query.filter_by(date=today).count()
    
    ## All Vheicles and Visitor Count ##
    activitiy = Activity.query.all()
    query_visitors_all = Timesheet_Visitor.query.count()

    ## Department Count Queries ##
    departments = { d.id : d.department_name for d in Department.query.all() } 
    dept_count = []
    for i in departments:
        count = Activity.query.filter_by(visiting_department=i).count()
        dept_count.append([departments[i], count])

    ## Date Wise Count Queries for charts ##

    legend = 'Total Visitors by Date'
    dates = [r.date for r in db.session.query(Timesheet_Visitor.date).distinct()]
    total_count = []
    for i in dates: 
        count = Timesheet_Visitor.query.filter_by(date=i).count()
        total_count.append([i.strftime("%d/%m/%Y"), count])


    ## departmentwise Count Queries for charts ##
    
    

    return render_template('dashboard-visitors.html',legend=legend, total_count=total_count, 
        query_visitors_all=query_visitors_all, query_visitors_today=query_visitors_today, dept_count=dept_count)

@report.route('/dashbaord/vehicles')
def dashboard_vehicle():
    today = datetime.now().date()
    ## Daily Vehicles and Visitors Count ##
    query_vehicles_today = Vehicle.query.filter_by(VeEntryDate=today).count()
    query_vehicles_all = Vehicle.query.count()

    legend = 'Total Outside Vehicles by Date'
    dates = [r.VeEntryDate for r in db.session.query(Vehicle.VeEntryDate).distinct()]
    total_count = []
    for i in dates: 
        count = Vehicle.query.filter_by(VeEntryDate=i).count()
        total_count.append([i.strftime("%d/%m/%Y"), count])


    return render_template('dashboard-vehicles.html',legend=legend, total_count=total_count, query_vehicles_all=query_vehicles_all, 
        query_vehicles_today=query_vehicles_today)


@report.route('/report/visitors')
def report_main():
    error = None
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    departments = Department.query.all()
    date = yesterday
    visitors = Timesheet_Visitor.query.all()
    vehicles = Vehicle.query.all()
    return render_template('report-visitors.html',departments=departments, date=date.strftime('%d-%b-%Y')
    , visitors=visitors, vehicles=vehicles, error=error)

@report.route('/report/vehicles')
def report_vehicles():
    depts = Department.query.all()
    query_vehicles_outside = Vehicle.query.all()
    return render_template('report-vehicles.html',query_vehicles_outside=query_vehicles_outside, 
       depts=depts)

@report.route('/report/vehicles/mill/')
def mill_report():
    if request.args:
        query_vehicles_mill = CompanyTimesheet.query.all()  
        query_comp_vehicles = CompanyVehicle.query.all()    
        comp_veh_id = request.args['comp_vehicle']
        comp_vehicle = CompanyVehicle.query.get(comp_veh_id)
        timesheet= comp_vehicle.timesheet   
        return render_template('report-mill.html',timesheet=timesheet,query_comp_vehicles=query_comp_vehicles,
        query_vehicles_mill=query_vehicles_mill,
       )
    depts = Department.query.all()
    query_vehicles_mill = CompanyTimesheet.query.all()
    query_comp_vehicles = CompanyVehicle.query.all()
    return render_template('report-mill.html',depts=depts, query_comp_vehicles=query_comp_vehicles, 
        query_vehicles_mill=query_vehicles_mill)

@report.route('/print-report', methods=['POST'])
def report_print():
    count = 0
    if request.form:
        print_id = request.form.get('printid')
        date = datetime.strptime(
                request.form.get('date'), '%Y-%m-%d').date()
        if print_id == '1':
            title = 'Visitor Records'
            query = Timesheet_Visitor.query.filter_by(date=date).all()
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
        elif print_id == '8':
            title = 'Visitor Records Sorted by Employee Visited'
            query = Timesheet_Visitor.query.filter_by(date=date).all()
            count = len(query)
            return render_template('report-visitors-print.html',count=count, query=query, date=date, title=title)
        elif print_id == '10':
            title = 'Visitor Records Sorted By Department'
            query = Timesheet_Visitor.query.filter_by(date=date).all()
            count = len(query)
            return render_template('report-visitors-print.html',count=count, query=query, date=date, title=title)
        elif print_id == '9': 
            dept_check = request.form.get('deptcheck')
            if dept_check:
                title = 'Visitor Records Sorted by Department'
                query = Timesheet_Visitor.query.filter_by(date=date).all()
                count = len(query)
                return render_template('report-visitors-print.html',count=count, query=query, date=date, title=title)
            else:
                department_id = int(request.form.get('department'))
                department = Department.query.get(department_id)
                query = Timesheet_Visitor.query.filter_by(date=date).all()
                filtered_list = []
                for i in query:
                    if i.active.visiting_department == department_id:
                        filtered_list.append(i)
                title = 'Visitors Records by Department'
                count = len(filtered_list)
            
                return render_template('report-visitors-print.html',department=department, title=title, count=count, 
                    filtered_list=filtered_list, date=date)


@report.route('/print-slip', methods=['POST'])
def printslip():
    if request.form:
        get_id = int(request.form.get('vi_id'))
        visitor = Timesheet_Visitor.query.filter_by(id=get_id).first()
        return render_template('print-visitor-slip.html', visitor=visitor)        