import secrets, os
from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request
from putninalozi import db
from putninalozi.companys.forms import RegistrationCompanyForm, EditCompanyForm
from putninalozi.models import Company
from flask_login import current_user, login_required

companys = Blueprint('companys', __name__)


@companys.route("/company_list")
def company_list():
    companys = Company.query.all()
    return render_template('company_list.html', title='Companies', companys=companys)


@companys.route("/register_c", methods=['GET', 'POST'])
def register_c():
    if current_user.is_authenticated and current_user.authorization != 's_admin':
        return redirect(url_for('main.home'))
    form = RegistrationCompanyForm()
    if form.validate_on_submit():
        company = Company(companyname=form.companyname.data.upper(),
                            companyname_short=form.companyname_short.data.upper(),
                            company_address=form.company_address.data.upper(),
                            company_address_number=form.company_address_number.data,
                            company_zip_code=form.company_zip_code.data,
                            company_city=form.company_city.data.upper(),
                            company_state=form.company_state.data.upper(),
                            company_pib=form.company_pib.data,
                            company_mb=form.company_mb.data,
                            company_site=form.company_site.data,
                            company_mail=form.company_mail.data,
                            company_phone=form.company_phone.data)
        db.session.add(company)
        db.session.commit()
        flash(f'Company {form.companyname.data} has been created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register_c.html', title='Register New Company', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/company_logos', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@companys.route("/company/<int:company_id>", methods=['GET', 'POST'])
@login_required
def company_profile(company_id): #ovo je funkcija za editovanje user-a
    company = Company.query.get_or_404(company_id)
    if current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        if current_user.id == user.id:
            pass
        else:
            abort(403)
    form = EditCompanyForm()
    if form.validate_on_submit():
        if form.company_logo.data:
            picture_file = save_picture(form.company_logo.data)
        companyname=form.companyname.data
        company_address=form.company_address.data
        company_address_number=form.company_address_number.data
        company_zip_code=form.company_zip_code.data
        company_city=form.company_city.data
        company_state=form.company_state.data
        company_pib=form.company_pib.data
        company_mb=form.company_mb.data
        company_site=form.company_site.data
        company_mail=form.company_mail.data
        company_phone=form.company_phone.data
        company_logo=form.company_logo.data
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
        # form.company_logo.data=company.company_logo
    return render_template('company.html', title='Edit Company', form=form, legend='Edit Company')
