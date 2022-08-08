from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from putninalozi.models import Company

class RegistrationCompanyForm(FlaskForm):
    companyname = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
    company_address = StringField('Company Street', validators=[DataRequired(), Length(min=5, max=20)])
    company_address_number = StringField('Number', validators=[DataRequired(), Length(min=1, max=5)])
    company_zip_code = StringField('ZIP', validators=[DataRequired(), Length(min=5, max=5)])
    company_city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    company_state = StringField('State', validators=[DataRequired(), Length(min=2, max=20)])
    company_pib = StringField('PIB', validators=[DataRequired(), Length(min=5, max=9)]) #koji me min max broj cifara - da li su samo cifre - dali je fiksan broj cifara?
    company_mb = StringField('MB', validators=[DataRequired(), Length(min=5, max=8)]) #šta je ovo
    company_site = StringField('Web Site', validators=[DataRequired(), Length(min=5, max=50)])
    company_mail = StringField('Email', validators=[DataRequired(), Email()])
    company_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=9, max=13)])
    company_logo = "" #na ovom poraditi --->> https://www.youtube.com/watch?v=803Ei2Sq-Zs&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=7&ab_channel=CoreySchafer <<--- :)
    submit = SubmitField('Register Company')

    def validate_companyname(self, companyname):
        company = Company.query.filter_by(companyname=companyname.data).first()
        if company:
            raise ValidationError('That company name is taken, please choose a different one')

class EditCompanyForm(FlaskForm):
    companyname = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=20)])
    company_address = StringField('Company Street', validators=[DataRequired(), Length(min=5, max=20)])
    company_address_number = StringField('Number', validators=[DataRequired(), Length(min=1, max=5)])
    company_zip_code = StringField('ZIP', validators=[DataRequired(), Length(min=5, max=5)])
    company_city = StringField('City', validators=[DataRequired(), Length(min=2, max=20)])
    company_state = StringField('State', validators=[DataRequired(), Length(min=2, max=20)])
    company_pib = StringField('PIB', validators=[DataRequired(), Length(min=5, max=9)]) #koji me min max broj cifara - da li su samo cifre - dali je fiksan broj cifara?
    company_mb = StringField('MB', validators=[DataRequired(), Length(min=5, max=8)]) #šta je ovo
    company_site = StringField('Web Site', validators=[DataRequired(), Length(min=5, max=50)])
    company_mail = StringField('Email', validators=[DataRequired(), Email()])
    company_phone = StringField('Phone Number', validators=[DataRequired(), Length(min=9, max=13)])
    company_logo = FileField('Update Logo', validators=[FileAllowed(['jpg', 'png'])]) #na ovom poraditi --->> https://www.youtube.com/watch?v=803Ei2Sq-Zs&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&index=7&ab_channel=CoreySchafer <<--- :)
    submit = SubmitField('Update Company')
