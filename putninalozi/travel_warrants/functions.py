#Fajl u kojem se nalaze funkcije koje se koriste u drugim fajlovima istog foldera
from putninalozi.models import TravelWarrant


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