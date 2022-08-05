from flask import Blueprint
from flask import  render_template, url_for, flash, redirect
from putninalozi import app, db, bcrypt
from putninalozi.vehicles.forms import  RegistrationVehicleForm
from putninalozi.models import Company,  Vehicle
from flask_login import current_user

vehicles = Blueprint('vehicles', __name__)


@vehicles.route("/vehicle_list")
def vehicle_list():
    vehicles = Vehicle.query.all()
    return render_template('vehicle_list.html', title='Vehicles', vehicles=vehicles)


@vehicles.route("/register_v", methods=['GET', 'POST'])
def register_v():
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))
    form = RegistrationVehicleForm()
    if form.validate_on_submit():
        if current_user.authorization == 'c_admin':
            vehicle = Vehicle(vehicle_type=form.vehicle_type.data.upper(),
                                vehicle_brand=form.vehicle_brand.data.upper(),
                                vehicle_registration=form.vehicle_registration.data.upper(),
                                company_id=int(current_user.company_id))
            db.session.add(vehicle)
            db.session.commit()
        elif current_user.authorization == 's_admin':
            vehicle = Vehicle(vehicle_type=form.vehicle_type.data.upper(),
                                vehicle_brand=form.vehicle_brand.data.upper(),
                                vehicle_registration=form.vehicle_registration.data.upper(),
                                company_id=Company.query.filter_by(companyname=form.company_id.data).first().id)
            db.session.add(vehicle)
            db.session.commit()
        flash(f'Vehicle with registration: {form.vehicle_registration.data} has been created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register_v.html', title='Register New Vehicle', form=form)
