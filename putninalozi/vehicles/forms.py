from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from putninalozi import db
from putninalozi.models import Company


class RegistrationVehicleForm(FlaskForm):
    vehicle_ownership = SelectField('Vlasništvo vozila', choices=[('company', 'Službeno vozilo'), ('private', 'Privatno vozilo')])
    vehicle_type = SelectField('Tip vozila', validators=[DataRequired()], choices=[('putničko - automobil', 'putničko - automobil'),('putničko - kombi', 'putničko - kombi'),('teretno - kombi', 'teretno - kombi'),('teretno', 'teretno'),('terensko', 'terensko')])
    vehicle_brand = StringField('Marka vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registraciona oznaka vozila', validators=[DataRequired(), Length(min=7, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=[])
    submit = SubmitField('Registrujte vozilo')

    def reset(self):
        self.__init__()


class UpdateVehicleForm(FlaskForm):
    vehicle_ownership = SelectField('Vlasništvo vozila', choices=[('company', 'Službeno vozilo'), ('private', 'Privatno vozilo')])
    vehicle_type = SelectField('Tip vozila', validators=[DataRequired()], choices=[('putničko - automobil', 'putničko - automobil'),('putničko - kombi', 'putničko - kombi'),('teretno - kombi', 'teretno - kombi'),('teretno', 'teretno'),('terensko', 'terensko')])
    vehicle_brand = StringField('Marka vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registraciona oznaka vozila', validators=[DataRequired(), Length(min=7, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=[])
    submit = SubmitField('Ažurirajte podatke')

    def reset(self):
        self.__init__()
