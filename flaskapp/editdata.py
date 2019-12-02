from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from .cust_functions import convert, minutes, timeobj
from .models import Department, Vehicle, Visitor,Activity,Timesheet_Visitor, Employee, VehicleTypes, CompanyVehicle, CompanyTimesheet
from . import db


edit = Blueprint('edit', __name__)


#Main Page Render for Editing vistor data
@edit.route('/editVistor', methods=['GET','POST'])
def edit_visitor():
    backdate_visitors = ''
    emps = Employee.query.all()
    if request.form:
        selected_date = request.form.get('selected_date')
        date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        backdate_visitors = Timesheet_Visitor.query.filter_by(date=date).all()
    return render_template('edit-Visitor.html', backdate_visitors=backdate_visitors,emps=emps)


#Editing department route for visitor
@edit.route('/editVisitor/Department', methods=['POST'])
def edit_visitordepart():
    if request.form:
        emp_id = int(request.form.get('emp_id'))
        emp = Employee.query.get(emp_id)
        emp_dept = emp.department_id

        time_id = int(request.form.get('t_id'))
        timesheet_id = Timesheet_Visitor.query.get(time_id)
        
        activity_id = timesheet_id.activity_id
        activity = Activity.query.get(activity_id)
        activity.visiting_employee = emp_id
        activity.visiting_department = emp_dept
        db.session.commit()
        return jsonify({'status':'ok'})


#Main Page Render for Outside Vehicles
@edit.route('/editOutsidevehicle', methods=['GET','POST'])
def edit_outsideVehicle():
    backdate_vehicles = ''
    if request.form:
        selected_date = request.form.get('selected_date')
        date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        backdate_vehicles = Vehicle.query.filter_by(VeEntryDate=date).all()
    return render_template('edit-outsideVehicle.html',  backdate_vehicles=backdate_vehicles)


#Main Page Render for Mill Vehicles
@edit.route('/editMillVehicle', methods=['GET','POST'])
def edit_millVehicle():
    backdate_mill = ''
    if request.form:
        selected_date = request.form.get('selected_date')
        date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        backdate_mill = CompanyTimesheet.query.filter_by(date=date).all()
    return render_template('edit-millVehicle.html',backdate_mill=backdate_mill)

@edit.route('/editVisitorMaster', methods=['POST'])
def edit_visitorMaster():
    if request.form:
        vid = request.form.get('vid')
        name = request.form.get('vname')
        contact = request.form.get('vcontact')
        place = request.form.get('vplace')
        visitor = Visitor.query.get(vid)
        
        if name:
            visitor.name = name
            db.session.commit()
            
        if contact:
            visitor.contact = contact
            db.session.commit()
            
        if place:
            visitor.place_from = place
            db.session.commit()
    return jsonify({'status':'ok'})
