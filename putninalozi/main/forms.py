from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from putninalozi.models import Settings


class SettingsForm(FlaskForm):
    daily_wage_domestic = DecimalField('Iznos dnevnice u državi (RSD)', validators=[DataRequired()])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu (€)', validators=[DataRequired()])
    send_email_kreiran = BooleanField('Slanje mejla prilikom kreiranja putnog naloga', default=False)
    send_email_zavrsen = BooleanField('Slanje mejla prilikom završetka putnog naloga', default=False)
    send_email_obracunat = BooleanField('Slanje mejla prilikom obračunavanja putnog naloga', default=False)
    submit = SubmitField('Ažurirajte podatke')
