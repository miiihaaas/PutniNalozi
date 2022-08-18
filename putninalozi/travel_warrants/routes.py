from flask import Blueprint
from flask import  render_template, url_for, flash, redirect
from putninalozi import db
# from putninalozi.travel_warrants.forms import TravelWarrantForm
from putninalozi.models import TravelWarrant, User
from putninalozi.travel_warrants.forms import CreateTravelWarrantForm
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


travel_warrants = Blueprint('travel_warrants', __name__)

def users_list():
    users_list = User.query.filter_by(company_id=current_user.user_company.id).all()
    return users_list


@travel_warrants.route("/travel_warrant_list")
def travel_warrant_list():
    warrants = TravelWarrant.query.all()
    return render_template('travel_warrant_list.html', title='Travel Warrants', warrants=warrants)


@travel_warrants.route("/register_tw", methods=['GET', 'POST'])
def register_tw():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    print(f'{current_user.user_company.id=}')
    users_list = User.query.filter_by(company_id=current_user.user_company.id).all()
    print(users_list)
    print(f'{current_user.authorization=}')
    print(f'{current_user.user_company.companyname=}')
    form = CreateTravelWarrantForm()
    if form.validate_on_submit():
        warrant = TravelWarrant(
            with_task=form.with_task.data,
            user_id=form.user_id.data,
            company_id=form.company_id.data,
            abroad_contry=form.abroad_contry.data.upper(),
            relation=form.relation.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data
        )
        db.session.add(warrant)
        db.session.commit()
        flash(f'Travel Warrant number: {warrant.travel_warrant_id} has been created successfully!', 'success')
        return redirect('travel_warrant_list')
    print('nije dobra validacija')
    print(form.start_datetime.data)
    return render_template('register_tw.html', title='Create Travel Warrant', form=form)
