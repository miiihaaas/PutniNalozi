from flask import Blueprint
from flask import  render_template, url_for, flash, redirect, request, abort
from putninalozi import db, bcrypt, mail
from putninalozi.users.forms import RegistrationUserForm, LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm
from putninalozi.models import Company, User
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message


users = Blueprint('users', __name__)


@users.route("/user_list")
def user_list():
    users = User.query.all()
    return render_template('user_list.html', title='Users', users=users)


@users.route("/register_u", methods=['GET', 'POST'])
@login_required
def register_u():
    if current_user.is_authenticated and (current_user.authorization != 'c_admin' and current_user.authorization != 's_admin'):
        return redirect(url_for('main.home'))
    form = RegistrationUserForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if current_user.authorization == 'c_admin':
            user = User(email=form.email.data,
                        old_email=form.email.data,
                        password=hashed_password,
                        name=form.name.data,
                        surname=form.surname.data,
                        authorization=form.authorization.data,
                        company_id=Company.query.filter_by(companyname=current_user.user_company.companyname).first().id) #Company.query.filter_by(companyname=form.company_id.data).first().id) #int(current_user.company_id)) ##
        elif current_user.authorization == 's_admin':
            user = User(email=form.email.data,
                        password=hashed_password,
                        name=form.name.data,
                        surname=form.surname.data,
                        authorization=form.authorization.data,
                        company_id=Company.query.filter_by(companyname=form.company_id.data).first().id)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data} {form.surname.data}!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register_u.html', title='Register New User', form=form, legend='Add New User')




@users.route("/user/<int:user_id>", methods=['GET', 'POST'])
@login_required
def user_profile(user_id): #ovo je funkcija za editovanje user-a
    user = User.query.get_or_404(user_id)
    if current_user.authorization != 's_admin' and current_user.authorization != 'c_admin':
        if current_user.id == user.id:
            pass
        else:
            abort(403)
    form = UpdateUserForm()
    if form.validate_on_submit():
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.old_email = form.old_email.data

        if current_user.authorization != 'c_user':
            user.authorization = form.authorization.data
        if current_user.authorization == 's_admin':
            user.company_id = Company.query.filter_by(companyname=form.company_id.data).first().id


        db.session.commit()
        flash('Profile was updated', 'success')
        return redirect(url_for('users.user_list')) #vidi da li je bolje na neko drugo mesto da ga prebaci
    elif request.method == 'GET':
        form.name.data = user.name
        form.surname.data = user.surname
        form.email.data = user.email

        form.old_email.data = user.email
    return render_template('user.html', title="Edit User", user=user, form=form, legend='Edit User')



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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
            flash(f'Welcome back {user.name}!', 'success')
        else:
            flash(f'Username or Password are not valid!', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')


@users.route("/user/<int:user_id>/delete", methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    print(f'debug - {request.form.get("input_password")}')
    if not bcrypt.check_password_hash(current_user.password, request.form.get("input_password")):
        print('nije dobar password')
        abort(403)
    else:
        if current_user.authorization == 'c_user':
            abort(403)
        elif current_user.authorization == 'c_admin':
            if current_user.user_company.id != user.user_company.id:
                abort(403)
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.username} has been deleted', 'success' )
            return redirect(url_for('users.user_list'))
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f'User {user.name} {user.surname} has been deleted', 'success' )
            return redirect(url_for('users.user_list'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset Request', sender='noreplay@putninalozi.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made.
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
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('users.login')) # ili samo 'login'
        return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
        if current_user.is_authenticated:
            return redirect(url_for('main.home'))
        user = User.verify_reset_token(token)
        if user is None:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('users.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash(f'Your password has been updated!', 'success')
            return redirect(url_for('users.login')) # ili samo 'login'

        return render_template('reset_token.html', title='Reset Password', form=form)
