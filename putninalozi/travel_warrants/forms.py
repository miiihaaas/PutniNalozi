from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, FloatField, DecimalField, SelectField, DateField, TimeField, DateTimeField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, InputRequired, NumberRange, ValidationError
from putninalozi.models import Company, User, Vehicle
from flask_login import current_user
from putninalozi import db
# from putninalozi.travel_warrants.routes import users_list


class PreCreateTravelWarrantForm(FlaskForm):
    user_id = SelectField('Zaposleni:', validators=[DataRequired()], choices=[]) #[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    start_datetime = DateTimeField('Polazno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Dalje')


class CreateTravelWarrantForm(FlaskForm):
    with_task = StringField('Sa zadatkom: ', validators=[DataRequired()])
    company_id = SelectField('Kompanija: ', validators=[DataRequired()], choices=[])
    abroad = BooleanField('Putovanje u inostranstvo')
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()], choices=[])
    together_with = SelectField('Zajedno sa: ', validators=[Optional()], choices=[])
    personal_vehicle_id = SelectField('Privatno vozilo: ', validators=[Optional()], choices=[])    
    other = StringField('Drugo: ')

    advance_payment = DecimalField('Akontacija: ', validators=[Optional('oriban'), NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    daily_wage = DecimalField('Iznos dnevnice u državi: ', validators=[NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu: ', validators=[NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    daily_wage_abroad_currency = SelectField('Valuta: ', choices=[('€', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškovi padaju na teret: ', validators=[DataRequired()])
    principal_id = SelectField('Nalogodavac: ', validators=[Optional()], choices=[])
    cashier_id = SelectField('Blagajnik: ', validators=[Optional()], choices=[])

    submit = SubmitField('Kreirajte putni nalog')
    
    def validate_form(self, with_task):
        print(len(f'dužina stringa: {with_task.data=}'))
        if not with_task.data:
            raise ValidationError('Polje je obavezno')

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

    vehicle_id = SelectField('Službeno vozilo: ', validators=[Optional()])
    together_with = SelectField('Zajedno sa: ', validators=[Optional()], choices=[])
    personal_vehicle_id = SelectField('Privatno vozilo: ', validators=[Optional()])
    other = StringField('Drugo: ')

    advance_payment = DecimalField('Akontacija: ', validators=[NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    daily_wage = DecimalField('Iznos dnevnice u državi: ', validators=[NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu: ', validators=[NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    daily_wage_abroad_currency = SelectField('Valuta: ', choices=[('€', 'EUR'), ('usd', 'USD')])
    costs_pays = StringField('Putni troškovi padaju na teret: ')
    principal_id = SelectField('Nalogodavac:', validators=[Optional()], choices=[])
    cashier_id = SelectField('Blagajnik: ', validators=[Optional()], choices=[])

    status = SelectField('Status: ', choices=[("kreiran", "kreiran"), ("završen", "završen"), ("obračunat", "obračunat") , ("storniran", "storniran")]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)
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
    personal_vehicle_id = SelectField('Privatno vozilo: ', validators=[Optional()])
    other = StringField('Drugo: ')

    # advance_payment = IntegerField('Akontacija: ')
    # advance_payment_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    # daily_wage = IntegerField('Dnevnica: ')
    # daily_wage_currency = SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    # costs_pays = StringField('Putni troškovi padaju na teret: ')

    status = SelectField('Status: ', choices=[("kreiran", "kreiran"), ("završen", "završen")]) #1 - kreiran, 2 - u delu, 3 - kompletiran od strane radnika (popunjeno sve: sati, km, troškovi...), 4 - završen od strane administratora (arhiviran)
    # expenses = FloatField('Ukupni troškovi', validators=[DataRequired()])

    add_expenses = SubmitField('Dofaj trošak')
    submit = SubmitField('Ažurirajte putni nalog')

    def reset(self):
        self.__init__()


class TravelWarrantExpensesForm(FlaskForm):
    expenses_type = SelectField('Tip troška', choices=[('Ostali troškovi na službenom putu', 'Ostali troškovi na službenom putu'), ('Parkiranje', 'Parkiranje'), ('Putarine', 'Putarine'), ('Troškovi amortizacije privatnog vozila', 'Troškovi amortizacije privatnog vozila'), ('Troškovi noćenja', 'Troškovi noćenja'), ('Troškovi prevoza', 'Troškovi prevoza'), ('Troškovi smeštaja i ishrane', 'Troškovi smeštaja i ishrane')] )
    description = TextAreaField('Opis troška: ')
    amount = DecimalField('Iznos: ', validators=[DataRequired(), NumberRange(min=0, message='Iznos troška mora biti veći od 0.')])
    amount_currency =  SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    submit = SubmitField('Dodajte trošak')

    def reset(self):
        self.__init__()


class EditTravelWarrantExpenses(FlaskForm):
    expenses_type = SelectField('Tip troška', choices=[('Ostali troškovi na službenom putu', 'Ostali troškovi na službenom putu'), ('Parkiranje', 'Parkiranje'), ('Putarine', 'Putarine'), ('Troškovi amortizacije privatnog vozila', 'Troškovi amortizacije privatnog vozila'), ('Troškovi noćenja', 'Troškovi noćenja'), ('Troškovi prevoza', 'Troškovi prevoza'), ('Troškovi smeštaja i ishrane', 'Troškovi smeštaja i ishrane')] )
    description = TextAreaField('Opis troška: ')
    amount = DecimalField('Iznos: ', validators=[DataRequired(), NumberRange(min=0, message='Iznos troška mora biti veći od 0.')])
    amount_currency =  SelectField('Valuta: ', choices=[('rsd', 'RSD'), ('€', 'EUR'), ('usd', 'USD')])
    submit = SubmitField('Ažurirajte trošak')

    def reset(self):
        self.__init__()
