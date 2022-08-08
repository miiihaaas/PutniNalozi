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
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    old_email = StringField('Old Email', validators=[DataRequired(), Email()]) # služi za validaciju prilikom promene podataka usera...
    # password = PasswordField('New Password', validators=[DataRequired()]) #stavljaće se podrazumevana šifra tipa: korisnik1234
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    authorization = SelectField('Authorization Level', validators=[DataRequired()], choices=[('c_user', 'USER'),('c_admin', 'ADMIN')]) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    company_id = SelectField('Company ID', choices=Company.query.all()) #Company.query.all()  vs  [(1, 'Helios'),(2, 'Metalac')]
    submit = SubmitField('Update User')

    def validate_email(self, email, old_email):
        print(f'{email.data=}')

        user = User.query.filter_by(email=old_email.data).first()
        # print(f'{user.email=}')
        # print(f'{user.id=}')
        user = User.query.filter_by(email=user.old_email).first()
        # print(f'{user.email=}')
        if user.old_email != user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken, please choose a different one')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You have to ask your admin to create an account.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
