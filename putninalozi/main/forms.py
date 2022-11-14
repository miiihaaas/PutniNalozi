from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired
from putninalozi.models import Settings


class SettingsForm(FlaskForm):
    daily_wage_domestic = DecimalField('Iznos dnevnice u državi', validators=[DataRequired()])
    daily_wage_abroad = DecimalField('Iznos dnevnice u inostranstvu', validators=[DataRequired()])
    submit = SubmitField('Ažurirajte podatke')
