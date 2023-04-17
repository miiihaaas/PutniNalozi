from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from putninalozi.models import Settings


class SettingsForm(FlaskForm):
    daily_wage_domestic = DecimalField('Iznos dnevnice u državi (RSD)', validators=[DataRequired(), NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu (€)', validators=[DataRequired(), NumberRange(min=0, message='Iznos dnevnice mora biti veći od 0.')])
    send_email_kreiran = BooleanField('Slanje mejla korisniku prilikom kreiranja putnog naloga', default=False)
    send_email_kreiran_principal = BooleanField('Slanje mejla nalogodavcu prilikom kreiranja putnog naloga', default=False)
    send_email_zavrsen = BooleanField('Slanje mejla nalogodavcu o završetku putnog naloga', default=False)
    send_email_obracunat_cashier = BooleanField('Slanje mejla blagajniku po obračunavanju putnog naloga', default=False)
    submit = SubmitField('Ažurirajte podatke')
