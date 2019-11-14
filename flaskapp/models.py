from . import db
from flask_login import UserMixin

from flaskapp import app

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    

    VeEntryDate = db.Column(db.Date)
    VeID = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    VeNO = db.Column(db.String(25), nullable=False)
    VendorName = db.Column(db.String(80))
    visited_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    VehicleTypeName_id = db.Column(
        db.Integer, db.ForeignKey('vehicletypes.id'))
    InTime = db.Column(db.Time)
    OutTime = db.Column(db.Time)
    TotalDuration = db.Column(db.String(25))

class VehicleTypes(db.Model):
    __tablename__ = "vehicletypes"
    id = db.Column(db.Integer, primary_key=True)
    typename = db.Column(db.String(10))
    vehicles = db.relationship('Vehicle', backref='vehicle_type')
    compnay_vehicles = db.relationship('CompanyVehicle', backref='comp_vehicle_type')


class CompanyVehicle(db.Model):
    

    __tablename__ = "companyvehicles"

    

    id = db.Column(db.Integer, primary_key=True)
    comp_vehicle_no = db.Column(db.String(20), unique=True)
    vehicle_type = db.Column(db.Integer, db.ForeignKey('vehicletypes.id'))
    model_name = db.Column(db.String(20))
    timesheet = db.relationship('CompanyTimesheet', backref='comp_timesheet')

class CompanyTimesheet(db.Model):
    __tablename__ = 'companyvehiclestime'

    

    id = db.Column(db.Integer, primary_key=True)
    comp_vehicle_id = db.Column(db.Integer, db.ForeignKey('companyvehicles.id'))
    visited_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    date = db.Column(db.Date)
    InTime = db.Column(db.Time)
    OutTime = db.Column(db.Time)
    duration = db.Column(db.String(25)) 

class Visitor(db.Model):
    __tablename__ = 'visitor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25))
    contact = db.Column(db.String(11))
    place_from = db.Column(db.String(20))
    activities = db.relationship('Activity', backref='activity')
    a_timesheet = db.relationship('Timesheet_Visitor', backref="a_timelog")
    
class Activity(db.Model):
    __tablename__ = "activity"

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    visiting_purpose = db.Column(db.String(50))
    visiting_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))
    visiting_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    timelog = db.relationship('Timesheet_Visitor', backref='active')
   

class Timesheet_Visitor(db.Model):
    __tablename__ = 'timesheet_visitor'

    id = db.Column(db.Integer, primary_key=True)
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))

class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    employees = db.relationship('Employee', backref='dept')
    activity_dept = db.relationship('Activity',  backref='visited_dept')
    outside_vehicles = db.relationship('Vehicle', backref='outside_dept')
    mill_vehicles = db.relationship('CompanyTimesheet', backref='mill_dept')

class Employee(db.Model):
    __tablename__ = "employee"
    
    id = db.Column(db.Integer, primary_key=True)
    employee_name =  db.Column(db.String(80), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    activity_emp = db.relationship('Activity' , backref='visited_employee')

class User(UserMixin ,db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(13))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def user_role(self):
        return self.role_id

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='current_role')

