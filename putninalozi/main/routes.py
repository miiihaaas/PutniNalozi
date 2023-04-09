from flask import Blueprint
from flask import  render_template, flash, redirect, url_for, request
from putninalozi import db
from putninalozi.models import Settings, Company
from putninalozi.main.forms import SettingsForm
from flask_login import current_user
from datetime import datetime, timedelta

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    return render_template('home.html', title='Početna', legend='Početna')


@main.route("/about")
def about():
    return render_template('about.html', title='O softveru', legend='O softveru')


@main.route("/settings/<int:company_id>", methods=['GET', 'POST'])
def settings(company_id):
    now = datetime.now().date()
    now_plus_one_year = now + timedelta(days=365) 
    premium = Company.query.filter_by(id=company_id).first()
    print(f'{now_plus_one_year=}')
    end_of_premium=datetime.strptime(premium.premium_expiration_date, '%Y-%m-%d').date()
    print(f'{end_of_premium=}')
    if now_plus_one_year > end_of_premium:
        premium = True
    else:
        premium = False
    if current_user.user_company.id != company_id:
        flash(f'Nemate ovlašćenje da podešavate parametre drugih kompanija.', 'danger')
        return redirect(url_for('main.home'))
    global_settings = Settings.query.filter_by(company_id=company_id).first()
    form = SettingsForm()
    if form.validate_on_submit():
        global_settings.daily_wage_domestic = form.daily_wage_domestic.data
        global_settings.daily_wage_abroad = form.daily_wage_abroad.data
        global_settings.send_email_kreiran = form.send_email_kreiran.data
        global_settings.send_email_kreiran_principial = form.send_email_kreiran_principial.data
        global_settings.send_email_zavrsen = form.send_email_zavrsen.data
        global_settings.send_email_obracunat_cashier = form.send_email_obracunat_cashier.data
        db.session.commit()
        flash(f'Ažurirana su podešavanja.', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.daily_wage_domestic.data = global_settings.daily_wage_domestic
        form.daily_wage_abroad.data = global_settings.daily_wage_abroad
        form.send_email_kreiran.data = global_settings.send_email_kreiran
        form.send_email_kreiran_principial.data = global_settings.send_email_kreiran_principial
        form.send_email_zavrsen.data = global_settings.send_email_zavrsen
        form.send_email_obracunat_cashier.data = global_settings.send_email_obracunat_cashier

    return render_template('settings.html', title='Podešavanja', 
                            legend='Podešavanja', global_settings=global_settings, 
                            form=form, premium=premium)
