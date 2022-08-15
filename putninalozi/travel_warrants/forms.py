from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from putninalozi.models import Company, User, Vehicle
from flask_login import current_user



class CreateTravelWarrantForm(FlaskForm):
    user_id = SelectField('Zaposleni:', choices=User.query.all())
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
    approve_usage_of = SelectField('Odobrava se upotreba: ', validators=[DataRequired()], choices=['službenog vozila', 'sa kolegom (ukucati broj putnog naloga kolege)', 'ličnog vozila', 'drugo (autobus, avion...)'])
    km_start = StringField('Početna Kilometraža', validators=[DataRequired()])
    km_end = StringField('Završna Kilometraža', validators=[DataRequired()])
    approve_usage_of_lisa_vozila = SelectField('Službeno Vozilo:', choices=Vehicle.query.all())
    approve_usage_of_sa_kolegom = IntegerField('Broj Koleginog Putnog Naloga:', validators=[DataRequired()])
    approve_usage_of_licno_vozilo_tip = StringField('Tip Vozila:', validators=[DataRequired()])
    approve_usage_of_licno_vozilo_marka = StringField('Marka Vozila:', validators=[DataRequired()])
    approve_usage_of_licno_vozilo_registracija = StringField('Registracija Vozila:', validators=[DataRequired()])
    approve_usage_of_drugo = StringField('Drugo (autobus, avion, taksi, rentakar...) :', validators=[DataRequired()])
    submit = SubmitField('Sačuvaj Putni Nalog')
    #nastaviti

class EditTravelWarrantForm(FlaskForm):
    pass
    #nastaviti
