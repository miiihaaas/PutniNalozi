from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField, DateTimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, InputRequired
from putninalozi.models import Company, User, Vehicle
from flask_login import current_user
from putninalozi import db
# from putninalozi.travel_warrants.routes import users_list


class PreCreateTravelWarrantForm(FlaskForm):
    user_id = SelectField('Zaposleni:', validators=[DataRequired()], choices=[]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Dalje')


class CreateTravelWarrantForm(FlaskForm):
    # user_id = SelectField('Zaposleni:', validators=[DataRequired()], choices=[]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa zadatkom: ', validators=[DataRequired()])
    company_id = SelectField('Kompanija: ', validators=[DataRequired()], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ', validators=[DataRequired()])
    # start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()], choices=[])
    together_with = IntegerField('Zajedno sa: ', validators=[Optional()])
    personal_type = SelectField('Tip vozila: ', choices=[('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=7, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    advance_payment = IntegerField('Akontacija: ', validators=[InputRequired('oriban')])
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage = IntegerField('Dnevnica: ', validators=[InputRequired()])
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškvoi padaju na teret: ', validators=[DataRequired()])
    # principal = #nalogodavac

    submit = SubmitField('Kreiraj putni nalog')
    #nastaviti

    def reset(self):
        self.__init__()


class EditAdminTravelWarrantForm(FlaskForm):
    user_id = SelectField('Zaposleni:', coerce=int, choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa zadatkom: ', validators=[])
    company_id = SelectField('Company ID', validators=[], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ')
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno Vozilo: ', validators=[Optional()])
    together_with = IntegerField('Zajedno sa: ', validators=[Optional()])
    personal_type = SelectField('Tip vozila: ', validators=[Optional()], choices=[('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=9, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    advance_payment = IntegerField('Akontacija: ')
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage = IntegerField('Dnevnica: ')
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškvoi padaju na teret: ')

    km_start = IntegerField('Početna kilometraža: ', validators=[DataRequired()])
    km_end = IntegerField('Završna kilometraža: ', validators=[DataRequired()])
    status = SelectField('Status: ', choices=[]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)

    submit = SubmitField('Ažuriraj putni nalog')

    def reset(self):
        self.__init__()


class EditUserTravelWarrantForm(FlaskForm):
    # user_id = SelectField('Zaposleni:', coerce=int, choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa zadatkom: ', validators=[])
    # company_id = SelectField('Company ID', validators=[], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ')
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()])
    together_with = IntegerField('Zajedno sa: ', validators=[Optional()])
    personal_type = SelectField('Tip vozila: ', validators=[Optional()], choices=[('ATMBL', 'AUTOMOBIL'),('KMB', 'KOMBI'),('KMN', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=9, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    # advance_payment = IntegerField('Akontacija: ')
    # advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    # daily_wage = IntegerField('Dnevnica: ')
    # daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    # costs_pays = StringField('Putni Troškvoi Padaju Na Teret: ')

    km_start = IntegerField('Početna kilometraža: ', validators=[DataRequired()])
    km_end = IntegerField('Završna kilometraža: ', validators=[DataRequired()])
    status = SelectField('Status: ', choices=[]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)

    submit = SubmitField('Ažuriraj putni nalog')

    def reset(self):
        self.__init__()
