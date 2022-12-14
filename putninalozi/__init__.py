import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
#kod ispod treba da reši problem Internal Server Error - komunikacija sa serverom
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_pre_ping": True,
    "pool_recycle": 300,
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['FLASK_APP'] = 'run.py'
#'sqlite:///site.db' #'mysql://scott:tiger@localhost/mydatabase'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://putninalozi_mihas:mihasmihasmihas@MariaDB/putninalozi_app' #iz simketovog mejla sam dobio IP
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://putninalozi_mihas:mihasmihasmihas@localhost:3306/putninalozi_app' #ovo zapravo radi na serveru
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://putninalozi_mihas:mihasmihasmihas@putninalozi.online:3306/putninalozi_app'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER') #dodati u .env: 'mail.putninalozi.online'
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT') #dodati u .env: 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS') # https://www.youtube.com/watch?v=IolxqkL7cD8&ab_channel=CoreySchafer -- za 2 step verification: https://support.google.com/accounts/answer/185833
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
