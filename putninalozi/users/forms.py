from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from putninalozi.models import Company, User


class RegistrationUserForm(FlaskForm):
    # username = StringField('Username', validators=[DataRequired(), Email()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Authorization Level', validators=[DataRequired()], choices=[('c_user', 'USER'),('c_admin', 'ADMIN')]) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    company_id = SelectField('Company ID', choices=Company.query.all()) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Register User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken, please choose a different one')


class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Authorization Level', validators=[DataRequired()], choices=[('c_user', 'USER'),('c_admin', 'ADMIN')]) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    company_id = SelectField('Company ID', choices=Company.query.all()) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Update User')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if username.data != user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken, please choose a different one')

    # def validate_email(self, email):
    # if True:
    #     pass
    # elif email.data != current_user.email:
    #         user = User.query.filter_by(email=email.data).first()
    #         if user:
    #             raise ValidationError('That email is taken, please choose a different one')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
