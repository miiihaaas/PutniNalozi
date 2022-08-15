from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField
from wtforms.validators import DataRequired
from putninalozi.models import Company, User
from flask_login import current_user



class CreateTravelWarrantForm(FlaskForm):
    choices=User.query.all()
    user_id = SelectField('User ID', choices=choices)
    with_task = StringField('Sa Zadatkom: ', validators=[DataRequired()])
    workplace = StringField('Radno Mesto: ', validators=[DataRequired()]) ###
    abroad = BooleanField('Putovanje U Inostranstvo')
    abroad_contry = StringField('Država: ', validators=[DataRequired()])
    date_start = DateField('Polazno Vreme: ', format='dd.mm.yyyy' )
    time_start = TimeField('Polazno Vreme: ', format='%d-%m-%Y' )
    date_end = DateField('Vreme Završetka: ', format='dd.mm.yyyy' )
    time_end = TimeField('Vreme Završetka: ', format='%d-%m-%Y' )
    relation = StringField('Relacija:', validators=[DataRequired()])
    trip_approved_by = StringField('Putovanje Odobrio: ', validators=[DataRequired()])
    travel_expenses_paid_by = StringField('Putne Troškove Plaća: ', validators=[DataRequired()])
    advance_payment_amount = StringField('Iznos Akontacije: ', validators=[DataRequired()])
    advance_payment_amount_currency = SelectField('Valuta', validators=[DataRequired()], choices=[('rsd', 'DIN'),('eur', '€'),('usd', '$')])
    amount_of_daily_wages = StringField('Iznos Dnevnice: ', validators=[DataRequired()])
    amount_of_daily_wages_currency = SelectField('Valuta', validators=[DataRequired()], choices=[('rsd', 'DIN'),('eur', '€'),('usd', '$')])
    approve_usage_of = StringField('Odobrava se upotreba: ', validators=[DataRequired()])
    km_start = StringField('Početna Kilometraža', validators=[DataRequired()])
    km_end = StringField('Završna Kilometraža', validators=[DataRequired()])
    pass
    #nastaviti

class EditTravelWarrantForm(FlaskForm):
    pass
    #nastaviti
