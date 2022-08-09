from flask import Blueprint
from flask import  render_template, url_for, flash, redirect
from putninalozi import db
# from putninalozi.travel_warrants.forms import TravelWarrantForm
from putninalozi.models import TravelWarrant
from flask_login import login_user, login_required, logout_user, current_user


travel_warrants = Blueprint('travel_warrants', __name__)



@travel_warrants.route("/travel_warrant", methods=['GET', 'POST'])
def travel_warrant():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.home'))
    return render_template('travel_warrant.html', title='Travel Warrant')
