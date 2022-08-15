from putninalozi import app, db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    companyname = db.Column(db.String(20), unique=True, nullable=False)         #Helios, Metalac, Tetrapak, Foka, Papir Print
    # companyname_short = db.Column(db.String(5), unique=True, nullable=False)    #HLS, MTLC,TTRPK, FOKA, PPRPT
    company_address = db.Column(db.String(20), unique=False, nullable=False)
    company_address_number = db.Column(db.Integer, nullable=False)
    company_zip_code = db.Column(db.Integer, nullable=False)
    company_city = db.Column(db.String(20), unique=False, nullable=False)
    company_state = db.Column(db.String(20), unique=False, nullable=False)
    company_pib = db.Column(db.Integer, nullable=False)
    company_mb = db.Column(db.Integer, nullable=False)
    company_site = db.Column(db.String(20), unique=True, nullable=False) #vidi imali neki model tipa db.Link()
    company_mail = db.Column(db.String(120), unique=True, nullable=False)
    company_phone = db.Column(db.Integer, nullable=False)
    company_logo = db.Column(db.String(60), nullable=False)
    users = db.relationship('User', backref='user_company', lazy=True)
    vehicles = db.relationship('Vehicle', backref='vehicle_company', lazy=True)
    travelwarrants = db.relationship('TravelWarrant', backref='travelwarrants_company', lazy=True)

    def __repr__(self):
        return self.companyname



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(20), unique=True, nullable=False) #predlog je da bude standardizovano: npr prva tri slova prezimena, imena (PANMIH, SIMDUS)
    email = db.Column(db.String(120), unique=True, nullable=False)
    old_email = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(60), nullable = False)
    name = db.Column(db.String(20), unique=False, nullable=False)
    surname = db.Column(db.String(20), unique=False, nullable=False)
    authorization = db.Column(db.String(10), nullable = False) # ovde treba da budu tipovi korisnika: S_admin, C_admin, C_user
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    travelwarrants = db.relationship('TravelWarrant', backref='travelwarrant_user', lazy=True)

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
        return self.name + " " + self.surname


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(10), nullable = False)
    vehicle_brand = db.Column(db.String(10), nullable = False)
    vehicle_registration = db.Column(db.String(12), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __repr__(self):
        return f"Vehicle('{self.id}', '{self.vehicle_type}', '{self.vehicle_brand}'', '{self.vehicle_registration}', '{self.company_id}')"


class TravelWarrant(db.Model):
    travel_warrant_id = db.Column(db.Integer, primary_key=True)
    with_task = db.Column(db.String(50), nullable=False)
    workplace = db.Column(db.String(50), nullable=False)
    abroad = db.Column(db.Boolean, nullable=False)
    abroad_contry = db.Column(db.String(50), nullable=False) # čekboks za putovanje u inostranstvo
    relation = db.Column(db.String(150), nullable=False)
    date_start = db.Column(db.DateTime, nullable=False)
    date_end = db.Column(db.DateTime, nullable=False)
    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    trip_approved_by = db.Column(db.String(50), nullable=False)                 # putnovanje odobrio
    travel_expenses_paid_by = db.Column(db.String(50), nullable=False)          # npr firma zaposlenog ili firma kod koje se ide (kupac, dobavljač)
    advance_payment_amount = db.Column(db.Integer, nullable=False)              # iznos akontacije
    advance_payment_amount_currency = db.Column(db.String(3), nullable=False)   # valuta (rsd, eur, dol...)
    amount_of_daily_wages = db.Column(db.Integer, nullable=False)               # iznos dnevnice
    amount_of_daily_wages_currency = db.Column(db.String(3), nullable=False)    # valuta (rsd, eur, dol...)
    approve_usage_of = db.Column(db.String(30), nullable=False)                 #odobrava se upotreba (ili: službenog [lista vozila]. ličnog vozila [tip, marka registracija], drugo [autobus, avion...]
        #dodati podkategorije koje će da budu viljive u odnosu na odabranu opciju (službenog, ličnog, drugo)
    km_start = db.Column(db.Integer, nullable=False)
    km_end = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)                              #(1 - priprema, 2 - u delu, 3 - završen, 4 - arhiviran)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    #nastaviti sa dodavanjem potrebnih polja (nakon definisanja), napisati formu (forms.py), dodati funkciju (routes.py) i napraviti html fajl



db.create_all()
db.session.commit()
