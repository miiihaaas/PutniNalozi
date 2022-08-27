from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, abort
from putninalozi import db
# from putninalozi.travel_warrants.forms import TravelWarrantForm
from putninalozi.models import TravelWarrant, User
from putninalozi.travel_warrants.forms import CreateTravelWarrantForm
from putninalozi.travel_warrants.pdf_form import create_pdf_form, send_email
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime


travel_warrants = Blueprint('travel_warrants', __name__)

def users_list():
    users_list = User.query.filter_by(company_id=current_user.user_company.id).all()
    return users_list


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
    form = CreateTravelWarrantForm()
    form.reset()
    form.user_id.choices = user_list
    if form.validate_on_submit():
        warrant = TravelWarrant(
            with_task=form.with_task.data,
            user_id=form.user_id.data,
            company_id=User.query.filter_by(id=form.user_id.data).first().user_company.id,  #form.company_id.data,
            abroad_contry=form.abroad_contry.data.upper(),
            relation=form.relation.data,
            start_datetime=form.start_datetime.data,
            end_datetime=form.end_datetime.data
        )

        db.session.add(warrant)
        db.session.commit()
        file_name = create_pdf_form(warrant)
        send_email(warrant, current_user, file_name)
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
    return render_template('travel_warrant.html', title='Edit Travel Warrant', warrant=warrant, legend='Edit Travel Warrant')
