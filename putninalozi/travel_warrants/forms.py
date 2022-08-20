from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, DateField, TimeField, DateTimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from putninalozi.models import Company, User, Vehicle
from flask_login import current_user
from putninalozi import db
# from putninalozi.travel_warrants.routes import users_list


class CreateTravelWarrantForm(FlaskForm):
    with_task = StringField('Sa Zadatkom: ', validators=[DataRequired()])
    user_id = SelectField('Zaposleni:', validators=[DataRequired()], choices=[(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).all()]) #umesto users: db.session.query(User.id,User.name,User.surname).all()
    company_id = SelectField('Company ID', validators=[DataRequired()], choices=[(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()])
    abroad_contry = StringField('Država: ')
    relation = StringField('Relacija: ', validators=[DataRequired()])
    start_datetime = DateTimeField('Polazno Vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_datetime = DateTimeField('Završno Vreme: ', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Kreiraj Putni Nalog')
    #nastaviti

    def reset(self):
        self.__init__()
        self.users = [(u.id, u.name+" " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).all()]
        print(current_user.user_company.companyname)
        print(self.users)
        return self.users





class EditTravelWarrantForm(FlaskForm):
    pass

    def reset(self):
        self.__init__()
    #nastaviti
