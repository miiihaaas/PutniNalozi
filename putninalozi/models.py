from putninalozi import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(50), unique=True, nullable=False)
    company_address = db.Column(db.String(50), unique=False, nullable=False)
    company_address_number = db.Column(db.String(5), nullable=False)
    company_zip_code = db.Column(db.Integer, nullable=False)
    company_city = db.Column(db.String(50), unique=False, nullable=False)
    company_state = db.Column(db.String(50), unique=False, nullable=False)
    company_pib = db.Column(db.Integer, nullable=False)
    company_mb = db.Column(db.Integer, nullable=False)
    company_site = db.Column(db.String(50), unique=True, nullable=False) #vidi imali neki model tipa db.Link()
    company_mail = db.Column(db.String(120), unique=True, nullable=False)
    company_phone = db.Column(db.String(20), nullable=False)
    company_logo = db.Column(db.String(60), nullable=False)
    cashier_email = db.Column(db.String(120), unique=True, nullable=False) #mejl blagajnika koji će se koristiti kada se zatvrori nalog da pošalje pdf sa preračunatim računima i potrebnoj uplati
    CEO = db.Column(db.String(120), nullable=False) #ime i prezime direkora (osobe) koji odobrava putovanje, akontaciju ...
    users = db.relationship('User', backref='user_company', lazy=True)
    vehicles = db.relationship('Vehicle', backref='vehicle_company', lazy=True)
    travelwarrants = db.relationship('TravelWarrant', backref='travelwarrant_company', lazy=True)
    settings = db.relationship('Settings', backref='settings_company', lazy=True)

    def __repr__(self):
        return self.companyname



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    surname = db.Column(db.String(20), unique=False, nullable=False)
    gender = db.Column(db.String(1)) #(0, "srednji"), (1, "muški"), (2, "ženski")
    workplace = db.Column(db.String(20), unique=False, nullable=True)
    authorization = db.Column(db.String(20), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    default_vehicle = db.Column(db.Integer) #kod radnika koji imaju svoj auto, da bude podrazumevana vrednost id tog vozila
    travelwarrants = db.relationship('TravelWarrant', backref='travelwarrant_user', lazy='dynamic', foreign_keys='TravelWarrant.user_id')
    
    principals = db.relationship('TravelWarrant', backref='principal_user', lazy='dynamic', foreign_keys='TravelWarrant.principal_id')
    cashiers = db.relationship('TravelWarrant', backref='cashier_user', lazy='dynamic', foreign_keys='TravelWarrant.cashier_id')
    admins = db.relationship('TravelWarrant', backref='admin_user', lazy='dynamic', foreign_keys='TravelWarrant.admin_id')
    # principals = db.relationship('TravelWarrant', backref='travelwarrant_user', lazy=True)
    # https://www.reddit.com/r/flask/comments/2o4ejl/af_flask_sqlalchemy_two_foreign_keys_referencing/

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"{self.id}, '{self.name} {self.surname}'"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(30), nullable = False)
    vehicle_brand = db.Column(db.String(30), nullable = False)
    vehicle_registration = db.Column(db.String(12), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    travelwarrants = db.relationship('TravelWarrant', backref='travelwarrant_vehicle', lazy=True)

    def __repr__(self):
        return f"Vehicle('{self.id}', '{self.vehicle_type}', '{self.vehicle_brand}'', '{self.vehicle_registration}', '{self.company_id}')"


class TravelWarrant(db.Model):
    travel_warrant_id = db.Column(db.Integer, primary_key=True)
    travel_warrant_number = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    with_task = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    abroad = db.Column(db.Boolean(), default=False, nullable=True)
    abroad_contry = db.Column(db.String(50), nullable=True)
    relation = db.Column(db.String(150), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=True)
    end_datetime = db.Column(db.DateTime, nullable=True)
    contry_leaving = db.Column(db.DateTime, nullable=True)
    contry_return = db.Column(db.DateTime, nullable=True)


    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=True)
    together_with = db.Column(db.String(50), nullable=True)
    personal_type = db.Column(db.String(50), nullable=True)
    personal_brand = db.Column(db.String(50), nullable=True)
    personal_registration = db.Column(db.String(12), nullable=True)
    other = db.Column(db.String(50), nullable=True) #avion, bus, taksi...

    advance_payment = db.Column(db.Float, nullable=True)
    advance_payment_currency = db.Column(db.String(5), nullable=False)
    daily_wage = db.Column(db.Float, nullable=False)
    daily_wage_currency = db.Column(db.String(5), nullable=False)
    daily_wage_abroad = db.Column(db.Float, nullable=False)
    daily_wage_abroad_currency = db.Column(db.String(5), nullable=False)
    costs_pays = db.Column(db.String(50), nullable=False)
    
    principal_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cashier_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    status = db.Column(db.String(15), nullable=False)
    file_name = db.Column(db.String(100), nullable=True) #za PDF fajl
    text_form = db.Column(db.String(1000), nullable=True) #za tekst forme iz pdf fajla
    expenses = db.relationship('TravelWarrantExpenses', backref='trawelwarrantexpenses_travelwarrant', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f"Travel Warrant('{self.travel_warrant_id=}', '{self.with_task=}', '{self.user_id=}')"


class TravelWarrantExpenses(db.Model):
    expenses_id = db.Column(db.Integer, primary_key=True)
    expenses_type = db.Column(db.String(50), nullable = True) # možda false...?
    expenses_date = db.Column(db.DateTime, nullable=True)
    description = db.Column(db.String(1000), nullable = True)
    amount = db.Column(db.Float, nullable=True)
    amount_currency = db.Column(db.String(5), nullable=False)
    travelwarrant_id = db.Column(db.Integer, db.ForeignKey('travel_warrant.travel_warrant_id'), nullable=True)

    def __repr__(self):
        return f"Travel Warrant Expenses('{self.expenses_id=}', '{self.expenses_type=}', '{self.description=}')"


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    daily_wage_domestic = db.Column(db.Float, nullable=False)
    daily_wage_abroad = db.Column(db.Float, nullable=False)
    send_email_kreiran = db.Column(db.Boolean, nullable=False)
    send_email_zavrsen = db.Column(db.Boolean, nullable=False)
    send_email_obracunat = db.Column(db.Boolean, nullable=False)


db.create_all()
db.session.commit()
