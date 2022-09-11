import pandas as pd
from putninalozi.models import User, Vehicle, Company, TravelWarrant
from putninalozi import db

x = input('da li žeiš da izezeš User u excel? (y/n)')
if x=='y':
    records = db.session.query(User.id, User.email, User.password, User.name, User.surname, User.authorization, User.company_id).all()
    df = pd.DataFrame(data=records, )

    print(df)

    with pd.ExcelWriter('backup_data.xlsx', mode='a', if_sheet_exists='replace') as writer: #if_sheet_exists{‘error’, ‘new’, ‘replace’, ‘overlay’}, default ‘error’
        df.to_excel(writer, sheet_name='Users_export')

x = input('da li žeiš da izezeš Company u excel? (y/n)')
if x=='y':
    records = db.session.query(Company.id, Company.companyname, Company.company_address, Company.company_address_number, Company.company_zip_code, Company.company_city, Company.company_state, Company.company_state, Company.company_pib, Company.company_mb, Company.company_site, Company.company_mail, Company.company_phone, Company.company_logo).all()
    df = pd.DataFrame(data=records, )

    print(df)

    with pd.ExcelWriter('backup_data.xlsx', mode='a', if_sheet_exists='replace') as writer: #if_sheet_exists{‘error’, ‘new’, ‘replace’, ‘overlay’}, default ‘error’
        df.to_excel(writer, sheet_name='Company_export')

x = input('da li žeiš da masovno uneseš korisnike iz exel fajla? (y/n)')
if x=="y":
    df = pd.read_excel('D:\Mihas\Programming\Python\Projects\PutniNalozi\\backup_data.xlsx', sheet_name='Users_input')

    for index, row in df.iterrows():
        user_input = User(id=row['id'],
                            email=row['email'],
                            password=row['password'],
                            name=row['name'],
                            surname=row['surname'],
                            gender=row['gender'],
                            workplace=row['workplace'],
                            authorization=row['authorization'],
                            company_id=row['company_id'])
        print(user_input)
        db.session.add(user_input)
        db.session.commit()
