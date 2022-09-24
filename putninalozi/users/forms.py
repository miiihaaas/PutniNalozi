from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from putninalozi import db
from putninalozi.models import Company, User


class RegistrationUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Pol', validators=[DataRequired()], choices = [(0, 'SREDNJI'),(1, 'MUŠKI'),(2, 'ŽENSKI')])
    workplace = StringField('Radno Mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo Autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')])
    company_id = SelectField('Kompanija', choices=Company.query.all()) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Registruj Korisnika')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Taj email je već zauzet, izaberide drugi email')

    def reset(self):
        self.__init__()


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Pol', validators=[DataRequired()], choices=[(0, 'SREDNJI'), (1, 'MUŠKI'), (2, 'ŽENSKI')])
    workplace = StringField(label='Radno Mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo Autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_admin', 'ADMIN')]) #[('c_user', 'USER'),('c_admin', 'ADMIN')]) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    company_id = SelectField('Kompanija', choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]) #, choices=Company.query.all())
    submit = SubmitField('Ažuriraj Korisnika')

    def reset(self):
        self.__init__()



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember = BooleanField('Zapamti Me')
    submit = SubmitField('Prijaviti Se')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Zatraži Reset Lozinke')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ne postoji korisnik sa Vašim emailom. Zatražite od vašeg administratora da Vam otvori nalog.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Lozinka', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrdi Lozinku', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Resetuj Lozinku')
