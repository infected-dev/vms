from . import db
from flask_login import UserMixin

from flaskapp import app

class Vehicle(db.Model):
    __tablename__ = "vehicles"

    

    VeEntryDate = db.Column(db.Date)
    VeID = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    VeNO = db.Column(db.String(25), nullable=False)
    VendorName = db.Column(db.String(80))
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
    date = db.Column(db.Date)
    InTime = db.Column(db.Time)
    OutTime = db.Column(db.Time)
    duration = db.Column(db.String(25)) 

class Visitor(db.Model):
    __tablename__ = "visitor"

    

    id = db.Column(db.Integer, primary_key=True)
    visitor_name = db.Column(db.String(80), nullable=False)
    visitor_contact = db.Column(db.Integer, nullable=False)
    visitor_company = db.Column(db.String(80), nullable=False)
    visiting_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    visiting_person = db.Column(db.Integer, db.ForeignKey('employee.id'))
    visiting_purpose = db.Column(db.String(100), nullable=False)
    entry_date = db.Column(db.Date)
    entry_time = db.Column(db.Time)
    exit_time = db.Column(db.Time)
    total_duration = db.Column(db.String(25))


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(80), nullable=False)
    employees = db.relationship('Employee', backref='dept')
    visitors = db.relationship('Visitor',  backref='visited_dept')

class Employee(db.Model):
    __tablename__ = "employee"
    
    id = db.Column(db.Integer, primary_key=True)
    employee_name = db.Column(db.String(80), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    visitors = db.relationship('Visitor' , backref='visited_employee')

class User(UserMixin ,db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True)
    password = db.Column(db.String(13))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(10), unique=True)
    users = db.relationship('User', backref='current_role')

