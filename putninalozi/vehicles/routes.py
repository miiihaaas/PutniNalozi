from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from putninalozi import app, db, bcrypt
from putninalozi.vehicles.forms import  RegistrationVehicleForm, UpdateVehicleForm
from putninalozi.models import Company,  Vehicle
from flask_login import current_user, login_required

vehicles = Blueprint('vehicles', __name__)


@vehicles.route("/vehicle_list")
def vehicle_list():
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    vehicles = Vehicle.query.all()
    return render_template('vehicle_list.html', title='Vehicles', vehicles=vehicles)


@vehicles.route("/register_v", methods=['GET', 'POST'])
def register_v():
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))
    form = RegistrationVehicleForm()
    form.reset()
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
        return redirect(url_for('vehicles.vehicle_list'))
    return render_template('register_v.html', title='Register New Vehicle', form=form)



@vehicles.route("/vehicle/<int:vehicle_id>", methods=['GET', 'POST'])
# @login_required
def vehicle_profile(vehicle_id): #ovo je funkcija za editovanje vozila
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    elif current_user.authorization == 'c_admin':
        if current_user.user_company.id != vehicle.vehicle_company.id:
            abort(403)
    print(Company.query.filter_by(id=vehicle.company_id).first().id)
    form = UpdateVehicleForm()
    # form.reset()
    # form.company_id=Company.query.filter_by(id=vehicle.company_id).first().id
    # form.process()
    if form.validate_on_submit():
        vehicle.vehicle_type = form.vehicle_type.data.upper()
        vehicle.vehicle_brand = form.vehicle_brand.data.upper()
        vehicle.vehicle_registration = form.vehicle_registration.data.upper()
        if current_user.authorization == 'c_admin':
            vehicle.company_id=int(current_user.company_id)
        elif current_user.authorization == 's_admin':
            vehicle.company_id = form.company_id.data

        db.session.commit()
        flash('Vehicle profile was updated', 'success')
        return redirect(url_for('vehicles.vehicle_list')) #vidi da li je bolje na neko drugo mesto da ga prebaci
    elif request.method == 'GET':
        form.vehicle_type.data = vehicle.vehicle_type
        form.vehicle_brand.data = vehicle.vehicle_brand
        form.vehicle_registration.data = vehicle.vehicle_registration
        form.company_id.choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]
        form.company_id.data = str(vehicle.company_id)
    return render_template('vehicle.html', title="Edit Vehicle", vehicle=vehicle, form=form, legend='Edit Vehicle')


@vehicles.route("/vehicle/<int:vehicle_id>/delete", methods=['POST'])
@login_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    print(f'debug - {request.form.get("input_password")}')
    if not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('nije dobar password')
        abort(403)
    else:
        if current_user.authorization == 'c_user':
            abort(403)
        elif current_user.authorization == 'c_admin':
            if current_user.user_company.id != vehicle.vehicle_company.id:
                abort(403)
            db.session.delete(vehicle)
            db.session.commit()
            flash(f'Vehicle {vehicle.vehicle_brand} has been deleted', 'success' )
            return redirect(url_for('vehicles.vehicle_list'))
        else:
            db.session.delete(vehicle)
            db.session.commit()
            flash(f'Vehicle: {vehicle.vehicle_brand} has been deleted', 'success' )
            return redirect(url_for('vehicles.vehicle_list'))
