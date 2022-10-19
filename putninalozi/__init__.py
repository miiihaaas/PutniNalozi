import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '0b0f805f651d04f909f539ec57f8a89c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' #'mysql://scott:tiger@localhost/mydatabase'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://putninalozi_mihas:mihasmihasmihas@MariaDB/puntninalozi_app' #iz simketovog mejla sam dobio IP
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://putninalozi_mihas:mihasmihasmihas@localhost/puntninalozi_app' #localhost na sreveru??
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://putninalozi_mihas:mihasmihasmihas@putninalozi.online:3306/puntninalozi_app'

# sqlite:///site.db
# mysql://putninalozi_mihas:mihasmihasmihas@68.66.248.21/puntninalozi_app #iz simketovog mejla sam dobio IP
# mysql://putninalozi_mihas:mihasmihasmihas@localhost/puntninalozi_app #localhost na sreveru??
# mysql://putninalozi_mihas:mihasmihasmihas@putninalozi.online:2083/puntninalozi_app #localhost na sreveru??
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer -- za 2 step verification: https://support.google.com/accounts/answer/185833
mail = Mail(app)

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
