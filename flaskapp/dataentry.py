from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from .cust_functions import convert, minutes, timeobj
from datetime import datetime
from .models import Vehicle, Visitor, Employee, VehicleTypes, CompanyVehicle, CompanyTimesheet
from . import db

dataentry = Blueprint('dataentry', __name__)

@dataentry.route('/vehicles/mill', methods=['POST'])
def mill_vehicles():
    if request.form:
        entrydate = datetime.strptime(
                        request.form.get('entry_date'), '%Y-%m-%d').date()
        OutTime = datetime.strptime(
                        request.form.get('outime'), '%H:%M').time()

        comp_vehicle_time = CompanyTimesheet(
                        comp_vehicle_id=int(request.form.get('comp_id')), date=entrydate, OutTime=OutTime)
        db.session.add(comp_vehicle_time)
        db.session.commit()
        flash('Compnay Vehicle Time Noted')
        return redirect(url_for('dataentry.post_vehicles'))
    
@dataentry.route('/vehicles/mill/update', methods=['POST'])
def mill_vehicles_update():
    if request.form:
        comp_id = int(request.form.get('vid'))
        compnay_vehicle = CompanyTimesheet.query.filter_by(id=comp_id).first()
        duration = compnay_vehicle.duration
        InTime = datetime.strptime(request.form.get('intime'), '%H:%M').time() 
        compnay_vehicle.InTime = InTime
        db.session.commit()
        flash('InTime Updated!')
        if duration == None or 'none':
                intime = compnay_vehicle.InTime
                outtime = compnay_vehicle.OutTime
                diff = timeobj(outtime, intime)
                compnay_vehicle.duration = diff
                db.session.commit()
        return redirect(url_for('dataentry.post_vehicles'))

@dataentry.route('/vehicles', methods=['POST'])
def vehicles_post():
            entrydate = datetime.strptime(
                request.form.get('entry_date'), '%Y-%m-%d').date()
            InTime = datetime.strptime(request.form.get('intime'), '%H:%M').time()
            VeNO = request.form.get('veno')
            VeNO = VeNO.upper()
            comp_vehs = CompanyVehicle.query.all()
            comp_vehs_list = [c.comp_vehicle_no for c in comp_vehs]
            if VeNO[-6:] in comp_vehs_list:
                flash('Add Vehicle in Company Timesheet')
                return redirect(url_for('dataentry.post_vehicles'))
            else:
                vehicle = Vehicle(VeEntryDate=entrydate, VeNO=VeNO, VehicleTypeName_id=request.form.get(
                    'vehicletype'), VendorName=request.form.get('vendorname').upper(), InTime=InTime, TotalDuration='none')
                db.session.add(vehicle)
                db.session.commit()
                flash('New Vehicle Added')
            return redirect(url_for('dataentry.post_vehicles'))


@dataentry.route('/vehicles/update', methods=['POST'])
def update_vehicle():
    if request.form:
        vid = request.form.get('vid')
        vehicle = Vehicle.query.filter_by(VeID=vid).first()
        vendor = vehicle.VendorName
        duration = vehicle.TotalDuration
        if (vendor != 'MILL'):
            outtime = datetime.strptime(
                request.form.get('outtime'), '%H:%M').time()
            vehicle.OutTime = outtime
            db.session.commit()
            if duration == None or 'none':
                intime = vehicle.InTime
                outtime = vehicle.OutTime
                diff = timeobj(intime, outtime)
                vehicle.TotalDuration = diff
                db.session.commit()
                flash('Out Time Updated')
            return redirect(url_for('dataentry.post_vehicles'))
        else:
            intime = datetime.strptime(
                request.form.get('intime'), '%H:%M').time()
            vehicle.InTime = intime
            flash('In Time Updated')
            db.session.commit()
            if duration == None or 'none':
                intime = vehicle.InTime
                outtime = vehicle.OutTime
                diff = timeobj(outtime, intime)
                vehicle.TotalDuration = diff
                db.session.commit()

    return redirect(url_for('dataentry.post_format'))


@dataentry.route('/vehicles/delete', methods=['POST'])
def delete_vehicles():
    vid = request.form.get('vid')
    vehicle = Vehicle.query.filter_by(VeID=vid).first()
    db.session.delete(vehicle)
    db.session.commit()
    flash('Vehicle Deleted')
    return redirect(url_for('dataentry.vehicles'))






@dataentry.route('/test-database-postformat')
def post_format():
    today_date = datetime.now().date()
    today_time = (datetime.now().time()).strftime("%H:%M")
    today_visitors = Visitor.query.all()
   
    employees = Employee.query.all()
    types = VehicleTypes.query.all()
    
    return render_template('test-dashboard-postformat.html', today_time=today_time, today_date=today_date, types=types, employees=employees,
                           today_visitors=today_visitors)


@dataentry.route('/test-dashboard-vehicles')
def post_vehicles():
    today_date = datetime.now().date()
    today_time = (datetime.now().time()).strftime("%H:%M")
    today_vehicles = Vehicle.query.filter_by(VeEntryDate=today_date).all()
    types = VehicleTypes.query.all()
    comp_vehicles = CompanyVehicle.query.all()
    comp_vehicles_today = CompanyTimesheet.query.filter_by(date=today_date).all()
    return render_template('test-dashboard-vehicles.html',today_vehicles=today_vehicles,today_date=today_date,today_time=today_time, types=types, comp_vehicles=comp_vehicles, comp_vehicles_today=comp_vehicles_today)


@dataentry.route('/test-postformat/visitor', methods=['POST'])
def visitors_post():
    if request.form:
        employee_id = int(request.form.get('visiting_employee'))
        employee = Employee.query.filter_by(id=employee_id).first()
        employee_dept = int(employee.department_id)
        entry_date = datetime.strptime(
            request.form.get('entrydate'), '%Y-%m-%d').date()
        intime = datetime.strptime(request.form.get('intime'), '%H:%M').time()
        visitor = Visitor(visitor_name=request.form.get('visitorname').upper(), visitor_contact=request.form.get('visitorcontact'), visitor_company=request.form.get(
            'visitorcompany').upper(), visiting_department=employee_dept, visiting_person=employee_id, visiting_purpose=request.form.get('visitingpurpose'), entry_date=entry_date, entry_time=intime)
        db.session.add(visitor)
        db.session.commit()
        flash('Visitor Added')
    return redirect(url_for('dataentry.post_format'))


@dataentry.route('/visitors/update', methods=['POST'])
def visitors_update():
    if request.form:
        vid = request.form['vi_id']
        visitor = Visitor.query.filter_by(id=vid).first()
        duration = visitor.total_duration
        exittime = datetime.strptime(
            request.form['exittime'], '%H:%M').time()
        visitor.exit_time = exittime
        db.session.commit()
        
        if (duration == None or 'none'):
            intime = visitor.entry_time
            outtime = visitor.exit_time
            diff = timeobj(intime, outtime)
            visitor.total_duration = diff
            db.session.commit()
    return jsonify({'status':'ok'})


@dataentry.route('/visitors/delete', methods=['POST'])
def visitors_delete():
    vid = request.form.get('vi_id')
    visitor = Visitor.query.filter_by(id=vid).first()
    db.session.delete(visitor)
    db.session.commit()
    return redirect(url_for('dataentry.post_format'))
