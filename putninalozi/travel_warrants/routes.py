from markupsafe import Markup
from flask import Blueprint, render_template, url_for, flash, redirect, abort, request, send_file
from putninalozi import db, bcrypt
from putninalozi.models import TravelWarrant, Company, User, Vehicle, TravelWarrantExpenses, Settings
from putninalozi.travel_warrants.forms import PreCreateTravelWarrantForm, CreateTravelWarrantForm, EditAdminTravelWarrantForm, EditUserTravelWarrantForm, TravelWarrantExpensesForm, EditTravelWarrantExpenses
from putninalozi.travel_warrants.pdf_form import create_pdf_form, update_pdf_form
from putninalozi.travel_warrants.functions import proracun_broja_dnevnica, send_email, update_warrant
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime, timedelta
from sqlalchemy import or_, not_


travel_warrants = Blueprint('travel_warrants', __name__)


@travel_warrants.route("/download/<string:file_name>")
def download_file(file_name):
    file_name = file_name.replace('%20', ' ')
    path = "static/pdf_forms/" + file_name
    return send_file(path, as_attachment=False)


@travel_warrants.route("/travel_warrant_list", methods=['GET', 'POST'])
def travel_warrant_list():
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    warrants = TravelWarrant.query.all()
    form = PreCreateTravelWarrantForm()
    # form.user_id.choices = [(0, '----------')] + [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).filter(User.authorization != 'c_deleted').order_by('name').all()]

    unfiltered_authorizations = ['c_deleted', 'o_cashier']
    form.user_id.choices = [(0, '----------')] + [(u.id, u.name+ " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).filter(not_(User.authorization.in_(unfiltered_authorizations))).order_by('name').all()]

    
    if form.validate_on_submit():
        korisnik_id = form.user_id.data
        datum = form.start_datetime.data
        return redirect(url_for('travel_warrants.register_tw',korisnik_id=korisnik_id, datum=datum))
    return render_template('travel_warrant_list.html', title='Putni nalozi', warrants=warrants, form=form, legend='Putni nalozi')


@travel_warrants.route("/register_tw/<int:korisnik_id>/<datum>", methods=['GET', 'POST'])
def register_tw(korisnik_id, datum):
    premium = Company.query.filter_by(id=current_user.user_company.id).first()
    number_of_warrants = TravelWarrant.query.filter_by(company_id=current_user.company_id).count()
    now = datetime.now().date()
    expiration_date = premium.premium_expiration_date.date()
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif number_of_warrants >= premium.premium_warrants:
        flash(f'Dostigi ste limit od {premium.premium_warrants} putnih naloga.', 'danger')
        return render_template('premium.html', title='Premium licenca', legend='Premium licenca')
    elif now >= expiration_date:
        flash(f'Vaša licenca je istekla {premium.premium_expiration_date}.', 'danger')
        return render_template('premium.html', title='Premium licenca', legend='Premium licenca')

    if current_user.authorization in ['c_admin', 's_admin', 'c_functionary', 'c_founder', 'c_cashier', 'o_cashier']:
        user_list = [(u.id, u.name + " " + u.surname) for u in db.session.query(User.id,User.name,User.surname).filter_by(company_id=current_user.user_company.id).order_by('name').all()]
        print(user_list)
        vehicle_company_list = [('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='company').order_by('vehicle_type').all()]
        vehicle_personal_list = [('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='private').order_by('vehicle_type').all()]
        datum = datum.replace('%20', ' ') #na sevreu zimeđu datuma i vremena se nalazi '%20' zbog toga ima ovaj replace


        print(f'{korisnik_id=}, {datum=}')
        datum = datetime.strptime(datum, '%Y-%m-%d %H:%M:%S') #'2022-09-27 15:02:00'
        end_datum = datum + timedelta(days=30) #'2022-10-27 15:02:00'

        drivers = [('', '----------')] + [(tw.travel_warrant_number, tw.travel_warrant_number + " => " + tw.travelwarrant_user.name + " " + tw.travelwarrant_user.surname + " - " + tw.travelwarrant_vehicle.vehicle_registration)
                                                for tw in TravelWarrant.query.filter(TravelWarrant.company_id==current_user.user_company.id,
                                                                                    TravelWarrant.vehicle_id!='').filter(TravelWarrant.start_datetime.between(
                                                                                                                    datum.replace(hour=0, minute=0, second=0, microsecond=0),
                                                                                                                    datum.replace(hour=23, minute=59, second=59, microsecond=9))).all()] + [(tw.travel_warrant_number, tw.travel_warrant_number + " => " + tw.travelwarrant_user.name + " " + tw.travelwarrant_user.surname + " - " + tw.travelwarrant_personal.vehicle_registration)
                                                for tw in TravelWarrant.query.filter(TravelWarrant.company_id==current_user.user_company.id,
                                                                                    TravelWarrant.personal_vehicle_id!='').filter(TravelWarrant.start_datetime.between(
                                                                                                                    datum.replace(hour=0, minute=0, second=0, microsecond=0),
                                                                                                                    datum.replace(hour=23, minute=59, second=59, microsecond=9))).all()]
        print(drivers)
        
        principal_list = [(principal.id, principal.name + " " + principal.surname) for principal in User.query.filter_by(company_id=current_user.company_id).filter_by(principal=True).filter(User.authorization != "c_deleted").all()]
        cashier_list = [(cashier.id, cashier.name + " " + cashier.surname) for cashier in User.query.filter_by(company_id=current_user.company_id).filter(or_(User.authorization == 'c_cashier', User.authorization == 'o_cashier')).all()]
        
        ime_prezime = User.query.filter_by(id=korisnik_id).first().name + " " + User.query.filter_by(id=korisnik_id).first().surname
        print(ime_prezime)
        brojac = max([0] + [int(b.travel_warrant_number[-2:]) for b in TravelWarrant.query.filter_by(company_id=current_user.user_company.id).filter(TravelWarrant.start_datetime.between(
                                                                                                            datum.replace(hour=0, minute=0, second=0, microsecond=0),
                                                                                                            datum.replace(hour=23, minute=59, second=59, microsecond=9))).all()])
        # return f'{max_brojac=}'
        if brojac + 1 < 10:
            brojac = '-0' + str(brojac + 1)
        else:
            brojac = '-' + str(brojac + 1)

        print(f'{korisnik_id=}, {datum=}, {brojac=}')
        podrazumevano_vozilo = User.query.filter_by(id=korisnik_id).first().default_vehicle
        print(f'{podrazumevano_vozilo=}')


        form = CreateTravelWarrantForm()
        form.reset()
        global_settings = Settings.query.filter_by(company_id=current_user.user_company.id).first()
        form.company_id.choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).all()]
        # form.user_id.choices = user_list
        # form.user_id.data = str(korisnik_id)
        form.vehicle_id.choices = vehicle_company_list
        form.personal_vehicle_id.choices = vehicle_personal_list
        form.together_with.choices = drivers
        form.principal_id.choices = principal_list
        form.cashier_id.choices = cashier_list
        if request.method == 'GET':
            form.vehicle_id.data  = str(podrazumevano_vozilo)
            form.personal_vehicle_id.data  = str(podrazumevano_vozilo)
            form.costs_pays.data = 'poslodavca'
            form.daily_wage.data = global_settings.daily_wage_domestic
            form.daily_wage_currency.data = global_settings.default_currency
            form.daily_wage_abroad.data = global_settings.daily_wage_abroad
            form.advance_payment_currency.data = global_settings.default_currency
            if form.advance_payment.data == None:
                form.advance_payment.data = 0
        # form.start_datetime.data = datum
    else:
        flash('Nemate autorizaciju da kreirate putne naloge.', 'warning')
        return redirect(url_for('travel_warrants.travel_warrant_list'))

    if form.validate_on_submit():
        warrant_data = {
            'user_id': korisnik_id,
            'with_task': form.with_task.data,
            'company_id': User.query.filter_by(id=korisnik_id).first().user_company.id,
            'abroad': form.abroad.data,
            'abroad_contry': form.abroad_contry.data.upper(),
            'relation': form.relation.data.title(),
            'start_datetime': datum,
            'end_datetime': form.end_datetime.data,
            'vehicle_id': None,
            'together_with': form.together_with.data,
            'personal_vehicle_id': None,
            'other': "",
            'advance_payment': form.advance_payment.data,
            'advance_payment_currency': form.advance_payment_currency.data,
            'daily_wage': form.daily_wage.data,
            'daily_wage_currency': form.daily_wage_currency.data,
            'daily_wage_abroad': form.daily_wage_abroad.data,
            'daily_wage_abroad_currency': form.daily_wage_abroad_currency.data,
            'costs_pays': form.costs_pays.data,
            'principal_id': form.principal_id.data,
            'cashier_id': form.cashier_id.data,
            'admin_id': current_user.id,
            'status': 'kreiran',
            'travel_warrant_number': datum.strftime('%Y%m%d') + brojac,
            'file_name': "",
            'text_form': "",
            'expenses': [],
        }
        if form.together_with.data != '':
            warrant_data['together_with'] = form.together_with.data
        elif form.personal_vehicle_id.data != "":
            warrant_data['personal_vehicle_id'] = form.personal_vehicle_id.data
        elif form.other.data != "":
            warrant_data['other'] = form.other.data
        elif form.vehicle_id.data == "":
            flash('Morate da odaberete jedan od načina prevoza klikom na dugme "Nazad".', 'danger')
            return render_template('403.html')
        else:
            warrant_data['vehicle_id'] = form.vehicle_id.data
            
        warrant = TravelWarrant(**warrant_data)
        db.session.add(warrant)
        db.session.commit()

        if warrant.abroad:
            br_casova = form.end_datetime.data - datum
            br_casova = br_casova.total_seconds() / 3600
            br_casova_ino = 0                                                           #! vreme provedeno u inostranstvu
            br_casova_start = 0                                                         #! vreme provedeno u zemlji pre izlaska iz zemlje
            br_casova_end = 0                                                           #! vreme provedeno u zemlji po povratku iz inostranstva
            br_dnevnica_start = 0
            br_dnevnica_end = 0
            br_dnevnica_ino = 0
            br_dnevnica = proracun_broja_dnevnica(br_casova)
        else:
            br_casova = form.end_datetime.data - datum
            br_casova = br_casova.total_seconds() / 3600  
            br_casova_ino = 0
            br_casova_start = 0
            br_casova_end = 0
            br_dnevnica = proracun_broja_dnevnica(br_casova)
            br_dnevnica_start = 0
            br_dnevnica_end = 0
            br_dnevnica_ino = 0
        print(f'{br_casova=} {br_casova_ino=} {br_dnevnica=} {br_dnevnica_ino=} ')

        file_name, text_form = create_pdf_form(warrant, br_casova, br_casova_ino, br_casova_start, br_casova_end, br_dnevnica, br_dnevnica_start, br_dnevnica_end, br_dnevnica_ino)
        warrant.file_name = file_name
        # warrant.text_form = Markup(text_form.replace('\n', '<br>')) #! menja \n u <br> element, a Markup omogućava da se <br> vidi kao element a ne kao string, u html filu treba dodati nastavak "| save" -> {{ warrant.text_form | safe }}
        warrant.text_form = text_form
        db.session.commit()
        print(text_form)
        print(file_name)

        print(f'{warrant.end_datetime=},{warrant.start_datetime=}')


        flash(f'Putni nalog broj: {warrant.travel_warrant_number} je uspešno kreiran.', 'success')
        if global_settings.send_email_kreiran or global_settings.send_email_kreiran_principal:
            send_email(warrant, current_user, warrant.file_name, global_settings)
            if global_settings.send_email_kreiran and global_settings.send_email_kreiran_principal:
                flash(f'{warrant.travelwarrant_user.name} i {warrant.principal_user.name} su dobili mejl sa detaljima putnog naloga.', 'success')
            elif global_settings.send_email_kreiran:
                flash(f'{warrant.travelwarrant_user.name} je {"dobio" if warrant.travelwarrant_user.gender == "1" else "dobila"} mejl sa detaljima putnog naloga.', 'success')
            elif global_settings.send_email_kreiran_principal:
                flash(f'{warrant.principal_user.name} je {"dobio" if warrant.principal_user.gender == "1" else "dobila"} mejl sa detaljima putnog naloga.', 'success')
        return redirect(url_for('travel_warrants.travel_warrant_list'))

    return render_template('register_tw.html', title='Kreiranje putnog naloga',
                            legend='Kreiranje putnog naloga',
                            form=form, ime_prezime=ime_prezime, datum=datum, end_datum=end_datum)


@travel_warrants.route("/travel_warrant/<int:warrant_id>", methods=['GET', 'POST'])
def travel_warrant_profile(warrant_id):
    rod = []
    troskovi = TravelWarrantExpenses.query.filter_by(travelwarrant_id = warrant_id).all()
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if warrant.travelwarrant_user.gender == "1":
        rod=["Radnik", "raspoređen"]
    elif warrant.travelwarrant_user.gender == "2":
        rod=["Radnica", "raspoređena"]
    vehicle_company_list = [('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='company').order_by('vehicle_type').all()]
    vehicle_personal_list = [('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='private').order_by('vehicle_type').all()]
    print(f'{vehicle_company_list=}')
    print(f'{vehicle_personal_list=}')
    drivers = [('', '----------')] + [(tw.travel_warrant_number, tw.travel_warrant_number + " => " + tw.travelwarrant_user.name + " " + tw.travelwarrant_user.surname)
                                                    for tw in TravelWarrant.query.filter(TravelWarrant.company_id==current_user.user_company.id,
                                                                                        TravelWarrant.vehicle_id!='').filter(TravelWarrant.start_datetime.between(
                                                                                                                        warrant.start_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
                                                                                                                        warrant.start_datetime.replace(hour=23, minute=59, second=59, microsecond=9))).all()] + [(tw.travel_warrant_number, tw.travel_warrant_number + " => " + tw.travelwarrant_user.name + " " + tw.travelwarrant_user.surname)
                                                    for tw in TravelWarrant.query.filter(TravelWarrant.company_id==current_user.user_company.id,
                                                                                        TravelWarrant.personal_vehicle_id!='').filter(TravelWarrant.start_datetime.between(
                                                                                                                        warrant.start_datetime.replace(hour=0, minute=0, second=0, microsecond=0),
                                                                                                                        warrant.start_datetime.replace(hour=23, minute=59, second=59, microsecond=9))).all()]
    end_datum = warrant.start_datetime + timedelta(days=30)
    start_datetime_min = datetime(warrant.start_datetime.year, warrant.start_datetime.month, warrant.start_datetime.day, 0, 0, 0)
    start_datetime_max = datetime(warrant.start_datetime.year, warrant.start_datetime.month, warrant.start_datetime.day, 23, 59, 59)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization != 's_admin' and current_user.user_company.id != warrant.travelwarrant_company.id:
        flash('Nemate ovlašćenje da posetite ovu stranici.', 'danger')
        return render_template('403.html')
    elif current_user.authorization in ['c_user', 'c_member'] and current_user.id != warrant.travelwarrant_user.id:
        flash('Nemate ovlašćenje da posetite ovu stranici.', 'danger')
        return render_template('403.html')

    if current_user.authorization not in ['c_admin', 's_admin', 'c_functionary', 'c_founder', 'c_cashier', 'o_cashier']:
        if warrant.status == 'storniran' or warrant.status == 'obračunat':
            # warrant.text_form = Markup(text_form.replace('\n', '<br>')) #! menja \n u <br> element, a Markup omogućava da se <br> vidi kao element a ne kao string, u html filu treba dodati nastavak "| save" -> {{ warrant.text_form | safe }}
            return render_template('read_travel_warrant_user.html', title='Pregled putnog naloga', 
                                    warrant=warrant, legend='Pregled putnog naloga', 
                                    detalji=Markup(warrant.text_form.replace('\n', '<br>')), rod=rod, troskovi=troskovi)
        else:
            form = EditUserTravelWarrantForm()
            form.reset()
            form.together_with.choices = drivers
            global_settings = Settings.query.filter_by(company_id=current_user.user_company.id).first()
            form.vehicle_id.choices = vehicle_company_list
            form.personal_vehicle_id.choices = vehicle_personal_list
    else:
        form = EditAdminTravelWarrantForm()
        form.reset()
        form.together_with.choices = drivers
        global_settings = Settings.query.filter_by(company_id=current_user.user_company.id).first()
        form.vehicle_id.choices = vehicle_company_list
        form.personal_vehicle_id.choices = vehicle_personal_list

        form.principal_id.choices = [(principal.id, principal.name + " " + principal.surname) for principal in User.query.filter_by(company_id=current_user.company_id).filter_by(principal=True).filter(User.authorization != "c_deleted").all()]
        form.cashier_id.choices = [(cashier.id, cashier.name + " " + cashier.surname) for cashier in User.query.filter_by(company_id=current_user.company_id).filter(or_(User.authorization == 'c_cashier', User.authorization == 'o_cashier')).all()]
            
    if form.validate_on_submit():
        if form.together_with.data:
            warrant.vehicle_id=None
            update_warrant(warrant, form, global_settings, current_user, form.status.data)
            print('zajedno sa - c_user')
        elif form.personal_vehicle_id.data:
            warrant.vehicle_id=None
            warrant.together_with=""
            update_warrant(warrant, form, global_settings, current_user, form.status.data)
            print('licno vozilo - c_user')
        elif form.other.data:
            warrant.vehicle_id=None
            warrant.together_with=""
            warrant.personal_vehicle_id=None
            update_warrant(warrant, form, global_settings, current_user, form.status.data)
            print('drugo - c_user')
        elif form.vehicle_id.data:
            warrant.together_with=""
            warrant.personal_vehicle_id=None
            warrant.other=""
            update_warrant(warrant, form, global_settings, current_user, form.status.data)
        else:
            flash('Morate da odaberete jedan od načina prevoza klikom na dugme "Nazad".', 'danger')
            return render_template('403.html')
            ####################################################################################

        if warrant.abroad:
            br_casova = 0
            br_casova_ino = warrant.contry_return - warrant.contry_leaving
            br_casova_ino = br_casova_ino.total_seconds() / 3600                        #! vreme provedeno u inostranstvu
            br_casova_start = warrant.contry_leaving - form.start_datetime.data
            br_casova_start = br_casova_start.total_seconds() / 3600                    #! vreme provedeno u zemlji pre izlaska iz zemlje
            br_casova_end = form.end_datetime.data - warrant.contry_return
            br_casova_end = br_casova_end.total_seconds() / 3600                        #! vreme provedeno u zemlji po povratku iz inostranstva
            br_dnevnica_start = proracun_broja_dnevnica(br_casova_start)
            br_dnevnica_end = proracun_broja_dnevnica(br_casova_end)
            br_dnevnica_ino = proracun_broja_dnevnica(br_casova_ino)
            br_dnevnica = br_dnevnica_start + br_dnevnica_end
        else:
            br_casova = form.end_datetime.data - form.start_datetime.data
            br_casova = br_casova.total_seconds() / 3600  
            br_casova_ino = 0
            br_casova_start = 0
            br_casova_end = 0
            br_dnevnica = proracun_broja_dnevnica(br_casova)
            br_dnevnica_start = 0
            br_dnevnica_end = 0
            br_dnevnica_ino = 0
        print(f'{br_casova=} {br_casova_ino=} {br_dnevnica=} {br_dnevnica_ino=} ')

        file_name, text_form = update_pdf_form(warrant, br_casova, br_casova_ino, br_casova_start, br_casova_end, br_dnevnica, br_dnevnica_start, br_dnevnica_end, br_dnevnica_ino, troskovi)
        print(f'update naloga: {text_form=}')
        warrant.file_name = file_name
        # warrant.text_form = Markup(text_form.replace('\n', '<br>')) #! menja \n u <br> element, a Markup omogućava da se <br> vidi kao element a ne kao string, u html filu treba dodati nastavak "| save" -> {{ warrant.text_form | safe }}
        warrant.text_form = text_form
        print(f'{warrant.end_datetime=},{warrant.start_datetime=}')

        db.session.commit()
            
        ##########################################################################################

        flash(f'Putni nalog {warrant.travel_warrant_number} je ažuriran.', 'success')
        if request.form.get('dugme') == 'Dodajte trošak':
            return redirect(url_for('travel_warrants.add_expenses', warrant_id=warrant.travel_warrant_id))
        return redirect(url_for('travel_warrants.travel_warrant_list'))
    elif request.method == 'GET':
        form.with_task.data = warrant.with_task
        form.abroad.data = warrant.abroad
        form.abroad_contry.data = warrant.abroad_contry
        form.relation.data = warrant.relation
        form.start_datetime.data = warrant.start_datetime
        form.end_datetime.data = warrant.end_datetime
        form.contry_leaving.data = warrant.contry_leaving
        form.contry_return.data = warrant.contry_return
        form.vehicle_id.choices =[('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='company').order_by('vehicle_type').all()]
        form.vehicle_id.data = str(warrant.vehicle_id)
        form.together_with.data = warrant.together_with
        form.personal_vehicle_id.choices = [('', '----------')] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).filter_by(vehicle_ownership='private').order_by('vehicle_type').all()]
        form.personal_vehicle_id.data = str(warrant.personal_vehicle_id)
        form.other.data = warrant.other

        form.status.choices=[("kreiran", "kreiran"), ("završen", "završen")]
        form.status.data = str(warrant.status)

        # end_datum = warrant.start_datetime + timedelta(days=30)
        # start_datetime_min = datetime(warrant.start_datetime.year, warrant.start_datetime.month, warrant.start_datetime.day, 0, 0, 0)
        # start_datetime_max = datetime(warrant.start_datetime.year, warrant.start_datetime.month, warrant.start_datetime.day, 23, 59, 59)
        
        if current_user.authorization in ['c_admin', 's_admin', 'c_functionary', 'c_founder', 'c_cashier', 'o_cashier']:
            form.advance_payment.data = warrant.advance_payment
            form.advance_payment_currency.data = warrant.advance_payment_currency
            form.daily_wage.data = warrant.daily_wage
            form.daily_wage_currency.data = warrant.daily_wage_currency
            form.daily_wage_abroad.data = warrant.daily_wage_abroad
            form.daily_wage_abroad_currency.data = warrant.daily_wage_abroad_currency
            form.costs_pays.data = warrant.costs_pays
            form.principal_id.data = str(warrant.principal_id)
            form.cashier_id.data = str(warrant.cashier_id)
            
            form.status.choices=[("kreiran", "kreiran"), ("završen", "završen"), ("obračunat", "obračunat") , ("storniran", "storniran")]
            form.status.data = str(warrant.status)
            
    if current_user.authorization in ['c_admin', 's_admin', 'c_functionary', 'c_founder', 'c_cashier', 'o_cashier']:
        return render_template('travel_warrant.html', title='Uređivanje putnog naloga', warrant=warrant, 
                        legend='Uređivanje putnog naloga (pregled korisnika)', detalji=Markup(warrant.text_form.replace('\n', '<br>')), form=form, rod=rod, 
                        troskovi=troskovi, end_datum=end_datum, start_datetime_min=start_datetime_min, start_datetime_max=start_datetime_max)
    else:
        return render_template('travel_warrant_user.html', title='Uređivanje putnog naloga', warrant=warrant, 
                                legend='Uređivanje putnog naloga (pregled korisnika)', detalji=Markup(warrant.text_form.replace('\n', '<br>')), form=form, rod=rod, 
                                troskovi=troskovi, end_datum=end_datum, start_datetime_min=start_datetime_min, start_datetime_max=start_datetime_max)


@travel_warrants.route("/add_expenses/<int:warrant_id>", methods=['GET', 'POST'])
def add_expenses(warrant_id):
    troskovi = TravelWarrantExpenses.query.filter_by(travelwarrant_id = warrant_id).all()
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.user_company.id != warrant.company_id:
            return render_template('403.html')
    form = TravelWarrantExpensesForm()
    if form.validate_on_submit():
        expense = TravelWarrantExpenses(expenses_type = form.expenses_type.data,
                description = form.description.data,
                amount = form.amount.data,
                amount_currency = form.amount_currency.data,
                travelwarrant_id = warrant_id)
        db.session.add(expense)
        db.session.commit()
        flash(f'U putnom nalogu broj {warrant.travel_warrant_number} je dodat trošak - {expense.expenses_type}.', 'success')
        return redirect(url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant_id))


    print(troskovi)
    print(warrant)
    return render_template('expenses.html', form=form, legend='Dodavanje troškova:', warrant=warrant, troskovi=troskovi)


@travel_warrants.route("/expenses/<int:warrant_id>/<int:expenses_id>", methods=['GET', 'POST'])
def expenses_profile(warrant_id, expenses_id): #ovo je funkcija a editovnaje troškova
    expense = TravelWarrantExpenses.query.get_or_404(expenses_id)
    troskovi = TravelWarrantExpenses.query.filter_by(travelwarrant_id = warrant_id).all()
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.user_company.id != warrant.company_id:
            return render_template('403.html')
    form = EditTravelWarrantExpenses()
    form.reset()
    # form.expenses_type.choices=[('Troškovi amortizacije privatnog vozila', 'Troškovi amortizacije privatnog vozila'), ('Ostali troškovi na službenom putu', 'Ostali troškovi na službenom putu'), ('Parkiranje', 'Parkiranje'), ('Putarine', 'Putarine'), ('Troškovi noćenja', 'Troškovi noćenja'), ('Troškovi prevoza', 'Troškovi prevoza'), ('Troškovi smeštaja i ishrane', 'Troškovi smeštaja i ishrane')]
    if form.validate_on_submit():
        expense.expenses_type = form.expenses_type.data
        expense.description = form.description.data
        expense.amount = form.amount.data
        expense.amount_currency = form.amount_currency.data
        db.session.commit()
        flash(f'Uspešno je ažuriran trošak: {expense.expenses_type}.', 'success')
        return redirect(url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant_id))
    elif request.method == 'GET':
        form.expenses_type.data = str(expense.expenses_type)
        form.description.data = expense.description
        form.amount.data = expense.amount
        form.amount_currency.data = expense.amount_currency
    return render_template('expenses.html', form=form, legend='Uređivanje troška:', warrant=warrant, troskovi=troskovi, expense=expense)


@travel_warrants.route("/expenses/<int:warrant_id>/<int:expenses_id>/delete", methods=['GET', 'POST'])
# @login_required
def delete_expense(warrant_id, expenses_id):
    expense = TravelWarrantExpenses.query.get_or_404(expenses_id)
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    print(expense)
    print(warrant)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.user_company.id != warrant.company_id: #ako putni nalog nije iz kompanije trenutno ulogovanok korisnika
        flash('Nemate ovlašćenje da brišete troškove putnih naloga drugih kompanija', 'danger')
        return render_template('403.html')
    else:
        db.session.delete(expense)
        db.session.commit()
        flash(f'Trošak {expense.expenses_type} je obrisan.', 'success' )
        return redirect(url_for('travel_warrants.travel_warrant_profile', warrant_id=warrant_id))


@travel_warrants.route('/travel_warrant/<int:warrant_id>/delete', methods=['GET', 'POST'])
def delete_travel_warrant(warrant_id):
    warrant = TravelWarrant.query.get_or_404(warrant_id)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('Pogrešna lozinka!')
        flash('Pogrešna lozinka!', 'danger')
        return render_template('403.html')
    else:
        if current_user.authorization not in ['c_admin', 's_admin', 'c_functionary', 'c_founder']:
            flash('Nemate ovlašćenje da brišete putne naloge!', 'danger')
            return render_template('403.html')
        elif current_user.authorization not in ['c_admin', 'c_functionary', 'c_founder']:
            if current_user.user_company.id != warrant.company_id: #ako putni nalog nije iz kompanije trenutno ulogovanok korisnika
                flash('Nemate ovlašćenje da brišete putne naloge drugih kompanija', 'danger')
                return render_template('403.html')
            db.session.delete(warrant)
            db.session.commit()
            flash(f'Putni nalog: {warrant.travel_warrant_number} je obrisan.', 'success' )
            return redirect(url_for('travel_warrants.travel_warrant_list'))
        else:
            db.session.delete(warrant)
            db.session.commit()
            flash(f'Putni nalog: {warrant.travel_warrant_number} je obrisan.', 'success' )
            return redirect(url_for('travel_warrants.travel_warrant_list'))
        

@travel_warrants.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404