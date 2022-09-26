from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length
from putninalozi import db
from putninalozi.models import Company


class RegistrationVehicleForm(FlaskForm):
    vehicle_type = SelectField('Tip vozila', validators=[DataRequired()], choices=[('AUTOMOBIL', 'AUTOMOBIL'),('KOMBI', 'KOMBI'),('KAMION', 'KAMION')])
    vehicle_brand = StringField('Marka vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registracija vozila', validators=[DataRequired(), Length(min=7, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=Company.query.all())
    submit = SubmitField('Registruj vozilo')

    def reset(self):
        self.__init__()


class UpdateVehicleForm(FlaskForm):
    vehicle_type = SelectField('Tip vozilo', validators=[DataRequired()], choices=[('AUTOMOBIL', 'AUTOMOBIL'),('KOMBI', 'KOMBI'),('KAMION', 'KAMION')])
    vehicle_brand = StringField('Marka vozila', validators=[DataRequired(), Length(min=2, max=20)])
    vehicle_registration = StringField('Registracija vozila', validators=[DataRequired(), Length(min=7, max=12)]) # GM 047-DD
    company_id = SelectField('Kompanija', validators=[DataRequired()], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()])
    submit = SubmitField('Ažuriraj podatke')

    def reset(self):
        self.__init__()
