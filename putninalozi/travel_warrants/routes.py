from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, abort, request
from putninalozi import db
# from putninalozi.travel_warrants.forms import TravelWarrantForm
from putninalozi.models import TravelWarrant, User, Vehicle
from putninalozi.travel_warrants.forms import CreateTravelWarrantForm, EditAdminTravelWarrantForm, EditUserTravelWarrantForm
from putninalozi.travel_warrants.pdf_form import create_pdf_form, send_email
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


travel_warrants = Blueprint('travel_warrants', __name__)
#
# def users_list():
#     users_list = User.query.filter_by(company_id=current_user.user_company.id).all()
#     return users_list


@travel_warrants.route("/travel_warrant_list")
def travel_warrant_list():
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    warrants = TravelWarrant.query.all()
    return render_template('travel_warrant_list.html', title='Travel Warrants', warrants=warrants)


@travel_warrants.route("/register_tw", methods=['GET', 'POST'])
def register_tw():
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    user_list = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).group_by('name').all()]
    print(user_list)
    vehicle_list = [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).group_by('vehicle_type').all()]
    form = CreateTravelWarrantForm()
    form.reset()
    form.user_id.choices = user_list
    form.vehicle_id.choices = vehicle_list
    if form.validate_on_submit():
        warrant = TravelWarrant(
            user_id=form.user_id.data,
            with_task=form.with_task.data,
            company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
            abroad_contry=form.abroad_contry.data.upper(),
            relation=form.relation.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data,
            vehicle_id=form.vehicle_id.data,
            together_with=form.together_with.data,
            personal_type=form.personal_type.data,
            personal_brand=form.personal_brand.data,
            personal_registration=form.personal_registration.data,
            other=form.other.data,
            advance_payment=form.advance_payment.data,
            advance_payment_currency=form.advance_payment_currency.data,
            daily_wage=form.daily_wage.data,
            daily_wage_currency=form.daily_wage_currency.data,
            costs_pays=form.costs_pays.data,
            km_start=1,
            km_end=1,
            status=1
        )

        db.session.add(warrant)
        db.session.commit()
        # file_name = create_pdf_form(warrant)
        # send_email(warrant, current_user, file_name)
        flash(f'Travel Warrant number: {warrant.travel_warrant_id} has been created successfully!', 'success')
        return redirect('travel_warrant_list')
    print('nije dobra validacija')
    return render_template('register_tw.html', title='Create Travel Warrant', form=form)


@travel_warrants.route("/travel_warrant/<int:warrant_id>", methods=['GET', 'POST'])
def travel_warrant_profile(warrant_id):
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if not current_user.is_authenticated:
        flash('You have to be logged in to access this page', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.user_company.id != warrant.travelwarrant_company.id:
        abort(403)
    elif current_user.authorization == 'c_user' and current_user.id != warrant.travelwarrant_user.id:
        abort(403)

    if current_user.authorization == 'c_user':
        form = EditUserTravelWarrantForm()
        form.reset()

        if form.validate_on_submit():
            warrant.start_datetime = form.start_datetime.data
            warrant.end_datetime = form.end_datetime.data
            warrant.vehicle_id = form.vehicle_id.data
            warrant.together_with = form.together_with.data
            warrant.personal_type = form.personal_type.data
            warrant.personal_brand = form.personal_brand.data
            warrant.personal_registration = form.personal_registration.data
            warrant.other = form.other.data

            warrant.km_start = form.km_start.data
            warrant.km_end = form.km_end.data

            db.session.commit()
            flash('Travel Warrant was updated', 'success')
            return redirect(url_for('travel_warrants.travel_warrant_list'))
        elif request.method == 'GET':
            form.start_datetime.data = warrant.start_datetime
            form.end_datetime.data = warrant.end_datetime
            form.vehicle_id.choices = [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).group_by('vehicle_type').all()]
            form.vehicle_id.data = warrant.vehicle_id
            form.together_with.data = warrant.together_with
            form.personal_type.data = warrant.personal_type
            form.personal_brand.data = warrant.personal_brand
            form.personal_registration.data = warrant.personal_registration
            form.other.data = warrant.other
            form.km_start.data = warrant.km_start
            form.km_end.data = warrant.km_end
        return render_template('travel_warrant.html', title='Edit Travel Warrant', warrant=warrant, legend='Edit Travel Warrant', form=form)

    else:
        form = EditAdminTravelWarrantForm()
        form.reset()

        if form.validate_on_submit():
            pass
        return render_template('travel_warrant.html', title='Edit Travel Warrant', warrant=warrant, legend='Edit Travel Warrant')
