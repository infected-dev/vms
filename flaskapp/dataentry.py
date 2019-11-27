from datetime import datetime, timedelta
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from .cust_functions import convert, minutes, timeobj
from .models import Department, Vehicle, Visitor,Activity,Timesheet_Visitor, Employee, VehicleTypes, CompanyVehicle, CompanyTimesheet
from . import db


dataentry = Blueprint('dataentry', __name__)


#New Mill Vehicle Time Record Function
@dataentry.route('/vehicles/mill', methods=['POST'])
def mill_vehicles():
    if request.form:
        entrydate = datetime.strptime(
                        request.form.get('entry_date'), '%Y-%m-%d').date()
        OutTime = datetime.strptime(
                        request.form.get('outime'), '%H:%M').time()
        department_id = int(request.form.get('dept'))
        comp_vehicle_time = CompanyTimesheet(
                        comp_vehicle_id=int(request.form.get('comp_id')),visited_department=department_id, date=entrydate, OutTime=OutTime)
        db.session.add(comp_vehicle_time)
        db.session.commit()
        flash('Compnay Vehicle Time Noted')
        return redirect(url_for('dataentry.post_mill'))


#Update Existsing Mill Vehicle Time Record InTime
@dataentry.route('/vehicles/mill/update', methods=['POST'])
def mill_vehicles_update():
    if request.form:
        comp_id = int(request.form['vid'])
        compnay_vehicle = CompanyTimesheet.query.filter_by(id=comp_id).first()
        duration = compnay_vehicle.duration
        InTime = datetime.strptime(request.form['intime'], '%H:%M').time() 
        compnay_vehicle.InTime = InTime
        db.session.commit()
        if duration == None or 'none':
                intime = compnay_vehicle.InTime
                outtime = compnay_vehicle.OutTime
                diff = timeobj(outtime, intime)
                compnay_vehicle.duration = diff
                db.session.commit()
        return jsonify({'status':'OK'})


#New Outside Vehicle Time Record Function
@dataentry.route('/vehicles', methods=['POST'])
def vehicles_post():
            entrydate = datetime.strptime(
                request.form.get('entry_date'), '%Y-%m-%d').date()
            InTime = datetime.strptime(request.form.get('intime'), '%H:%M').time()
            VeNO = request.form.get('veno')
            VeNO = VeNO.upper()
            comp_vehs = CompanyVehicle.query.all()
            department_id = int(request.form.get('dept'))
            comp_vehs_list = [c.comp_vehicle_no for c in comp_vehs]
            if VeNO[-6:] in comp_vehs_list:
                flash('Add Vehicle in Company Timesheet')
                return redirect(url_for('dataentry.post_vehicles'))
            else:
                vehicle = Vehicle(VeEntryDate=entrydate, VeNO=VeNO, VehicleTypeName_id=request.form.get(
                    'vehicletype'), VendorName=request.form.get('vendorname').upper(),
                    visited_department=department_id, InTime=InTime, TotalDuration='none')
                db.session.add(vehicle)
                db.session.commit()
                flash('New Vehicle Added')
            return redirect(url_for('dataentry.post_vehicles'))


#Update Exisiting Outside Vehicle Time Record InTime
@dataentry.route('/vehicles/update', methods=['POST'])
def update_vehicle():
    if request.form:
        vid = request.form['VeID']
        vehicle = Vehicle.query.filter_by(VeID=vid).first()
        duration = vehicle.TotalDuration
        outtime = datetime.strptime(
                request.form['outtime'], '%H:%M').time()
        vehicle.OutTime = outtime
        db.session.commit()
        if duration == None or 'none':
                intime = vehicle.InTime
                outtime = vehicle.OutTime
                diff = timeobj(intime, outtime)
                vehicle.TotalDuration = diff
                db.session.commit()             
        return jsonify({'status': 'OK'})

#Updating Department and outtime backdate
@dataentry.route('/vehicles/update/dept', methods=['POST'])
def update_vehicle_dept():
    if request.form:
            id = request.form.get('oid')
            dept = int(request.form.get('dept'))
            outtime = request.form.get('out_time')
            if outtime:
                outtime = datetime.strptime(outtime, '%H:%M').time()
            vehicle = Vehicle.query.get(id)
            vehicle.visited_department = dept
            if outtime:
                vehicle.OutTime = outtime  
            db.session.commit()
            if vehicle.OutTime != None or 'none':
                intime = vehicle.InTime
                outtime = vehicle.OutTime
                diff = timeobj(intime, outtime)
                vehicle.TotalDuration = diff
                db.session.commit()
            return jsonify({'status':'ok'})


#Updating Deoartment of mill vehicles
@dataentry.route('/vehicles/mill/update/dept', methods=['POST'])
def update_mill_dept():
    if request.form:
            id = request.form.get('oid')
            
            dept = int(request.form.get('dept'))
           
            timelog = CompanyTimesheet.query.get(id)
            timelog.visited_department = dept
            db.session.commit()
            return jsonify({'status':'ok'})

#Delete Exsisiting Outside Vehicle Record
@dataentry.route('/vehicles/delete', methods=['POST'])
def delete_vehicles():
    vid = int(request.form.get('vid'))
    vehicle = Vehicle.query.filter_by(VeID=vid).first()
    db.session.delete(vehicle)
    db.session.commit()
    flash('Outside Vehicle Record Deleted')
    return redirect(url_for('dataentry.post_vehicles'))

@dataentry.route('/vehicles/mill/delete', methods=['POST'])
def delete_mill():
    vid = int(request.form.get('vid'))
    vehicle = CompanyTimesheet.query.filter_by(id=vid).first()
    db.session.delete(vehicle)
    db.session.commit()
    flash('Mill Vehicle Record Deleted')
    return redirect(url_for('dataentry.post_mill'))


#Main Page Render Function for Visitor Data Entry
@dataentry.route('/DataentryVisitor', methods=['GET','POST'])
def post_format():
    today_date = datetime.now().date()
    today_time = (datetime.now().time()).strftime("%H:%M")
    today_visitors = Timesheet_Visitor.query.filter_by(date=today_date).all()
    
    employees = Employee.query.all()
    types = VehicleTypes.query.all()
    visitors = Visitor.query.all()
    return render_template('dataentry-visitors.html', today_time=today_time, 
        today_date=today_date, types=types, employees=employees, 
        today_visitors=today_visitors, visitors=visitors)

#Main Page Render Function for Outside Vehicle DataEntry
@dataentry.route('/DataentryVehicle')
def post_vehicles():
    today_date = datetime.now().date()
    yesterday = today_date - timedelta(days=1)
    today_time = (datetime.now().time()).strftime("%H:%M")
    today_vehicles = Vehicle.query.filter_by(VeEntryDate=yesterday).all()
    types = VehicleTypes.query.all()
    departments = Department.query.all()
    return render_template('dataentry-vehicle.html',departments=departments, today_vehicles=today_vehicles,today_date=yesterday,today_time=today_time, types=types)


#Main Page Render Function for Mill Vehicle DataEntry
@dataentry.route('/DataentryVehicle/mill')
def post_mill():
    today_date = datetime.now().date()
    yesterday = today_date - timedelta(days=1)
    today_time = (datetime.now().time()).strftime("%H:%M")
    comp_vehicles = CompanyVehicle.query.all()  
    comp_vehicles_today = CompanyTimesheet.query.filter_by(date=yesterday).all()
    departments = Department.query.all()
    return render_template('dataentry-mill.html',departments=departments, today_date=yesterday, today_time=today_time, comp_vehicles=comp_vehicles, comp_vehicles_today=comp_vehicles_today)


#New Visitor DataEntry Function
@dataentry.route('/test-postformat/visitor', methods=['POST'])
def visitors_post():
   if request.form:
       name = request.form.get('visitorname').upper()
       contact = request.form.get('visitorcontact')
       place_from = request.form.get('visitorcompany')
       #Checks if the Visitor Already existis in the master, if it does only the id is taken over
       if Visitor.query.filter_by(contact=contact).first():
           visitor = Visitor.query.filter_by(contact=contact).first()
       else:
           #Adds new Visitor if it doesnt exist
            visitor = Visitor(name=name, contact=contact, place_from=place_from)
            db.session.add(visitor)
            db.session.commit()
        
       employee_id = Employee.query.get(int(request.form.get('visiting_employee')))
       emp_id = employee_id.id
       department_id = employee_id.department_id
       visiting_purpose = request.form.get('visitingpurpose')
       activity = Activity(visitor_id=visitor.id, visiting_purpose=visiting_purpose,
            visiting_employee=emp_id, visiting_department=department_id)
       db.session.add(activity)
       db.session.commit()

       date = datetime.strptime(request.form.get('entrydate'), '%Y-%m-%d').date()
       time = datetime.strptime(request.form.get('intime'), '%H:%M').time()
       extras = 0
       if request.form.get('extras'):
           extras = int(request.form.get('extras'))
       timelog = Timesheet_Visitor(visitor_id=visitor.id, activity_id=activity.id, extras=extras , date=date, in_time=time)
       db.session.add(timelog)
       db.session.commit()
       return redirect(url_for('dataentry.post_format'))    

#Update Exsisting Visitor Record OutTime
@dataentry.route('/visitors/update', methods=['POST'])
def visitors_update():
    if request.form:
        vid = request.form['vi_id']
        visitor = Timesheet_Visitor.query.filter_by(id=vid).first()
        duration = visitor.duration
        exittime = datetime.strptime(
            request.form['exittime'], '%H:%M').time()
        visitor.out_time = exittime
        db.session.commit()
        if (duration == None or 'none'):
            intime = visitor.in_time
            outtime = visitor.out_time
            diff = timeobj(intime, outtime)
            visitor.duration = diff
            db.session.commit()
    return jsonify({'status':'ok'})


#Delete Exsisting Visitor Record
@dataentry.route('/visitors/delete', methods=['POST'])
def visitors_delete():
    
    vid = int(request.form.get('vi_id'))
    page = request.form.get('page')
    visitor = Timesheet_Visitor.query.get(vid)
    db.session.delete(visitor)
    db.session.commit()
    if page == 'dataentry':
        return redirect(url_for('dataentry.post_format'))
    else:
        return redirect(url_for('report.report_main'))
