import secrets, os
from PIL import Image
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from putninalozi import db, app
from putninalozi.companys.forms import RegistrationCompanyForm, EditCompanyForm
from putninalozi.models import Company
from flask_login import current_user, login_required

companys = Blueprint('companys', __name__)


@companys.route("/company_list")
def company_list():
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    companys = Company.query.all()
    return render_template('company_list.html', title='Companies', companys=companys)


@companys.route("/register_c", methods=['GET', 'POST'])
def register_c():
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.is_authenticated and current_user.authorization != 's_admin':
        return redirect(url_for('main.home'))
    form = RegistrationCompanyForm()
    if form.validate_on_submit():
        company = Company(companyname=form.companyname.data.upper(),
                            company_address=form.company_address.data.upper(),
                            company_address_number=form.company_address_number.data,
                            company_zip_code=form.company_zip_code.data,
                            company_city=form.company_city.data.upper(),
                            company_state=form.company_state.data.upper(),
                            company_pib=form.company_pib.data,
                            company_mb=form.company_mb.data,
                            company_site=form.company_site.data,
                            company_mail=form.company_mail.data,
                            company_phone=form.company_phone.data,
                            company_logo="",
                            cashier_email=form.cashier_email.data,
                            CEO=form.CEO.data)
        db.session.add(company)
        db.session.commit()
        flash(f'Kompanija: {form.companyname.data} je uspešno kreirana!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register_c.html', title='Kreiranje Nove Kompanije', legend='Kreiranje Nove Kompanije', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/company_logos', picture_fn)
    form_picture.save(picture_path)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@companys.route("/company/<int:company_id>", methods=['GET', 'POST'])
# @login_required
def company_profile(company_id): #ovo je funkcija za editovanje user-a
    company = Company.query.get_or_404(company_id)
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        abort(403)
    elif current_user.user_company.id != company.id and current_user.authorization != 's_admin':
        abort(403)
    form = EditCompanyForm()
    if form.validate_on_submit():
        if form.company_logo.data:
            picture_file = save_picture(form.company_logo.data)
            company.company_logo=picture_file


        company.companyname=form.companyname.data
        company.company_address=form.company_address.data
        company.company_address_number=form.company_address_number.data
        company.company_zip_code=form.company_zip_code.data
        company.company_city=form.company_city.data
        company.company_state=form.company_state.data
        company.company_pib=form.company_pib.data
        company.company_mb=form.company_mb.data
        company.company_site=form.company_site.data
        company.company_mail=form.company_mail.data
        company.company_phone=form.company_phone.data
        company.cashier_email=form.cashier_email.data
        company.CEO=form.CEO.data
        db.session.commit()
        flash('Podaci kompanije su ažurirani.', 'success')
        return redirect(url_for('companys.company_list', title='Kompanije', companys=companys))
    elif request.method == 'GET':
        form.companyname.data=company.companyname
        form.company_address.data=company.company_address
        form.company_address_number.data=company.company_address_number
        form.company_zip_code.data=company.company_zip_code
        form.company_city.data=company.company_city
        form.company_state.data=company.company_state
        form.company_pib.data=company.company_pib
        form.company_mb.data=company.company_mb
        form.company_site.data=company.company_site
        form.company_mail.data=company.company_mail
        form.company_phone.data=company.company_phone
        form.cashier_email.data=company.cashier_email
        form.CEO.data=company.CEO
        form.company_logo.data=company.company_logo
    image_file = url_for('static', filename='company_logos/' + company.company_logo)
    print(image_file)
    return render_template('company.html', title='Uređivanje Podataka Kompanije', company=company, form=form, legend='Uređivanje Podataka Kompanije', image_file=image_file)
