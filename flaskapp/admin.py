from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from .models import Visitor, Department, Employee, Vehicle, VehicleTypes, User, CompanyVehicle
from flask_login import login_required
from . import db


admin = Blueprint('admin', __name__)


#Main Page Render Function
@admin.route('/admin')
@login_required
def admin_main():
    vehicle_types = VehicleTypes.query.all()
    departments = Department.query.all()    
    employees = Employee.query.all()
    users = User.query.all()
    company_vehicles = CompanyVehicle.query.all()
    visitors = Visitor.query.all()
    return render_template('admin.html',visitors=visitors,
        company_vehicles=company_vehicles, vehicle_types=vehicle_types, 
        departments=departments, employees=employees, users=users)


#Add new Departments
@admin.route('/admin/post', methods=['POST'])
def admin_dept():
    if request.form:

        name = request.form.get('deptname').upper()
        dept = Department.query.filter_by(department_name=name).first()

        if dept is None:
            department = Department(department_name=name)
            db.session.add(department)
            db.session.commit()
            flash('Department Added')
            return redirect(url_for('admin.admin_main'))
        else:   
            flash('Department Already Exists')
            return redirect(url_for('admin.admin_main'))


#Delete Functions for Most of Admin Masters (Departments, Employees, Vehicles, Users)
@admin.route('/admin/delete', methods=['POST'])
def admin_delete():
    dept_id = request.form.get('dept_id')
    employee_id = request.form.get('employee_id')
    types_id = request.form.get('types_id')
    comp_v_id = request.form.get('comp_v_id')
    if dept_id:
        dept = Department.query.filter_by(id=dept_id).first()
        db.session.delete(dept)
        db.session.commit()
        flash('Department Deleted')
        return redirect(url_for('admin.admin_main'))
    elif employee_id:
        employee = Employee.query.filter_by(id=employee_id).first()
        db.session.delete(employee)
        db.session.commit()
        flash('Employee Deleted')
        return redirect(url_for('admin.admin_main'))
    elif types_id:
        vehicle_type = VehicleTypes.query.filter_by(id=types_id).first()
        db.session.delete(vehicle_type)
        db.session.commit()
        flash('Vehicle Type Deleted')
        return redirect(url_for('admin.admin_main'))
    elif comp_v_id:
        vehicle = CompanyVehicle.query.filter_by(id=comp_v_id).first()
        db.session.delete(vehicle)
        db.session.commit()
        flash('Company vehicle Deleted ')
        return redirect(url_for('admin.admin_main'))


#Add new Employee to a Particular Department
@admin.route('/admin/post/employee', methods=['POST'])
def admin_employee():
    if request.form:
        name = request.form.get('employeename').upper()
        department = request.form.get('current_department')
        employee = Employee.query.filter_by(employee_name=name).first()
        
        if employee is None:
            employee = Employee(employee_name=name, department_id=department)
            db.session.add(employee)
            db.session.commit()
            flash('Employee Added') 
            return redirect(url_for('admin.admin_main'))
        else:
            flash('Employee Already Exists')
            return redirect(url_for('admin.admin_main'))

     
#Add new Vehicle Type
@admin.route('/admin/post/vehicletype', methods=['POST'])
def admin_vehicletype():
    if request.form:
        type_name = request.form.get('vehicletype').upper()
        check_type = VehicleTypes.query.filter_by(typename=type_name).first()
        if check_type is None:
            types = VehicleTypes(typename=type_name)
            db.session.add(types)
            db.session.commit()
            flash('Vehicle Type Added')
            return redirect(url_for('admin.admin_main'))
        else:
            flash('VehicleType already Exists')
        return redirect(url_for('admin.admin_main'))


#Add new Company Vehicle 
@admin.route('/admin/post/compnayvehicles', methods=['POST'])
def admin_company_vehicles():
    if request.form:
        vehicle = CompanyVehicle(comp_vehicle_no=request.form.get('vehicleno').upper(), 
            vehicle_type=int(request.form.get('vehicletype')),
            model_name=request.form.get('modelname').upper())
        db.session.add(vehicle)
        db.session.commit()
        flash('Company Vehicle Added')
        return redirect(url_for('admin.admin_main'))


#Add new User
@admin.route('/admin/post/user', methods=['POST'])
def admin_user():
    if request.form:
        username = request.form.get('username')
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('admin.admin_main'))