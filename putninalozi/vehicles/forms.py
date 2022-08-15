from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from putninalozi.models import Company


class RegistrationVehicleForm(FlaskForm):
    vehicle_type = SelectField('Vehicle Type', validators=[DataRequired()], choices=[('atmbl', 'AUTOMOBIL'),('kmb', 'KOMBI'),('kmn', 'KAMION')])
    vehicle_brand = StringField('Vehicle Brand', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Vehicle Registration', validators=[DataRequired(), Length(min=9, max=12)]) # GM 047-DD
    company_id = SelectField('Company ID', validators=[DataRequired()], choices=Company.query.all())
    submit = SubmitField('Register Vehicle')


class UpdateVehicleForm(FlaskForm):
    vehicle_type = SelectField('Vehicle Type', validators=[DataRequired()], choices=[('atmbl', 'AUTOMOBIL'),('kmb', 'KOMBI'),('kmn', 'KAMION')])
    vehicle_brand = StringField('Vehicle Brand', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Vehicle Registration', validators=[DataRequired(), Length(min=9, max=12)]) # GM 047-DD
    company_id = SelectField('Company ID', validators=[DataRequired()], choices=Company.query.all())
    submit = SubmitField('Update Vehicle')
