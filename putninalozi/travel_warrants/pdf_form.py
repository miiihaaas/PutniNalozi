from fpdf import FPDF
from flask import url_for
from flask_mail import Message
from putninalozi import app, mail
from putninalozi.broj_slovima import number_to_text
import datetime
from putninalozi.models import TravelWarrant


def replace_serbian_characters(string):
    # breakpoint()
    try:
        string = string.replace("č", "c")
    except:
        pass
    try:
        string = string.replace("ć", "c")
    except:
        pass
    try:
        string = string.replace("đ", "dj")
    except:
        pass
    try:
        string = string.replace("ž", "z")
    except:
        pass
    try:
        string = string.replace("š", "s")
    except:
        pass
    try:
        string = string.replace("Č", "C")
    except:
        pass
    try:
        string = string.replace("Ć", "C")
    except:
        pass
    try:
        string = string.replace("Đ", "Dj")
    except:
        pass
    try:
        string = string.replace("Ž", "Z")
    except:
        pass
    try:
        string = string.replace("Š", "S")
    except:
        pass
    return string


def create_pdf_form(warrant, br_casova, br_casova_ino, br_dnevnica, br_dnevnica_ino):
    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega", 'izvršio', "Osnivač"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice", 'izvršila', "Osnivač"]

    warrant_id = warrant.travel_warrant_id
    warrant_number = warrant.travel_warrant_number
    name = warrant.travelwarrant_user.name
    surname = warrant.travelwarrant_user.surname
    workplace = warrant.travelwarrant_user.workplace
    with_task = warrant.with_task
    relation = warrant.relation
    abroad_contry = warrant.abroad_contry
    costs_pays = warrant.costs_pays
    start_datetime = warrant.start_datetime.strftime('%d.%m.%Y')
    end_datetime = warrant.end_datetime.strftime('%d.%m.%Y')
    if warrant.together_with != '':
        regisrtacija_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_vehicle.vehicle_registration
    else:
        regisrtacija_kolege_koji_vozi = ''

    #za footer
    company_logo = "putninalozi/static/company_logos/" + warrant.travelwarrant_company.company_logo
    company_name = warrant.travelwarrant_company.companyname
    company_address = warrant.travelwarrant_company.company_address + f" {warrant.travelwarrant_company.company_address_number}"
    company_zip_code = warrant.travelwarrant_company.company_zip_code
    company_city = warrant.travelwarrant_company.company_city
    company_state = warrant.travelwarrant_company.company_state
    company_pib = warrant.travelwarrant_company.company_pib
    company_mb = warrant.travelwarrant_company.company_mb
    company_phone = warrant.travelwarrant_company.company_phone
    company_mail = warrant.travelwarrant_company.company_mail
    company_site = warrant.travelwarrant_company.company_site

    text_form = f'''{rod[0]} {name} {surname} {rod[1]} na poslove radnog mesta {workplace} upućuje se na službeni put dana {start_datetime} u {relation} {f'({abroad_contry})'if abroad_contry !="" else ""} sa zadatkom: {with_task}.

Na službenom putu {'koristi' if warrant.together_with == '' else 'deli'} prevozno sredstvo registarske tablice: {warrant.travelwarrant_vehicle.vehicle_registration if warrant.vehicle_id != None else ""}{warrant.personal_registration}{regisrtacija_kolege_koji_vozi}.

Dnevnica za ovo služebno putovanje pripada u iznosu od: {warrant.daily_wage} {warrant.daily_wage_currency}{f' / {warrant.daily_wage_abroad} {warrant.daily_wage_abroad_currency}' if warrant.abroad else ""}.

Na službenom putu će se zadržati najdalje do {end_datetime}, a u roku od 48h po povratku sa službenog puta i dolaska na posao, podneće pismeni izveštaj o obavljenom službenom poslu. Račun o učinjenim putnim troškovima podneti u roku od tri dana.

Putni troškovi padaju na teret: {costs_pays}.

{f'Odobravam isplatu akontacije u iznosu od: {warrant.advance_payment} {warrant.advance_payment_currency}.' if warrant.advance_payment > 0 else ""}

Nalogodavac: {warrant.principal_user.name} {warrant.principal_user.surname}.
'''


    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './putninalozi/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './putninalozi/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
        def header(self):
            # Logo
            self.image(company_logo, 1, 1, 25)
            # set font
            self.set_font('DejaVuSansCondensed', '', 8)
            # Kompanija
            self.cell(50, 3, f'                         {company_name}', ln=False, align='L')
            # PIB
            self.cell(0, 3, f'                         PIB: {company_pib}', ln=False, align='L')
            # web stranica
            self.cell(1, 3, f'                         web: {company_site}', ln=True, align='R')
            # adresa
            self.cell(50, 3, f'                         {company_address}', ln=False, align='L')
            # MB
            self.cell(0, 3, f'                         MB: {company_mb}', ln=False, align='L')
            # email
            self.cell(1, 3, f'                         email: {company_mail}', ln=True, align='R')
            # mesto
            self.cell(0, 3, f'                         {company_zip_code} {company_city}', ln=False, align='L')
            # telefon
            self.cell(1, 3, f'                         tel: {company_phone}', ln=True, align='R')
            # Država
            self.cell(8, 3, f'                         {company_state}', ln=True, align='L')
            # linija
            pdf.line(10, 30, 200, 30)
        def footer(self):
            pass

    pdf = PDF()
    pdf.alias_nb_pages()
    #todo (2.0) pdf.add_page()
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.set_font('DejaVuSansCondensed','B', 16)
    #todo (2.0) pdf.cell(0, 10, f'ODLUKA' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 10, f'o upućivanju na službeni put' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.set_font('DejaVuSansCondensed','', 12)
    #todo (2.0) pdf.multi_cell(0, 4, f'''Upućuje se na službeni put u {warrant.relation} {warrant.travelwarrant_user.name} {warrant.travelwarrant_user.surname}. Upućeni će krenuti na put dana {warrant.start_datetime.strftime("%d/%m/%Y")} sa ciljem {warrant.with_task}. Upućeni će posao obaviti bez naknade.''', border=0, ln=True, align='L')
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 30, f'' , ln=True, align='C')
    #todo (2.0) pdf.cell(0, 8, f'U {company_city}, {warrant.start_datetime.strftime("%d/%m/%Y")}' , ln=True, align='L')
    #todo (2.0) pdf.cell(0, 8, f'Ovlašćeno lice' , ln=True, align='L')
    #todo (2.0) pdf.cell(0, 6, f'_________________________' , ln=True, align='L')
    #todo (2.0) pdf.cell(0, 4, f'{warrant.principal_user.name} {warrant.principal_user.surname}' , ln=True, align='L')
    
    pdf.add_page()
    pdf.set_font('DejaVuSansCondensed','B', 16)
    pdf.cell(0, 30, f'NALOG ZA SLUŽBENO PUTOVANJE: {warrant_number}', ln=True, align='C')

    pdf.set_font('DejaVuSansCondensed','', 12)
    pdf.multi_cell(0, 5, text_form, ln=True, border='B')

    pdf.cell(0, 5, f'Na osnovu prednjeg naloga {rod[3]} sam službeno putovanje i podnosim sledeći', ln=True, align='L')
    pdf.set_font('DejaVuSansCondensed','B', 16)
    pdf.cell(0, 20, f'PUTNI RAČUN', ln=True, align='C')

    pdf.set_fill_color(150, 150, 150)
    pdf.set_font('DejaVuSansCondensed','', 8)
    pdf.cell(56, 4, f'Dnevnice', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'Br čas', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'Br dnev', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'', border=1, ln=False, fill = True, align='L')
    pdf.cell(35, 4, f'Po', border=1, ln=False, fill = True, align='L')
    pdf.cell(35, 4, f'Svega', border=1, ln=True, fill = True, align='L')
    pdf.multi_cell(56, 4, f'''Dan odlaska: {warrant.start_datetime.strftime("%d/%m/%Y, %H:%M")}
Dan povratka: {warrant.end_datetime.strftime("%d/%m/%Y, %H:%M")}''', border=1, new_y='TOP', align='L')
    pdf.cell(20, 8, f'{round(br_casova)}', border=1, new_y='LAST', align='L')
    pdf.cell(20, 8, f'{br_dnevnica}', border=1, new_y='LAST', align='L')
    pdf.cell(20, 8, f'', border=1, new_y='LAST', align='L')
    pdf.cell(35, 8, f'{warrant.daily_wage} {warrant.daily_wage_currency}', border=1, new_y='LAST', align='L')
    pdf.cell(35, 8, f'{float(warrant.daily_wage) * br_dnevnica} {warrant.daily_wage_currency}', border=1, new_x='LMARGIN', new_y='NEXT', align='L')
    if warrant.abroad:
        pdf.multi_cell(56, 4, f'''Izlazak iz države: {warrant.contry_leaving.strftime("%d/%m/%Y, %H:%M") if warrant.contry_leaving != None else '-'}
Povratak u državu: {warrant.contry_return.strftime("%d/%m/%Y, %H:%M") if warrant.contry_return != None else '-'}''', border=1, new_y='TOP', align='L')
        # pdf.set_xy(70, 174)
        pdf.cell(20, 8, f'{round(br_casova_ino)}', border=1, new_y='LAST', align='L')
        pdf.cell(20, 8, f'{br_dnevnica_ino}', border=1, ln=False, align='L')
        pdf.cell(20, 8, f'', border=1, ln=False, align='L')
        pdf.cell(35, 8, f'{warrant.daily_wage_abroad} {warrant.daily_wage_abroad_currency}', border=1, ln=False, align='L')
        pdf.cell(35, 8, f'{float(warrant.daily_wage_abroad) * br_dnevnica_ino} {warrant.daily_wage_abroad_currency}', border=1, ln=True, align='L')

    pdf.cell(56, 4, f'Prevozni troškovi', border=1, ln=False, fill = True, align='L')
    pdf.cell(40, 8, f'Vrsta prevoza', border=1, ln=False, fill = True, align='C')
    pdf.cell(20, 8, f'km.', border=1, ln=False, fill = True, align='C')
    pdf.cell(35, 8, f'dinara', border=1, ln=True, fill = True, align='C')
    pdf.cell(28, -4, f'od', border=1, ln=False, fill = True, align='C')
    pdf.cell(28, -4, f'do', border=1, ln=True, fill = True, align='C')
    pdf.cell(28, 4, f'', border=1, ln=True, align='L')
    for i in range(5):
        pdf.cell(28, 4, f'', border=1, ln=False, align='L')
        pdf.cell(28, 4, f'', border=1, ln=False, align='L')
        pdf.cell(40, 4, f'', border=1, ln=False, align='L')
        pdf.cell(20, 4, f'', border=1, ln=False, align='L')
        pdf.cell(35, 4, f'', border=1, ln=True, align='L')
    pdf.cell(151, 8, f'Ostalo', border=1, ln=True, fill = True, align='L')
    for i in range(3):
        pdf.cell(116, 4, f'', border=1, ln=False, align='L')
        pdf.cell(35, 4, f'', border=1, ln=True, align='L')
    pdf.cell(151, 4, f'Svega', border=1, ln=True, align='R')
    pdf.cell(151, 4, f'Primljena akontacija', border=1, ln=False, align='R')
    pdf.cell(35, 4, f'', border=1, ln=True, align='C')
    pdf.cell(151, 4, f'Ostalo za isplatu - uplatu', border=1, ln=False, align='R')
    pdf.cell(35, 4, f'', border=1, ln=True, align='C')
    pdf.cell(186, 4, f'Prilog', border=1, ln=True, fill = True, align='L')
    pdf.multi_cell(186, 4, f'''U mestu {warrant.travelwarrant_company.company_city}, dana {warrant.start_datetime.strftime("%d/%m/%Y")}, {warrant.travelwarrant_user.name} {warrant.travelwarrant_user.surname}''', border=1, ln=True, align='C')
    pdf.multi_cell(0, 4, f'', ln=True, align='L')



    path = "putninalozi/static/pdf_forms/"
    file_name = replace_serbian_characters(f'{warrant_number} {company_name}-{name} {surname}.pdf')    
    pdf.output(path + file_name)
    return file_name, text_form


def update_pdf_form(warrant, br_casova, br_casova_ino, br_dnevnica, br_dnevnica_ino, troskovi):
    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega", 'izvršio']
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice", 'izvršila']

    warrant_id = warrant.travel_warrant_id
    warrant_number = warrant.travel_warrant_number
    name = warrant.travelwarrant_user.name
    surname = warrant.travelwarrant_user.surname
    workplace = warrant.travelwarrant_user.workplace
    with_task = warrant.with_task
    relation = warrant.relation
    abroad_contry = warrant.abroad_contry
    costs_pays = warrant.costs_pays
    start_datetime = warrant.start_datetime.strftime('%d.%m.%Y')
    end_datetime = warrant.end_datetime.strftime('%d.%m.%Y')
    if warrant.together_with != '':
        regisrtacija_kolege_koji_vozi = TravelWarrant.query.filter_by(travel_warrant_number=warrant.together_with).first().travelwarrant_vehicle.vehicle_registration
    else:
        regisrtacija_kolege_koji_vozi = ''

    #za footer
    company_logo = "putninalozi/static/company_logos/" + warrant.travelwarrant_company.company_logo
    company_name = warrant.travelwarrant_company.companyname
    company_address = warrant.travelwarrant_company.company_address + f" {warrant.travelwarrant_company.company_address_number}"
    company_zip_code = warrant.travelwarrant_company.company_zip_code
    company_city = warrant.travelwarrant_company.company_city
    company_state = warrant.travelwarrant_company.company_state
    company_pib = warrant.travelwarrant_company.company_pib
    company_mb = warrant.travelwarrant_company.company_mb
    company_phone = warrant.travelwarrant_company.company_phone
    company_mail = warrant.travelwarrant_company.company_mail
    company_site = warrant.travelwarrant_company.company_site

    text_form = f'''{rod[0]} {name} {surname} {rod[1]} na poslove radnog mesta {workplace} upućuje se na službeni put dana {start_datetime} u {relation} {f'({abroad_contry})'if abroad_contry !="" else ""} sa zadatkom: {with_task}.

Na službenom putu {'koristi' if warrant.together_with == '' else 'deli'} prevozno sredstvo registarske tablice: {warrant.travelwarrant_vehicle.vehicle_registration if warrant.vehicle_id != None else ""}{warrant.personal_registration}{regisrtacija_kolege_koji_vozi}.

Dnevnica za ovo služebno putovanje pripada u iznosu od: {warrant.daily_wage} {warrant.daily_wage_currency}{f' / {warrant.daily_wage_abroad} {warrant.daily_wage_abroad_currency}' if warrant.abroad else ""}.

Na službenom putu će se zadržati najdalje do {end_datetime}, a u roku od 48h po povratku sa službenog puta i dolaska na posao, podneće pismeni izveštaj o obavljenom službenom poslu. Račun o učinjenim putnim troškovima podneti u roku od tri dana.

Putni troškovi padaju na teret: {costs_pays}.

{f'Odobravam isplatu akontacije u iznosu od: {warrant.advance_payment} {warrant.advance_payment_currency}.' if warrant.advance_payment > 0 else ""}

Nalogodavac: {warrant.principal_user.name} {warrant.principal_user.surname}.
'''


    class PDF(FPDF):
        def __init__(self, **kwargs):
            super(PDF, self).__init__(**kwargs)
            self.add_font('DejaVuSansCondensed', '', './putninalozi/static/fonts/DejaVuSansCondensed.ttf', uni=True)
            self.add_font('DejaVuSansCondensed', 'B', './putninalozi/static/fonts/DejaVuSansCondensed-Bold.ttf', uni=True)
        def header(self):
            # Logo
            self.image(company_logo, 1, 1, 25)
            # set font
            self.set_font('DejaVuSansCondensed', '', 8)
            # Kompanija
            self.cell(50, 3, f'                         {company_name}', ln=False, align='L')
            # PIB
            self.cell(0, 3, f'                         PIB: {company_pib}', ln=False, align='L')
            # web stranica
            self.cell(1, 3, f'                         web: {company_site}', ln=True, align='R')
            # adresa
            self.cell(50, 3, f'                         {company_address}', ln=False, align='L')
            # MB
            self.cell(0, 3, f'                         MB: {company_mb}', ln=False, align='L')
            # email
            self.cell(1, 3, f'                         email: {company_mail}', ln=True, align='R')
            # mesto
            self.cell(0, 3, f'                         {company_zip_code} {company_city}', ln=False, align='L')
            # telefon
            self.cell(1, 3, f'                         tel: {company_phone}', ln=True, align='R')
            # Država
            self.cell(8, 3, f'                         {company_state}', ln=True, align='L')
            # linija
            pdf.line(10, 30, 200, 30)
        def footer(self):
            pass

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font('DejaVuSansCondensed', 'B', 16)
    pdf.cell(0, 30, f'NALOG ZA SLUŽBENO PUTOVANJE: {warrant_number}', ln=True, align='C')

    pdf.set_font('DejaVuSansCondensed','', 12)
    pdf.multi_cell(0, 5, text_form, ln=True, border='B')
    # pdf.line(10, 132, 200, 132)

    pdf.cell(0, 5, f'Na osnovu prednjeg naloga {rod[3]} sam sluzbeno putovanje i podnosim sledeći', ln=True, align='L')
    pdf.set_font('DejaVuSansCondensed','B', 16)
    pdf.cell(0, 20, f'PUTNI RAČUN', ln=True, align='C')

    pdf.set_fill_color(150, 150, 150)
    pdf.set_font('DejaVuSansCondensed','', 8)
    pdf.cell(60, 4, f'Dnevnice', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'Br čas', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'Br dnev', border=1, ln=False, fill = True, align='L')
    pdf.cell(20, 4, f'', border=1, ln=False, fill = True, align='L')
    pdf.cell(35, 4, f'Po', border=1, ln=False, fill = True, align='L')
    pdf.cell(35, 4, f'Svega', border=1, ln=True, fill = True, align='L')
    pdf.multi_cell(60, 4, f'''Dan odlaska: {warrant.start_datetime.strftime("%d/%m/%Y, %H:%M")}
Dan povratka: {warrant.end_datetime.strftime("%d/%m/%Y, %H:%M")}''', border=1, new_y='TOP', align='L')
    # pdf.set_xy(70, 166)
    pdf.cell(20, 8, f'{round(br_casova)}', border=1, new_y='LAST', align='L')
    pdf.cell(20, 8, f'{br_dnevnica}', border=1, new_y='LAST', align='L')
    pdf.cell(20, 8, f'', border=1, new_y='LAST', align='L')
    pdf.cell(35, 8, f'{warrant.daily_wage} {warrant.daily_wage_currency}', border=1, new_y='LAST', align='L')
    pdf.cell(35, 8, f'{float(warrant.daily_wage) * br_dnevnica} {warrant.daily_wage_currency}', border=1, new_x='LMARGIN', new_y='NEXT', align='L')
    if warrant.abroad:
        pdf.multi_cell(60, 4, f'''Izlazak iz države: {warrant.contry_leaving.strftime("%d/%m/%Y, %H:%M") if warrant.contry_leaving != None else '-'}
Povratak u državu: {warrant.contry_return.strftime("%d/%m/%Y, %H:%M") if warrant.contry_return != None else '-'}''', border=1, new_y='TOP', align='L')
        # pdf.set_xy(70, 174)
        pdf.cell(20, 8, f'{round(br_casova_ino)}', border=1, new_y='LAST', align='L')
        pdf.cell(20, 8, f'{br_dnevnica_ino}', border=1, ln=False, align='L')
        pdf.cell(20, 8, f'', border=1, ln=False, align='L')
        pdf.cell(35, 8, f'{warrant.daily_wage_abroad} {warrant.daily_wage_abroad_currency}', border=1, ln=False, align='L')
        pdf.cell(35, 8, f'{float(warrant.daily_wage_abroad) * br_dnevnica_ino} {warrant.daily_wage_abroad_currency}', border=1, ln=True, align='L')


    pdf.cell(0, 8, f'Troškovi', border=1, ln=True, fill = True, align='C')

    ukupni_trosak = 0.0
    ukupni_trosak_ino = 0.0
    ino_currency = '€'
    if troskovi != []:
        for trosak in troskovi:

            if trosak.amount_currency == 'rsd':
                ukupni_trosak = ukupni_trosak + trosak.amount
                print(ukupni_trosak)

                pdf.cell(24,4, f'{trosak.expenses_date.strftime("%d/%m/%Y")}', border=1, ln=False, align='C')
                pdf.cell(56,4, f'{trosak.expenses_type}', border=1, ln=False, align='L')
                pdf.cell(75,4, f'{trosak.description}', border=1, ln=False, align='L')
                pdf.cell(18,4, f'{trosak.amount} {trosak.amount_currency}', border=1, ln=False, align='R')
                pdf.cell(17,4, f'-', border=1, ln=True, align='C')
            else:
                ino_currency = trosak.amount_currency
                ukupni_trosak_ino = ukupni_trosak_ino + trosak.amount
                pdf.cell(24,4, f'{trosak.expenses_date.strftime("%d/%m/%Y")}', border=1, ln=False, align='C')
                pdf.cell(56,4, f'{trosak.expenses_type}', border=1, ln=False, align='L')
                pdf.cell(75,4, f'{trosak.description}', border=1, ln=False, align='L')
                pdf.cell(18,4, f'-', border=1, ln=False, align='C')
                pdf.cell(17,4, f'{trosak.amount} {trosak.amount_currency}', border=1, ln=True, align='R')


    ukupni_trosak = round(ukupni_trosak,2)
    ukupni_trosak_ino = round(ukupni_trosak_ino,2)

    pdf.cell(155, 4, f'Svega', border=1, ln=False, align='R')
    if troskovi != []:
        pdf.cell(18, 4, f'{ukupni_trosak} rsd', border=1, ln=False, align='R')
        pdf.cell(17, 4, f'{ukupni_trosak_ino} {ino_currency}', border=1, ln=True, align='R')
    else:
        pdf.cell(35, 4, f'', border=1, ln=True, align='R')
    pdf.cell(155, 4, f'Primljena akontacija', border=1, ln=False, align='R')
    if warrant.advance_payment_currency == 'rsd':
        pdf.cell(18, 4, f'{warrant.advance_payment} {warrant.advance_payment_currency}', border=1, ln=False, align='R')
        pdf.cell(17, 4, f'-', border=1, ln=True, align='C')
    else:
        pdf.cell(18, 4, f'-', border=1, ln=False, align='C')
        pdf.cell(17, 4, f'{warrant.advance_payment} {warrant.advance_payment_currency}', border=1, ln=True, align='R')


    saldo = round((float(warrant.daily_wage) * br_dnevnica - (warrant.advance_payment if warrant.advance_payment_currency == "rsd" else 0) + ukupni_trosak),2)
    saldo_ino = round((float(warrant.daily_wage_abroad) * br_dnevnica_ino - (warrant.advance_payment if warrant.advance_payment_currency != "rsd" else 0) + ukupni_trosak_ino),2)

    pdf.cell(155, 4, f'Ostalo za isplatu - uplatu', border=1, ln=False, align='R')
    pdf.cell(18, 4, f'{saldo} rsd', border=1, ln=False, align='R')
    pdf.cell(17, 4, f"{saldo_ino} {ino_currency}", border=1, ln=True, align='R')


    pdf.cell(0, 8, f'Prilog', border=1, ln=True, fill = True, align='C')
    pdf.multi_cell(0, 8, f'''U mestu {warrant.travelwarrant_company.company_city}, dana {warrant.start_datetime.strftime("%d/%m/%Y")}, {warrant.travelwarrant_user.name} {warrant.travelwarrant_user.surname}''', border=1, ln=True, align='C')
    pdf.multi_cell(0, 4, f'', ln=True, align='L')
    
    saldo = int(saldo)
    saldo_slovima = number_to_text(int(saldo))
    saldo_ino_slovima = number_to_text(int(saldo_ino))
    
    
    pdf.multi_cell(0, 4, f'''Potvrđujem da je putovanje izvršeno prema ovom nalogu i odobravam isplatu putnog računa od {saldo} ({saldo_slovima}) dinara {f'; {saldo_ino} ({saldo_ino_slovima}) {ino_currency}' if saldo_ino != 0 else ""} na teret {warrant.costs_pays}.
U mestu {warrant.travelwarrant_company.company_city}, dana {warrant.end_datetime.strftime("%d/%m/%Y")}.''', ln=True, align='L')
    pdf.multi_cell(0, 4, f'''

Blagajnik: _____________________________________          Podnosilac računa: _____________________________________''', ln=True, align='C')

    path = "putninalozi/static/pdf_forms/"
    file_name = replace_serbian_characters(f'{warrant_number} {company_name}-{name} {surname}.pdf')
    pdf.output(path + file_name)
    return file_name, text_form



def send_email(warrant, current_user, file_name):
    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice"]
    #dodaj if blok za različita slanja
    # ako je kreiran nalog: korisniku i nalogodavcu
    if warrant.status == 'kreiran':
        subject = f'Kreiran je putni nalog broj: {warrant.travel_warrant_number}'
        recipients = [warrant.travelwarrant_user.email, warrant.principal_user.email] #dodaj kod za nalogodavca!!!
        text_body = f'''{rod[2]},
Odobren je putni nalog {warrant.travel_warrant_number}.
Detaljije informacije o putnom nalogu mogu se videti u prilogu ili klikom na link:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

Pozdrav,
{current_user.name} {current_user.surname}
        '''
    # ako je završen nalog: adminu
    elif warrant.status == 'završen':
        subject = f'Završen je putni nalog broj: {warrant.travel_warrant_number}'
        recipients = [] #dodaj kod za admina kompanije za dati putni nalog!!!
        text_body = f'''Poštovani,
Završen je putni nalog {warrant.travel_warrant_number}. Klikom na donji link možete obračunati putni nalog:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

Pozdrav.'''
    # ako je obračunat nalog: blagajniku i korisniku
    elif warrant.status == 'obračunat':
        subject = f'Obračunat je putni nalog broj: {warrant.travel_warrant_number}'
        recipients = [warrant.travelwarrant_user.email] #dodaj kod za blagajnika
        text_body = f'''Poštovani,
Obračunat je putni nalog {warrant.travel_warrant_number}. Možete izvršiti uplatu dnevnica prema podacima iz priloga.

Pozdrav.'''
    # ako je storniran nalog: da li treba nekoga da obaveštava?
    msg = Message(subject,
                    sender='no_replay@putninalozi.online',
                    recipients=recipients)
    msg.body = text_body
    path = 'static/pdf_forms/'
    file_name = file_name
    print(path)
    print(file_name)
    print(path+file_name)
    with app.open_resource(path + file_name) as fp:
        msg.attach(path + file_name, 'application/pdf', fp.read())

    mail.send(msg)
