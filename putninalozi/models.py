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
        return f"User('{self.id}', '{self.email}', '{self.name}', '{self.surname}', '{self.authorization}')"


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(10), nullable = False)
    vehicle_brand = db.Column(db.String(10), nullable = False)
    vehicle_registration = db.Column(db.String(12), nullable = False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)

    def __repr__(self):
        return f"Vehicle('{self.id}', '{self.vehicle_type}', '{self.vehicle_brand}'', '{self.vehicle_registration}', '{self.company_id}')"


class TravelWarrant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    #nastaviti sa dodavanjem potrebnih polja (nakon definisanja), napisati formu (forms.py), dodati funkciju (routes.py) i napraviti html fajl


db.create_all()
db.session.commit()
