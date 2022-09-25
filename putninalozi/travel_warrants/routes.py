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
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    warrants = TravelWarrant.query.all()
    return render_template('travel_warrant_list.html', title='Travel Warrants', warrants=warrants)


@travel_warrants.route("/register_tw", methods=['GET', 'POST'])
def register_tw():
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    user_list = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).order_by('name').all()]
    print(user_list)
    vehicle_list = [(0, "----")] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
    form = CreateTravelWarrantForm()
    form.reset()
    form.user_id.choices = user_list
    form.vehicle_id.choices = vehicle_list
    if form.validate_on_submit():
        if form.together_with.data != None:
            warrant = TravelWarrant(
                user_id=form.user_id.data,
                with_task=form.with_task.data,
                company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
                abroad_contry=form.abroad_contry.data.upper(),
                relation=form.relation.data,
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                vehicle_id="",
                together_with=form.together_with.data,
                personal_type="",
                personal_brand="",
                personal_registration="",
                other="",
                advance_payment=form.advance_payment.data,
                advance_payment_currency=form.advance_payment_currency.data,
                daily_wage=form.daily_wage.data,
                daily_wage_currency=form.daily_wage_currency.data,
                costs_pays=form.costs_pays.data,
                km_start=1,
                km_end=1,
                status=1)
        elif form.personal_brand.data != "":
            warrant = TravelWarrant(
                user_id=form.user_id.data,
                with_task=form.with_task.data,
                company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
                abroad_contry=form.abroad_contry.data.upper(),
                relation=form.relation.data,
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                vehicle_id="",
                together_with=0,
                personal_type=form.personal_type.data,
                personal_brand=form.personal_brand.data,
                personal_registration=form.personal_registration.data,
                other="",
                advance_payment=form.advance_payment.data,
                advance_payment_currency=form.advance_payment_currency.data,
                daily_wage=form.daily_wage.data,
                daily_wage_currency=form.daily_wage_currency.data,
                costs_pays=form.costs_pays.data,
                km_start=1,
                km_end=1,
                status=1)
        elif form.other.data != "":
            warrant = TravelWarrant(
                user_id=form.user_id.data,
                with_task=form.with_task.data,
                company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
                abroad_contry=form.abroad_contry.data.upper(),
                relation=form.relation.data,
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                vehicle_id="",
                together_with="",
                personal_type="",
                personal_brand="",
                personal_registration="",
                other=form.other.data,
                advance_payment=form.advance_payment.data,
                advance_payment_currency=form.advance_payment_currency.data,
                daily_wage=form.daily_wage.data,
                daily_wage_currency=form.daily_wage_currency.data,
                costs_pays=form.costs_pays.data,
                km_start=1,
                km_end=1,
                status=1)
        else:
            warrant = TravelWarrant(
                user_id=form.user_id.data,
                with_task=form.with_task.data,
                company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
                abroad_contry=form.abroad_contry.data.upper(),
                relation=form.relation.data,
                start_datetime=form.start_datetime.data,
                end_datetime=form.end_datetime.data,
                vehicle_id=form.vehicle_id.data, #ovde napraviti kod da bude podrazumevano vozilo
                together_with="",
                personal_type="",
                personal_brand="",
                personal_registration="",
                other="",
                advance_payment=form.advance_payment.data,
                advance_payment_currency=form.advance_payment_currency.data,
                daily_wage=form.daily_wage.data,
                daily_wage_currency=form.daily_wage_currency.data,
                costs_pays=form.costs_pays.data,
                km_start=1,
                km_end=1,
                status=1)

        db.session.add(warrant)
        db.session.commit()
        file_name = create_pdf_form(warrant)
        # send_email(warrant, current_user, file_name)
        flash(f'Putni nalog broj: {warrant.travel_warrant_id} je uspešno kreiran!', 'success')
        flash(f'{warrant.travelwarrant_user.name} je dobio mejl sa detaljima putnog naloga', 'success')
        return redirect('travel_warrant_list')
    print('nije dobra validacija')
    return render_template('register_tw.html', title='Kreiranje Putnog naloga', legend='Kreiranje Novog Putnog naloga', form=form)


@travel_warrants.route("/travel_warrant/<int:warrant_id>", methods=['GET', 'POST'])
def travel_warrant_profile(warrant_id):
    rod = []
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena"]
    #
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.user_company.id != warrant.travelwarrant_company.id:
        abort(403)
    elif current_user.authorization == 'c_user' and current_user.id != warrant.travelwarrant_user.id:
        abort(403)

    if current_user.authorization == 'c_user':
        form = EditUserTravelWarrantForm()
        form.reset()
        # form.user_id.choices = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).group_by('name').all()]
        form.vehicle_id.choices = [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
        form.personal_type.choices = [('', '----'), ('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')]
        form.status.choices=[(1, "kreiran"), (2, "završen")]

        if form.validate_on_submit():
            # warrant.user_id = form.user_id.data
            warrant.with_task = form.with_task.data
            # warrant.company_id = int(form.company_id.data)
            warrant.abroad_contry = form.abroad_contry.data
            warrant.relation = form.relation.data

            warrant.start_datetime = form.start_datetime.data
            warrant.end_datetime = form.end_datetime.data
            if form.vehicle_id.data == '':
                warrant.vehicle_id = 0
            else:
                warrant.vehicle_id = int(form.vehicle_id.data)
            if form.together_with.data == '':
                warrant.together_with = 0
            else:
                warrant.together_with = form.together_with.data
            warrant.personal_type = form.personal_type.data
            warrant.personal_brand = form.personal_brand.data
            warrant.personal_registration = form.personal_registration.data
            warrant.other = form.other.data

            # warrant.advance_payment = int(form.advance_payment.data)
            # warrant.advance_payment_currency = form.advance_payment_currency.data
            # warrant.daily_wage = int(form.daily_wage.data)
            # warrant.daily_wage_currency = form.daily_wage_currency.data
            # warrant.costs_pays = form.costs_pays.data

            warrant.km_start = int(form.km_start.data)
            warrant.km_end = int(form.km_end.data)
            warrant.status = int(form.status.data)

            db.session.commit()
            flash('Putni nalog je ažuriran.', 'success')
            return redirect(url_for('travel_warrants.travel_warrant_list'))
        elif request.method == 'GET':
            # form.user_id.choices = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).order_by('name').all()]
            # form.user_id.data = warrant.user_id
            form.with_task.data = warrant.with_task
            # form.company_id.data = str(User.query.filter_by(id=form.user_id.data).first().user_company.id)
            form.abroad_contry.data = warrant.abroad_contry
            form.relation.data = warrant.relation
            form.start_datetime.data = warrant.start_datetime
            form.end_datetime.data = warrant.end_datetime
            form.vehicle_id.choices =[('', '----')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
            form.vehicle_id.data = str(warrant.vehicle_id)
            form.together_with.data = warrant.together_with
            form.personal_type.choices = [('', '----'), ('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')]
            form.personal_type.data = warrant.personal_type
            form.personal_brand.data = warrant.personal_brand
            form.personal_registration.data = warrant.personal_registration
            form.other.data = warrant.other

            # form.advance_payment.data = warrant.advance_payment
            # form.advance_payment_currency.data = warrant.advance_payment_currency
            # form.daily_wage.data = warrant.daily_wage
            # form.daily_wage_currency.data = warrant.daily_wage_currency
            # form.costs_pays.data = warrant.costs_pays
            form.km_start.data = warrant.km_start
            form.km_end.data = warrant.km_end
            form.status.choices=[(1, "kreiran"), (2, "završen")]
            form.status.data = str(warrant.status)

        print(f'EditUser: {form.errors=}')

        return render_template('travel_warrant_user.html', title='Uređivanje Putnog Naloga', warrant=warrant, legend='Uređivanje Putnog Naloga - User View', form=form, rod=rod)

    else:
        form = EditAdminTravelWarrantForm()
        form.reset()
        form.user_id.choices = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).order_by('name').all()]
        form.vehicle_id.choices = [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
        form.personal_type.choices = [('', '----'), ('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')]
        form.status.choices=[(1, "kreiran"), (2, "završen"), (3, "obračunat")]

        if form.validate_on_submit():
            warrant.user_id = form.user_id.data
            warrant.with_task = form.with_task.data
            warrant.company_id = int(form.company_id.data)
            warrant.abroad_contry = form.abroad_contry.data
            warrant.relation = form.relation.data
            #
            warrant.start_datetime = form.start_datetime.data
            warrant.end_datetime = form.end_datetime.data
            if form.vehicle_id.data == '':
                warrant.vehicle_id = 0
            else:
                warrant.vehicle_id = int(form.vehicle_id.data)
            if form.together_with.data == '':
                warrant.together_with = 0
            else:
                warrant.together_with = form.together_with.data
            warrant.personal_type = form.personal_type.data
            warrant.personal_brand = form.personal_brand.data
            warrant.personal_registration = form.personal_registration.data
            warrant.other = form.other.data

            warrant.advance_payment = int(form.advance_payment.data)
            warrant.advance_payment_currency = form.advance_payment_currency.data
            warrant.daily_wage = int(form.daily_wage.data)
            warrant.daily_wage_currency = form.daily_wage_currency.data
            warrant.costs_pays = form.costs_pays.data

            warrant.km_start = int(form.km_start.data)
            warrant.km_end = int(form.km_end.data)
            warrant.status = int(form.status.data)

            db.session.commit()
            flash('Putni nalog je ažuriran', 'success')
            return redirect(url_for('travel_warrants.travel_warrant_list'))
        elif request.method == 'GET':
            form.user_id.choices = [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).order_by('name').all()]
            form.user_id.data = warrant.user_id
            form.with_task.data = warrant.with_task
            form.company_id.data = str(User.query.filter_by(id=form.user_id.data).first().user_company.id)
            form.abroad_contry.data = warrant.abroad_contry
            form.relation.data = warrant.relation
            form.start_datetime.data = warrant.start_datetime
            form.end_datetime.data = warrant.end_datetime
            form.vehicle_id.choices =[('', '----')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
            form.vehicle_id.data = str(warrant.vehicle_id)
            form.together_with.data = warrant.together_with
            form.personal_type.choices = [('', '----'), ('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')]
            form.personal_type.data = warrant.personal_type
            form.personal_brand.data = warrant.personal_brand
            form.personal_registration.data = warrant.personal_registration
            form.other.data = warrant.other

            form.advance_payment.data = warrant.advance_payment
            form.advance_payment_currency.data = warrant.advance_payment_currency
            form.daily_wage.data = warrant.daily_wage
            form.daily_wage_currency.data = warrant.daily_wage_currency
            form.costs_pays.data = warrant.costs_pays
            form.km_start.data = warrant.km_start
            form.km_end.data = warrant.km_end
            form.status.choices=[(1, "kreiran"), (2, "završen"), (3, "obračunat")]
            form.status.data = str(warrant.status)

        print(f'EditAdmin: {form.errors=}')

        return render_template('travel_warrant.html', title='Uređivanje Putnog Naloga', warrant=warrant, legend='Uređivanje Putnog Naloga - Admin View', form=form, rod=rod)
