from fpdf import FPDF
from flask import url_for
from flask_mail import Message
from putninalozi import app, mail


def create_pdf_form(warrant):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('times','B', 16)

    string = warrant.travelwarrant_user.surname
    print(string)
    print(warrant.travelwarrant_company.company_logo)

    pdf.cell(0, 30, f'Sluzbeni Put - #{warrant.travel_warrant_id}', ln=True, align='C')
    pdf.set_font('times','', 12)
    pdf.cell(0, 10, f'Zaposleni: {warrant.travelwarrant_user.name} ', ln=True)
    pdf.cell(0, 10, f'Sa zadatkom: {warrant.with_task}', ln=True)
    pdf.cell(0, 10, f'Relacija: {warrant.relation}', ln=True)
    pdf.cell(0, 10, f'Datum: {warrant.start_datetime} - {warrant.end_datetime}', ln=True)
    pdf.image("putninalozi/static/company_logos/" + warrant.travelwarrant_company.company_logo)

    path = "putninalozi/static/pdf_forms"
    file_name = f'/{warrant.travel_warrant_id}-{warrant.travelwarrant_company.companyname}-{warrant.travelwarrant_user.name} {warrant.travelwarrant_user.surname}.pdf'
    pdf.output(path + file_name)


def send_email(warrant, current_user):
    msg = Message(f'Kreiran je putni nalog broj: {warrant.travel_warrant_id}',
                    sender=current_user.email, #ovo ipak ne radi - šalje sa miiihaaas@gmail.com
                    recipients=[warrant.travelwarrant_user.email])
    msg.body = f'''{warrant.travelwarrant_user.name},
Odobren je putni nalog: {warrant.travel_warrant_id}. Detaljije informacije o putnom nalogu možete videti u prilogu ili klikom na link:
{url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant.travel_warrant_id, _external=True)}

Pozdrav,
{current_user.name} {current_user.surname}
    '''

    with app.open_resource("29-METALAC AD-Marko Rajčević.pdf") as fp: #provali kako da se postavi path na /static/pdf_forms
        msg.attach("29-METALAC AD-Marko Rajčević.pdf", "application/pdf", fp.read())

    mail.send(msg)
    pass
