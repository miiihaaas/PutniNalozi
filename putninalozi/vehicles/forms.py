from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from putninalozi import db
from putninalozi.models import Company


class RegistrationVehicleForm(FlaskForm):
    vehicle_type = SelectField('Tip Vozila', validators=[DataRequired()], choices=[('atmbl', 'AUTOMOBIL'),('kmb', 'KOMBI'),('kmn', 'KAMION')])
    vehicle_brand = StringField('Brend Vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registracija Vozila', validators=[DataRequired(), Length(min=7, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=Company.query.all())
    submit = SubmitField('Registruj Vozilo')

    def reset(self):
        self.__init__()


class UpdateVehicleForm(FlaskForm):
    vehicle_type = SelectField('Tip Vozila', validators=[DataRequired()], choices=[('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')])
    vehicle_brand = StringField('Brend Vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registracija Vozila', validators=[DataRequired(), Length(min=9, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    submit = SubmitField('Registruj Vozilo')

    def reset(self):
        self.__init__()
