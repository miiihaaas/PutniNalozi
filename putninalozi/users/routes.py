from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from putninalozi import db, bcrypt, mail
from putninalozi.users.forms import RegistrationUserForm, LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm
from putninalozi.models import Company, User, Vehicle, TravelWarrant
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from wtforms.validators import ValidationError


users = Blueprint('users', __name__)


@users.route("/user_list")
def user_list():
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    users = User.query.all()
    return render_template('user_list.html', title='Korisnici', legend='Korisnici', users=users)


@users.route("/register_u", methods=['GET', 'POST'])
# @login_required
def register_u():
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.is_authenticated and (current_user.authorization not in ['c_admin', 's_admin', 'c_functionary', 'c_founder']):
        flash('Nemate autorizaciju da posetite ovu stranicu.', 'danger')
        return redirect(url_for('main.home'))
    form = RegistrationUserForm()
    form.reset()
    form.default_vehicle.choices = [(0, "----")] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if current_user.authorization in ['c_admin', 'c_functionary', 'c_founder']:
            user = User(email=form.email.data,
                        password=hashed_password,
                        name=form.name.data.title(),
                        surname=form.surname.data.title(),
                        gender=form.gender.data,
                        workplace=form.workplace.data,
                        authorization=form.authorization.data,
                        principal=form.principal.data,
                        company_id=Company.query.filter_by(companyname=current_user.user_company.companyname).first().id,
                        default_vehicle=form.default_vehicle.data) #Company.query.filter_by(companyname=form.company_id.data).first().id) #int(current_user.company_id)) ##
        elif current_user.authorization == 's_admin':
            user = User(email=form.email.data,
                        password=hashed_password,
                        name=form.name.data.title(),
                        surname=form.surname.data.title(),
                        gender=form.gender.data,
                        workplace=form.workplace.data,
                        authorization=form.authorization.data,
                        principal=form.principal.data,
                        company_id=Company.query.filter_by(companyname=form.company_id.data).first().id,
                        default_vehicle=form.default_vehicle.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Napravljen je korisnički nalog: {form.name.data} {form.surname.data}.', 'success')
        return redirect(url_for('users.user_list'))
    return render_template('register_u.html', title='Registracija novog korisnika', form=form, legend='Registracija novog korisnika')




@users.route("/user/<int:user_id>", methods=['GET', 'POST'])
# @login_required
def user_profile(user_id): #ovo je funkcija za editovanje user-a
    user = User.query.get_or_404(user_id)
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif current_user.authorization not in ['s_admin', 'c_admin', 'c_functionary', 'c_founder']:
        flash('Nemate ovlašćenje da pristupite ovoj stranici.', 'danger')
        return render_template('403.html')
    elif current_user.authorization == 's_admin':
        pass
    elif current_user.user_company.id != user.user_company.id:
        return render_template('403.html')

    form = UpdateUserForm()
    form.reset()
    form.default_vehicle.choices = [(0, "----------")] + [(v.id, v.vehicle_type + "-" + v.vehicle_brand+" ("+v.vehicle_registration+")") for v in db.session.query(Vehicle.id,Vehicle.vehicle_type,Vehicle.vehicle_brand,Vehicle.vehicle_registration).filter_by(company_id=current_user.user_company.id).order_by('vehicle_type').all()]
    if form.validate_on_submit():
        user.name = form.name.data.title()
        user.surname = form.surname.data.title()
        if form.authorization.data not in ['c_member', 'c_founder']:
            user.workplace = form.workplace.data
        else:
            user.workplace = ""

        if user.email == form.email.data:
            user.email = form.email.data
        else:
            validate_email = User.query.filter_by(email=form.email.data).first()
            if validate_email:
                flash('Taj mejl je već postoji, izabeite drugači mejl', 'danger')
                return render_template('user.html', title="Uređivanje korisnčkih podataka", user=user, form=form, legend='Uređivanje korisnčkih podataka')
            else:
                user.email = form.email.data

        
        user.authorization = form.authorization.data
        user.principal = form.principal.data

        user.gender = form.gender.data

        if current_user.authorization == 's_admin':
            user.company_id = form.company_id.data
        else:
            user.company_id = user.company_id
        user.default_vehicle = form.default_vehicle.data

        db.session.commit()
        flash('Profil je ažuriran.', 'success')
        return redirect(url_for('users.user_list'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.surname.data = user.surname
        form.workplace.data = user.workplace
        form.email.data = user.email

        form.authorization.data = user.authorization
        form.principal.data = user.principal
        form.gender.choices = [(1, 'muški'),(2, 'ženski')]
        form.gender.data = user.gender

        form.company_id.choices = [(c.id, c.companyname) for c in db.session.query(Company.id,Company.companyname).order_by('companyname').all()]
        form.company_id.data = str(user.company_id)
        form.default_vehicle.data = str(user.default_vehicle)
    return render_template('user.html', title="Uređivanje korisnčkih podataka", user=user, form=form, legend='Uređivanje korisnčkih podataka')



@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Dobro došli, {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Mejl ili lozinka nisu odgovarajući.', 'danger')
    return render_template('login.html', title='Prijavljivanje', form=form, legend='Prijavljivanje')


@users.route("/logout")
def logout():
    logout_user()
    flash(f'Uspešno ste se odjavili iz softvera.', 'success')
    return redirect(url_for('users.login'))


@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    list_of_users_warrants = TravelWarrant.query.filter_by(user_id=user_id).all()
    if not current_user.is_authenticated:
        flash('Da biste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    elif not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('Pogrešna lozinka!')
        flash('Pogrešna lozinka!', 'danger')
        return render_template('403.html')
    else:
        if current_user.authorization not in ['c_admin', 's_admin', 'c_functionary', 'c_founder']:
            flash('Nemate ovlašćenje da brišete profile korisnika!', 'danger')
            return render_template('403.html')
        elif current_user.authorization in ['c_admin', 'c_functionary', 'c_founder']:
            if current_user.user_company.id != user.user_company.id:
                flash('Nemate ovlašćenje da brišete profile korisnika drugih kompanija!', 'danger')
                return render_template('403.html')
            if len(list_of_users_warrants):
                print(f'ima {len(list_of_users_warrants)} prutnih naloga, treba tagovati profil')
                user.authorization = 'c_deleted'
                db.session.commit()
                flash(f'Korisnički profil {user.name} {user.surname} je obrisan. Putni nalozi korisnika su ostali u bazi podataka.', 'success' )
                return redirect(url_for('users.user_list'))
            else:
                print('nema putnih naloga, može da se obriše profil')
                db.session.delete(user)
                db.session.commit()
                flash(f'Korisnički profil {user.name} {user.surname} je obrisan.', 'success' )
                return redirect(url_for('users.user_list'))
        else:
            if len(list_of_users_warrants):
                print(f'ima {len(list_of_users_warrants)} prutnih naloga, treba tagovati profil')
                user.authorization = 'c_deleted'
                db.session.commit()
                flash(f'Korisnički profil {user.name} {user.surname} je obrisan. Putni nalozi korisnika su ostali u bazi podataka.', 'success' )
                return redirect(url_for('users.user_list'))
            else:
                print('nema putnih naloga, može da se obriše profil')
                db.session.delete(user)
                db.session.commit()
                flash(f'Korisnički profil {user.name} {user.surname} je obrisan.', 'success' )
                return redirect(url_for('users.user_list'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Zahtev za resetovanje lozinke', sender='no_replay@putninalozi.online', recipients=[user.email])
    msg.body = f'''Da biste resetovali lozinku, kliknite na sledeći link:
{url_for('users.reset_token', token=token, _external=True)}

Ako Vi niste napavili ovaj zahtev, molim Vas ignorišite ovaj mejl i neće biti napravljene nikakve izmene na Vašem nalogu.
    '''
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        form = RequestResetForm()
        if form.validate_on_submit():
            user  = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('Mejl je poslat na Vašu adresu sa instrukcijama za resetovanje lozinke. ', 'info')
            return redirect(url_for('users.login'))
        return render_template('reset_request.html', title='Resetovanje lozinke', form=form, legend='Resetovanje lozinke')


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('Ovo je nevažeći ili istekli token.', 'warning')
            return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f'Vaša lozinka je ažurirana!', 'success')
            return redirect(url_for('users.login'))

        return render_template('reset_token.html', title='Resetovanje lozinke', form=form)

@users.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404