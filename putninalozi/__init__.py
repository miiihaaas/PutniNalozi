from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '0b0f805f651d04f909f539ec57f8a89c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from putninalozi.companys.routes import companys
from putninalozi.travel_warrants.routes import travel_warrants
from putninalozi.users.routes import users
from putninalozi.vehicles.routes import vehicles
from putninalozi.main.routes import main


app.register_blueprint(companys)
app.register_blueprint(travel_warrants)
app.register_blueprint(users)
app.register_blueprint(vehicles)
app.register_blueprint(main)
