from flask_sqlalchemy import SQLAlchemy
from flaskapp import db
from flaskapp import app


class Visitor(db.Model):
    __tablename__ = 'visitor'

    name = db.Column(db.String(25))
    contact = db.Column(db.String(11))
    place_from = db.Column(db.String(20))
    timesheet = db.relationship('Timesheet_Visitor', backref='timelog')
    activities = db.relationship('Activity', backref='activity')

class Activity(db.Model):
    __tablename__ = "activity"

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    visiting_purpose = db.Column(db.String(50))
    visiting_employee = db.Column(db.Integer, db.ForeignKey('employee.id'))
    visiting_department = db.Column(db.Integer, db.ForeignKey('department.id'))
    timesheet = db.relationship('Timesheet_Visitor', backref="timelog")
   

class Timesheet_Visitor(db.Model):
    __tablename__ = 'timesheet_visitor'

    visitor_id = db.Column(db.Integer, db.ForeignKey('visitor.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    date = db.Column(db.Date)
    in_time = db.Column(db.Time)
    out_time = db.Column(db.Time)
    duration = db.Column(db.String(20))