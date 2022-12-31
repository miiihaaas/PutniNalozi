from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from putninalozi import db
from putninalozi.models import Company, User


class RegistrationUserForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Pol', validators=[DataRequired()], choices = [(1, 'muški'),(2, 'ženski')])
    workplace = StringField('Radno mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_principal', 'NALOGODAVAC'),('c_cashier', 'BLAGAJNIK'),('c_admin', 'ADMIN'),('c_founder', 'OSNIVAČ')])
    company_id = SelectField('Kompanija', choices=Company.query.all()) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    default_vehicle = SelectField('Dodeljeno vozilo', validators=[DataRequired()], choices = [])
    submit = SubmitField('Registrujte profil korisnika')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Taj email je već zauzet, izaberide drugi email')

    def reset(self):
        self.__init__()


class UpdateUserForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    name = StringField('Ime', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Prezime', validators=[DataRequired(), Length(min=2, max=20)])
    gender = SelectField('Pol', validators=[DataRequired()], choices=[ (1, 'muški'), (2, 'ženski')])
    workplace = StringField(label='Radno mesto', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Nivo autorizacije', validators=[DataRequired()], choices = [('c_user', 'USER'),('c_principal', 'NALOGODAVAC'),('c_cashier', 'BLAGAJNIK'),('c_admin', 'ADMIN'),('c_founder', 'OSNIVAČ')])
    company_id = SelectField('Kompanija', choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]) #, choices=Company.query.all())
    default_vehicle = SelectField('Dodeljeno vozilo', validators=[DataRequired()], choices = [])
    submit = SubmitField('Ažurirajte profil korisnika')

    def reset(self):
        self.__init__()



class LoginForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    password = PasswordField('Lozinka', validators=[DataRequired()])
    remember = BooleanField('Zapamti me')
    submit = SubmitField('Prijavite se')


class RequestResetForm(FlaskForm):
    email = StringField('Mejl', validators=[DataRequired(), Email()])
    submit = SubmitField('Zatražite reset lozinke')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Ne postoji korisnik sa Vašim emailom. Zatražite od vašeg administratora da Vam otvori nalog.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nova lozinka', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrdite novu lozinku', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Resetujte lozinku')
