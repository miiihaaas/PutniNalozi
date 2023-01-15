from flask import Blueprint
from flask import  render_template, flash, redirect, url_for, request
from putninalozi import db
from putninalozi.models import Settings
from putninalozi.main.forms import SettingsForm
from flask_login import current_user

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
    if current_user.user_company.id != company_id:
        flash(f'Nemate ovlašćenje da podešavate parametre drugih kompanija.', 'danger')
        return redirect(url_for('main.home'))
    global_settings = Settings.query.filter_by(company_id=company_id).first()
    form = SettingsForm()
    if form.validate_on_submit():
        global_settings.daily_wage_domestic = form.daily_wage_domestic.data
        global_settings.daily_wage_abroad = form.daily_wage_abroad.data
        global_settings.send_email_kreiran = form.send_email_kreiran.data
        global_settings.send_email_zavrsen = form.send_email_zavrsen.data
        global_settings.send_email_obracunat = form.send_email_obracunat.data
        db.session.commit()
        flash(f'Ažurirana su podešavanja.', 'success')
        return redirect(url_for('main.home'))
    elif request.method == 'GET':
        form.daily_wage_domestic.data = global_settings.daily_wage_domestic
        form.daily_wage_abroad.data = global_settings.daily_wage_abroad
        form.send_email_kreiran.data = global_settings.send_email_kreiran
        form.send_email_zavrsen.data = global_settings.send_email_zavrsen
        form.send_email_obracunat.data = global_settings.send_email_obracunat

    return render_template('settings.html', title='Podešavanja', legend='Podešavanja', global_settings=global_settings, form=form)
