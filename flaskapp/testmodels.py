from flask_sqlalchemy import SQLAlchemy
from flaskapp import db
from flaskapp import app


class Visitor(db.Model):
    __tablename__ = 'visitor'

    name = db.Column(db.String(25))
    contact = db.Column(db.String(11))
    place_from = db.Column(db.String(20))
    timesheet = db.relationship('Timesheet_Visitor_Log', backref='timelog')


class Timesheet_Visitor(db.Model):
    __tablename__ = 'timesheet_visitor'

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    purpose = db.Column(db.String(50))
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))

   
class Timesheet_Visitor_Log(db.Model):
    __tablename__ = 'timesheet_visitor_log'

    timesheet_id = db.Column(db.Integer, db.ForeignKey('timesheet_visitor.id'))
    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))


class Outsidevehicle(db.Model):
    __tablename__ = 'outsidevehicle'

    vehicle_no = db.Column(db.String(20), unique=True)
    vehicle_type = db.Column(db.Integer, db.ForeignKey('vehicletype.id'))
    vendor = db.Column(db.String(20))
    timesheet = db.relationship('Timesheet_OutsideVehicle_Log', backref='timelog')


class Timesheet_Outsidevehicle(db.Model):
    __tablename__='timesheet_outsidevehicle'

    vehicle_id = db.Column(db.Integer, db.ForeignKey('OutsideVehicle.id'))
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))


class Timesheet_Outsidevehicle_Log(db.Model):
    __tablename__ = 'timesheet_outsidevehicle_log'

    vehicle_id = db.Column(db.Integer, db.ForeignKey('outsidevehicle.id'))
    timesheet_id = db.Column(db.Integer, db.ForeignKey('timesheet_outsidevehicle.id'))


class CompanyVehicle(db.Model):
    __tablename__ = 'companyvehicle'

    vehicle_no = db.Column(db.String(20), unique=True)
    vehicle_type = db.Column(db.Integer, db.ForeignKey('vehicletype.id'))
    vendor = db.Column(db.String(20))
    timesheet = db.relationship('Timesheet_CompanyVehicle_Log', backref='timelog')
 

class Timesheet_CompanyVehicle(db.Model):
    __tablename__='timesheet_compnayvehicle'

    vehicle_id = db.Column(db.Integer, db.ForeignKey('companyvehicle.id'))
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))


class Timesheet_CompanyVehicle_Log(db.Model):
    __tablename__ = 'timesheet_CompanyVehicle_log'

    vehicle_id = db.Column(db.Integer, db.ForeignKey('outsidevehicle.id'))
    timesheet_id = db.Column(db.Integer, db.ForeignKey('timesheet_companyvehicle.id'))