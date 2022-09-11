from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField, DateTimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length
from putninalozi.models import Company, User, Vehicle
from flask_login import current_user
from putninalozi import db
# from putninalozi.travel_warrants.routes import users_list


class CreateTravelWarrantForm(FlaskForm):
    user_id = SelectField('Zaposleni:', validators=[DataRequired()], choices=[]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa Zadatkom: ', validators=[DataRequired()])
    company_id = SelectField('Company ID', validators=[DataRequired()], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ', validators=[DataRequired()])
    start_datetime = DateTimeField('Polazno Vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno Vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno Vozilo: ', choices=[])
    together_with = IntegerField('Zajedno sa: ')
    personal_type = SelectField('Tip Vozila: ', choices=[('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')])
    personal_brand = StringField('Brend Vozila: ')
    personal_registration = StringField('Vehicle Registration', validators=[Length(min=9, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    advance_payment = IntegerField('Akontacija: ', validators=[DataRequired()])
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage = IntegerField('Dnevnica: ', validators=[DataRequired()])
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni Troškvoi Padaju Na Teret: ', validators=[DataRequired()])

    submit = SubmitField('Kreiraj Putni Nalog')
    #nastaviti

    def reset(self):
        self.__init__()





class EditTravelWarrantForm(FlaskForm):
    pass

    def reset(self):
        self.__init__()
    #nastaviti
