from putninalozi.models import User, Vehicle, Company, TravelWarrant, TravelWarrantExpenses
from putninalozi import db

x = input('da li žeiš da obrišeš sve putne naloge? (y/n)')
if x=='y':
    TravelWarrant.__table__.drop(db.engine)
    db.create_all()
    db.session.commit()

x = input('da li žeiš da obrišeš sve troškove? (y/n)')
if x=='y':
    TravelWarrantExpenses.__table__.drop(db.engine)
    db.create_all()
    db.session.commit()
