import pandas as pd
from putninalozi.models import User, Vehicle, Company, TravelWarrant
from putninalozi import db

x = input('da li žeiš da izezeš User u excel? (y/n)')
if x=='y':
    records = db.session.query(User.id,
                                User.email,
                                User.password,
                                User.name,
                                User.surname,
                                User.gender,
                                User.workplace,
                                User.authorization,
                                User.company_id).all()
    df = pd.DataFrame(data=records, )

    print(df)

    with pd.ExcelWriter('backup_data.xlsx', mode='a', if_sheet_exists='replace') as writer: #if_sheet_exists{‘error’, ‘new’, ‘replace’, ‘overlay’}, default ‘error’
        df.to_excel(writer, sheet_name='Users_export')

x = input('da li žeiš da izezeš Company u excel? (y/n)')
if x=='y':
    records = db.session.query(Company.id,
                                Company.companyname,
                                Company.company_address,
                                Company.company_address_number,
                                Company.company_zip_code,
                                Company.company_city,
                                Company.company_state,
                                Company.company_pib,
                                Company.company_mb,
                                Company.company_site,
                                Company.company_mail,
                                Company.company_phone,
                                Company.company_logo).all()
    df = pd.DataFrame(data=records, )

    print(df)

    with pd.ExcelWriter('backup_data.xlsx', mode='a', if_sheet_exists='replace') as writer: #if_sheet_exists{‘error’, ‘new’, ‘replace’, ‘overlay’}, default ‘error’
        df.to_excel(writer, sheet_name='Company_export')

x = input('da li žeiš da izezeš TravelWarrant u excel? (y/n)')
if x=='y':
    records = db.session.query(TravelWarrant.travel_warrant_id,
                                    TravelWarrant.user_id,
                                    TravelWarrant.with_task,
                                    TravelWarrant.company_id,
                                    TravelWarrant.abroad_contry,
                                    TravelWarrant.relation,
                                    TravelWarrant.start_datetime,
                                    TravelWarrant.end_datetime,
                                    TravelWarrant.vehicle_id,
                                    TravelWarrant.together_with,
                                    TravelWarrant.personal_type,
                                    TravelWarrant.personal_brand,
                                    TravelWarrant.personal_registration,
                                    TravelWarrant.other,
                                    TravelWarrant.advance_payment,
                                    TravelWarrant.advance_payment_currency,
                                    TravelWarrant.daily_wage,
                                    TravelWarrant.daily_wage_currency,
                                    TravelWarrant.costs_pays,
                                    TravelWarrant.km_start,
                                    TravelWarrant.km_end,
                                    TravelWarrant.status).all()
    df = pd.DataFrame(data=records, )

    print(df)

    with pd.ExcelWriter('backup_data.xlsx', mode='a', if_sheet_exists='replace') as writer: #if_sheet_exists{‘error’, ‘new’, ‘replace’, ‘overlay’}, default ‘error’
        df.to_excel(writer, sheet_name='Warrants_export')

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
                            company_id=row['company_id'],
                            default_vehicle=row['default_vehicle'])
        print(user_input)
        db.session.add(user_input)
        db.session.commit()

x = input('da li žeiš da masovno uneseš kompanije iz exel fajla? (y/n)')
if x=="y":
    df = pd.read_excel('D:\Mihas\Programming\Python\Projects\PutniNalozi\\backup_data.xlsx', sheet_name='Company_input')

    for index, row in df.iterrows():
        user_input = Company(id=row['id'],
                            companyname=row['companyname'],
                            company_address=row['company_address'],
                            company_address_number=row['company_address_number'],
                            company_zip_code=row['company_zip_code'],
                            company_city=row['company_city'],
                            company_state=row['company_state'],
                            company_pib=row['company_pib'],
                            company_mb=row['company_mb'],
                            company_site=row['company_site'],
                            company_mail=row['company_mail'],
                            company_phone=row['company_phone'],
                            company_logo=row['company_logo'],
                            cashier_email=row['cashier_email'],
                            CEO=row['CEO'])
        print(user_input)
        db.session.add(user_input)
        db.session.commit()
