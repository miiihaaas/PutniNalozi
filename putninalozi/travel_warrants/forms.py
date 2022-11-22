from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, DecimalField, SelectField, DateField, TimeField, DateTimeField, IntegerField, SubmitField
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
    abroad = BooleanField('Putovanje u inostranstvo')
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ', validators=[DataRequired()])
    # start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()], choices=[])
    together_with = SelectField('Zajedno sa: ', validators=[Optional()], choices=[])
    personal_type = SelectField('Tip vozila: ', choices=[('AUTOMOBIL', 'AUTOMOBIL'),('KOMBI', 'KOMBI'),('KAMION', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=7, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    advance_payment = DecimalField('Akontacija: ', validators=[Optional('oriban')])
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage = DecimalField('Iznos dnevnice u državi: ')
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu: ')
    daily_wage_abroad_currency = SelectField('Valuta: ', choices=[('e', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškovi padaju na teret: ', validators=[DataRequired()])
    # principal = #nalogodavac

    submit = SubmitField('Kreiraj putni nalog')
    #nastaviti

    def reset(self):
        self.__init__()


class EditAdminTravelWarrantForm(FlaskForm):
    # user_id = SelectField('Zaposleni:', coerce=int, choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa zadatkom: ', validators=[])
    # company_id = SelectField('Company ID', validators=[], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad = BooleanField('Putovanje u inostranstvo')
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ')
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    contry_leaving = DateTimeField('Vrema napuštanja države: ', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    contry_return = DateTimeField('Vreme vraćanja u državu: ', format='%Y-%m-%dT%H:%M', validators=[Optional()])

    vehicle_id = SelectField('Službeno Vozilo: ', validators=[Optional()])
    together_with = SelectField('Zajedno sa: ', validators=[Optional()], choices=[])
    personal_type = SelectField('Tip vozila: ', validators=[Optional()], choices=[('AUTOMOBIL', 'AUTOMOBIL'),('KOMBI', 'KOMBI'),('KAMION', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=7, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    advance_payment = DecimalField('Akontacija: ')
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage = DecimalField('Iznos dnevnice u državi: ')
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu: ')
    daily_wage_abroad_currency = SelectField('Valuta: ', choices=[('e', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškovi padaju na teret: ')

    km_start = IntegerField('Početna kilometraža: ', validators=[DataRequired()])
    km_end = IntegerField('Završna kilometraža: ', validators=[DataRequired()])
    status = SelectField('Status: ', choices=[]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)
    # expenses = FloatField('Ukupni troškovi', validators=[DataRequired()])

    add_expenses = SubmitField('Dofaj trošak')
    submit = SubmitField('Ažurirajte putni nalog')

    def reset(self):
        self.__init__()


class EditUserTravelWarrantForm(FlaskForm):
    # user_id = SelectField('Zaposleni:', coerce=int, choices=[(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    with_task = StringField('Sa zadatkom: ', validators=[])
    # company_id = SelectField('Company ID', validators=[], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad = BooleanField('Putovanje u inostranstvo')
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ')
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    contry_leaving = DateTimeField('Vrema napuštanja države: ', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    contry_return = DateTimeField('Vreme vraćanja u državu: ', format='%Y-%m-%dT%H:%M', validators=[Optional()])

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()])
    together_with = SelectField('Zajedno sa: ', validators=[Optional()], choices=[])
    personal_type = SelectField('Tip vozila: ', validators=[Optional()], choices=[('AUTOMOBIL', 'AUTOMOBIL'),('KOMBI', 'KOMBI'),('KAMION', 'KAMION')])
    personal_brand = StringField('Brend vozila: ')
    personal_registration = StringField('Registracija ličnog vozila:', validators=[Optional(), Length(min=7, max=12)]) # GM 047-DD
    other = StringField('Drugo: ')

    # advance_payment = IntegerField('Akontacija: ')
    # advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    # daily_wage = IntegerField('Dnevnica: ')
    # daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    # costs_pays = StringField('Putni troškovi padaju na teret: ')

    km_start = IntegerField('Početna kilometraža: ', validators=[DataRequired()])
    km_end = IntegerField('Završna kilometraža: ', validators=[DataRequired()])
    status = SelectField('Status: ', choices=[]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)
    # expenses = FloatField('Ukupni troškovi', validators=[DataRequired()])

    add_expenses = SubmitField('Dofaj trošak')
    submit = SubmitField('Ažurirajte putni nalog')

    def reset(self):
        self.__init__()


class TravelWarrantExpensesForm(FlaskForm):
    expenses_type = SelectField('Tip troška', choices=[('Ostale naknade', 'Ostale naknade'), ('Ostali troškovi na službenom putu', 'Ostali troškovi na službenom putu'), ('Parkiranje', 'Parkiranje'), ('Putarine', 'Putarine'), ('Troškovi noćenja', 'Troškovi noćenja'), ('Troškovi prevoza', 'Troškovi prevoza'), ('Troškovi smeštaja i ishrane', 'Troškovi smeštaja i ishrane')] )
    expenses_date = DateTimeField('Datum: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = StringField('Opis troška: ', validators=[DataRequired()])
    amount = DecimalField('Iznos: ', validators=[DataRequired()])
    amount_currency =  SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    submit = SubmitField('Dodajte trošak')

    def reset(self):
        self.__init__()


class EditTravelWarrantExpenses(FlaskForm):
    expenses_type = SelectField('Tip troška', choices=[] )
    expenses_date = DateTimeField('Datum: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    description = StringField('Opis troška: ', validators=[DataRequired()])
    amount = DecimalField('Iznos: ', validators=[DataRequired()])
    amount_currency =  SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('e', 'EUR'), ('usd', 'USD')])
    submit = SubmitField('Ažurirajte trošak')

    def reset(self):
        self.__init__()
