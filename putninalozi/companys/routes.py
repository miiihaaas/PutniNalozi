from flask import Blueprint
from flask import  render_template, url_for, flash, redirect
from putninalozi import db
from putninalozi.companys.forms import RegistrationCompanyForm
from putninalozi.models import Company
from flask_login import current_user

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
