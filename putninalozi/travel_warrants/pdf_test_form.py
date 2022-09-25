from fpdf import FPDF
from flask import url_for
from flask_mail import Message
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



rod=["Radnik", "raspoređen", "Kolega"]

warrant_id = 111
name = replace_serbian_characters("Nikola")
surname = replace_serbian_characters("Martinović")
workplace = replace_serbian_characters("Poslovođa")
with_task = replace_serbian_characters("poseta kupcu")
relation = replace_serbian_characters("Novi Sad")
abroad_contry = replace_serbian_characters("")
costs_pays = replace_serbian_characters("Helios Srbija")
start_datetime = datetime.date(2022, 9, 26).strftime('%d.%m.%Y')
end_datetime = datetime.date(2022, 9, 27).strftime('%d.%m.%Y')
# end_datetime = warrant.end_datetime.strftime('%d.%m.%Y')


#za footer
company_logo = "putninalozi/static/company_logos/" + "c35002f0b322d770.png"
company_name = replace_serbian_characters("Helios Srbija")
company_address = replace_serbian_characters("Radovana Grkovića 24")
company_zip_code = 32300
company_city = replace_serbian_characters("Gornji Milanovac")
company_state = replace_serbian_characters("Srbija")

text_form = f'''{rod[0]} {name} {surname} {rod[1]} na poslove radnog mesta {workplace} upućuje se na službeni put dana {start_datetime} u {relation} {abroad_contry} sa zadatkom: {with_task}

Na službenom putu koristi prevozno sredstvo registarske tablice: GM031TC

Dnevnica za ovo služebno putovanje pripada u iznosu od: 1000 rsd

Na službenom putu će se zadržati najdalje do {end_datetime},a u roku od 48h po povratku sa službenog puta i dolask na posao, podnešće pismeni izveštaj o obavljenom službenom poslu. Račun o učinjenim putnim troškovima podneti u roku od tri dana

Putni troškovi padaju na teret: {costs_pays}

{f'Odobravam isplatu akontacije u iznosu od: 200 e' if 200 > 0 else ""}
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
        self.cell(0, 3, f'                         PIB: {"1234567"}', ln=False, align='L')
        # web stranica
        self.cell(1, 3, f'                         web: {"www.nekisajt.com"}', ln=True, align='R')
        # adresa
        self.cell(50, 3, f'                         {company_address}', ln=False, align='L')
        # MB
        self.cell(0, 3, f'                         MB: {"123123"}', ln=False, align='L')
        # email
        self.cell(1, 3, f'                         email: {"neki@email.com"}', ln=True, align='R')
        # mesto
        self.cell(0, 3, f'                         {company_zip_code} {company_city}', ln=False, align='L')
        # telefon
        self.cell(1, 3, f'                         tel: {"+381 65 123 123"}', ln=True, align='R')
        # Država
        self.cell(8, 3, f'                         {company_state}', ln=True, align='L')
        # linija
        pdf.line(10, 30, 200, 30)

pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('times','B', 16)
pdf.cell(0, 30, f'NALOG ZA SLUZBENO PUTOVANJE: #{warrant_id}', ln=True, align='C')

pdf.set_font('times','', 12)
pdf.multi_cell(0, 5, text_form, ln=True)



path = "d:/Mihas/Programming/Python/Projects/PutniNalozi/putninalozi/static/pdf_forms/"
file_name = f'{warrant_id}-{company_name}-{name} {surname}.pdf'
pdf.output(path + file_name)
print(path + file_name)
