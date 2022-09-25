from fpdf import FPDF
from flask import url_for
from flask_mail import Message
from putninalozi import app, mail
import datetime


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


def create_pdf_form(warrant):
    ################################ tutorial links: ################################
    # https://www.youtube.com/watch?v=q70xzDG6nls&ab_channel=ChartExplorers
    # https://www.youtube.com/watch?v=JhQVD7Y1bsA&t=400s&ab_channel=ChartExplorers
    # https://www.youtube.com/watch?v=FcrW-ESdY-A&t=1s&ab_channel=ChartExplorers
    # https://www.youtube.com/watch?v=K917aOsfnDc&ab_channel=ChartExplorers
    #################################################################################
    # https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
    # https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
    # https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html
    # https://pyfpdf.readthedocs.io/en/latest/Tutorial/index.html

    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice"]

    warrant_id = warrant.travel_warrant_id
    name = replace_serbian_characters(warrant.travelwarrant_user.name)
    surname = replace_serbian_characters(warrant.travelwarrant_user.surname)
    workplace = replace_serbian_characters(warrant.travelwarrant_user.workplace)
    with_task = replace_serbian_characters(warrant.with_task)
    relation = replace_serbian_characters(warrant.relation)
    abroad_contry = replace_serbian_characters(warrant.abroad_contry)
    costs_pays = replace_serbian_characters(warrant.costs_pays)
    start_datetime = warrant.start_datetime.strftime('%d.%m.%Y')
    end_datetime = warrant.end_datetime.strftime('%d.%m.%Y')


    #za footer
    company_logo = "putninalozi/static/company_logos/" + warrant.travelwarrant_company.company_logo
    company_name = warrant.travelwarrant_company.companyname
    company_address = replace_serbian_characters(warrant.travelwarrant_company.company_address) + f" {warrant.travelwarrant_company.company_address_number}"
    company_zip_code = warrant.travelwarrant_company.company_zip_code
    company_city = replace_serbian_characters(warrant.travelwarrant_company.company_city)
    company_state = replace_serbian_characters(warrant.travelwarrant_company.company_state)
    company_pib = warrant.travelwarrant_company.company_pib
    company_mb = warrant.travelwarrant_company.company_mb
    company_phone = warrant.travelwarrant_company.company_phone
    company_mail = warrant.travelwarrant_company.company_mail
    company_site = warrant.travelwarrant_company.company_site

    text_form = f'''{rod[0]} {name} {surname} {rod[1]} na poslove radnog mesta {workplace} upućuje se na službeni put dana {start_datetime} u {relation} {f'({abroad_contry})'if abroad_contry !="" else ""} sa zadatkom: {with_task}

Na službenom putu koristi prevozno sredstvo registarske tablice: {warrant.travelwarrant_vehicle.vehicle_registration}{warrant.personal_registration}

Dnevnica za ovo služebno putovanje pripada u iznosu od: {warrant.daily_wage} {warrant.daily_wage_currency}

Na službenom putu će se zadržati najdalje do {end_datetime},a u roku od 48h po povratku sa službenog puta i dolask na posao, podnešće pismeni izveštaj o obavljenom službenom poslu. Račun o učinjenim putnim troškovima podneti u roku od tri dana

Putni troškovi padaju na teret: {costs_pays}

{f'Odobravam isplatu akontacije u iznosu od: {warrant.advance_payment} {warrant.advance_payment_currency}' if warrant.advance_payment > 0 else ""}

Nalogodavac: {warrant.travelwarrant_company.CEO}
'''

    text_form = replace_serbian_characters(text_form)

    class PDF(FPDF):
        def header(self):
            # Logo
            self.image(company_logo, 1, 1, 25)
            # set font
            self.set_font('times', 'I', 8)
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
    pdf.set_font('times','B', 16)
    pdf.cell(0, 30, f'NALOG ZA SLUZBENO PUTOVANJE: #{warrant_id}', ln=True, align='C')

    pdf.set_font('times','', 12)
    pdf.multi_cell(0, 5, text_form, ln=True)

    path = "putninalozi/static/pdf_forms/"
    file_name = f'{warrant_id}-{company_name}-{name} {surname}.pdf'
    pdf.output(path + file_name)
    return file_name


def send_email(warrant, current_user, file_name):
    rod = []
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen", "Kolega"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena", "Koleginice"]

    msg = Message(f'Kreiran je putni nalog broj: {warrant.travel_warrant_id}',
                    sender=current_user.email, #ovo ipak ne radi - šalje sa miiihaaas@gmail.com
                    recipients=[warrant.travelwarrant_user.email])
    msg.body = f'''{rod[2]},
Odobren je putni nalog #{warrant.travel_warrant_id}.
Detaljije informacije o putnom nalogu mogu se videti u prilogu ili klikom na link:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

Pozdrav,
{current_user.name} {current_user.surname}
    '''
    path = 'D:\Mihas\Programming\Python\Projects\PutniNalozi\putninalozi\static\pdf_forms'
    file_name = '\\' + file_name
    with app.open_resource(path + file_name) as fp:
        msg.attach(path + file_name, 'application/pdf', fp.read())

    mail.send(msg)