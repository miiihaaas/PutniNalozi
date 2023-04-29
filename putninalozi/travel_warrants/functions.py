#Fajl u kojem se nalaze funkcije koje se koriste u drugim fajlovima istog foldera
from flask import  render_template, flash, request, url_for
from flask_mail import Message
from putninalozi import app, mail
from putninalozi.models import TravelWarrant
# from putninalozi.travel_warrants.pdf_form import update_pdf_form

#! koristi se u fajlu: routes.py
def send_email(warrant, current_user, file_name, global_settings):
    subject = ""
    recipients = []
    cc = []
    if warrant.status == 'kreiran':
        subject = f'Kreiran je putni nalog broj: {warrant.travel_warrant_number}'
        text_body = f'''Poštovani,

Kreiran je putni nalog broj {warrant.travel_warrant_number}.
Detaljnije informacije o putnom nalogu mogu se videti u dokumentu u prilogu ili klikom na link:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

S poštovanjem,
{current_user.name} {current_user.surname}'''
        if global_settings.send_email_kreiran and global_settings.send_email_kreiran_principal:
            recipients = [warrant.travelwarrant_user.email]
            cc = [warrant.principal_user.email]
        elif global_settings.send_email_kreiran:
            recipients = [warrant.travelwarrant_user.email]
        elif global_settings.send_email_kreiran_principal:
            recipients = [warrant.principal_user.email]
    # ako je završen nalog: adminu / nalogodavcu
    elif warrant.status == 'završen':
        subject = f'Završen je putni nalog broj: {warrant.travel_warrant_number}'
        text_body = f'''Poštovani,

Završen je putni nalog broj {warrant.travel_warrant_number}. Klikom na link u nastavku, možete obračunati putni nalog:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

S poštovanjem,
{warrant.travelwarrant_user.name} {warrant.travelwarrant_user.surname}'''
        if global_settings.send_email_zavrsen:
            recipients = [warrant.principal_user.email]
    # ako je obračunat nalog: blagajniku i korisniku
    elif warrant.status == 'obračunat':
        subject = f'Obračunat je putni nalog broj: {warrant.travel_warrant_number}'
        text_body = f'''Poštovani,
        
Obračunat je putni nalog broj {warrant.travel_warrant_number}. Možete izvršiti isplatu dnevnica prema podacima iz dokumenta u prilogu.'''
        if global_settings.send_email_obracunat_cashier:
            recipients = [warrant.cashier_user.email]
    else:
        return
    # ako je storniran nalog: da li treba nekoga da obaveštava?
    msg = Message(subject,
                    sender='noreply@putninalozi.online',
                    recipients=recipients, cc=cc)
    msg.body = text_body
    path = 'static/pdf_forms/'
    file_name = file_name
    print(path)
    print(file_name)
    print(path+file_name)
    with app.open_resource(path + file_name) as fp:
        msg.attach(path + file_name, 'application/pdf', fp.read())

    mail.send(msg)

#! koristi se u fajlu: routes.py
def proracun_broja_dnevnica(br_casova):
    if br_casova < 8:
        br_dnevnica = 0.0
        print(f'ispod 8h: {br_dnevnica=}')
    elif br_casova < 12:
        br_dnevnica = 0.5
        print(f'od 8h do 12h: {br_dnevnica=}')
    else:
        br_dnevnica = br_casova / 24
        print(f'proračun: {br_dnevnica=}')
        if br_dnevnica % 1 <= (8/24): #zaokruživanje na 0.5 (da li je 0-12h ili 8-12h)
            #zaokruži na x.0
            br_dnevnica = br_dnevnica // 1
            print(f'zaokruživanje na pola dnevnice: {br_dnevnica=}')
        elif br_dnevnica % 1 <= (12/24): #zaokruživanje na 0.5 (da li je 0-12h ili 8-12h)
            #zaokruži na x.5
            br_dnevnica = br_dnevnica // 1 + 0.5
            print(f'zaokruživanje na pola dnevnice: {br_dnevnica=}')
        else:
            #zaokruži na x+1
            br_dnevnica = br_dnevnica // 1 + 1
            print(f'zaokruživanje na celu dnevnicu: {br_dnevnica=}')
    br_dnevnica = br_dnevnica * 1.0
    return br_dnevnica

#! koristi se u fajlu: routes.py
def update_warrant(warrant, form, global_settings, current_user, status):
    print('ušao sam u def update_warrant')
    print(f'{current_user.authorization=}')
    warrant.with_task = form.with_task.data
    warrant.abroad = form.abroad.data
    warrant.abroad_contry = form.abroad_contry.data
    warrant.relation = form.relation.data.title()
    warrant.start_datetime = form.start_datetime.data
    warrant.end_datetime = form.end_datetime.data
    warrant.contry_leaving = form.contry_leaving.data
    warrant.contry_return = form.contry_return.data
    warrant.together_with = form.together_with.data if form.together_with.data else ""
    warrant.personal_vehicle_id = form.personal_vehicle_id.data if form.personal_vehicle_id.data else None
    warrant.other = form.other.data.upper() if form.other.data else ""
    
        
    print(f'{request.form.get("dugme")=}')
    if request.form.get('dugme') == 'Završi':
        print('kliknuto je dugme ZAVRŠI')
        warrant.status = 'završen'
        # todo send email nalogodavcu
        if global_settings.send_email_zavrsen:
            send_email(warrant, current_user, warrant.file_name, global_settings)
            flash(f'{warrant.principal_user.name} je {"dobio" if warrant.principal_user.gender == "1" else "dobila"} mejl sa informacijom da je putni nalog završen.', 'success')
    elif request.form.get('dugme') == 'Obračunajte':
        warrant.status = 'obračunat'
        #todo send email zaposlenom, blagajniku
        if global_settings.send_email_obracunat_cashier:
            send_email(warrant, current_user, warrant.file_name, global_settings)
            flash(f'{warrant.cashier_user.name} je {"dobio" if warrant.cashier_user.gender == "1" else "dobila"} mejl sa informacijom da je putni nalog obračunat.', 'success')
    else:
        warrant.status = status
    print(f'{current_user.authorization=}')
    if current_user.authorization in ['c_admin', 's_admin', 'c_functionary', 'c_founder', 'c_cashier', 'o_cashier']:
        warrant.advance_payment = int(form.advance_payment.data)
        warrant.advance_payment_currency = form.advance_payment_currency.data
        warrant.daily_wage = int(form.daily_wage.data)
        warrant.daily_wage_currency = form.daily_wage_currency.data
        warrant.daily_wage_abroad = form.daily_wage_abroad.data
        warrant.daily_wage_abroad_currency = form.daily_wage_abroad_currency.data
        warrant.costs_pays = form.costs_pays.data
        
        warrant.principal_id = form.principal_id.data
        warrant.cashier_id = form.cashier_id.data
    print(f'{form.vehicle_id.data=}')
    if form.vehicle_id.data != '':
        warrant.vehicle_id = form.vehicle_id.data



#! koristi se u fajlu pdf_form.py
def replace_serbian_characters(string):
    replacements = {
        "č": "c",
        "ć": "c",
        "đ": "dj",
        "ž": "z",
        "š": "s",
        "Č": "C",
        "Ć": "C",
        "Đ": "Dj",
        "Ž": "Z",
        "Š": "S"
    }
    for key, value in replacements.items():
        string = string.replace(key, value)
    return string


#! koristi se u fajlu pdf_form.py
def get_warrant_details(warrant):
    warrant_number = warrant.travel_warrant_number
    name = warrant.travelwarrant_user.name
    surname = warrant.travelwarrant_user.surname
    authorization = warrant.travelwarrant_user.authorization #!
    workplace = warrant.travelwarrant_user.workplace
    with_task = warrant.with_task
    relation = warrant.relation
    abroad_contry = warrant.abroad_contry
    costs_pays = warrant.costs_pays
    start_datetime = warrant.start_datetime.strftime('%d.%m.%Y')
    end_datetime = warrant.end_datetime.strftime('%d.%m.%Y')
    if warrant.together_with != '':
        try:
            regisrtacija_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_vehicle.vehicle_registration
            automobil_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_vehicle.vehicle_brand
        except AttributeError:
            # If the 'vehicle_registration' attribute is not found, try getting the 'vehicle_registration' from the 'travelwarrant_personal' object
            regisrtacija_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_personal.vehicle_registration
            automobil_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_personal.vehicle_brand
    else:
        regisrtacija_kolege_koji_vozi = ''
        automobil_kolege_koji_vozi = ''
        
    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega", 'izvršio']
        pozicija = ["Zaposleni", "Član", "Funkcioner", "Osnivač"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice", 'izvršila']
        pozicija = ["Zaposlena", "Članica", "Funkcionerka", "Osnivačica"]
        
    if authorization in ["c_user", "c_admin", "c_cashier"]:
        startna_recenica = f"{pozicija[0]} {name} {surname} {rod[1]} na poslove radnog mesta {workplace}"
    elif authorization == 'c_member':
        startna_recenica = f"{pozicija[1]} {name} {surname}"
    elif authorization == 'c_functionary':
        startna_recenica = f"{pozicija[2]} {name} {surname}"
    elif authorization == 'c_founder':
        startna_recenica = f"{pozicija[3]} {name} {surname}"
    return warrant_number, name, surname, with_task, relation, abroad_contry, costs_pays, start_datetime, end_datetime, regisrtacija_kolege_koji_vozi, automobil_kolege_koji_vozi, rod, startna_recenica