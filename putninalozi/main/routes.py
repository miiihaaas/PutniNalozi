from flask import Blueprint
from flask import  render_template, flash, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    if not current_user.is_authenticated:
        flash('Da bi ste pristupili ovoj stranici treba da budete ulogovani.', 'danger')
        return redirect(url_for('users.login'))
    return render_template('home.html', title='Home')


@main.route("/about")
def about():
    return render_template('about.html', title='About')
