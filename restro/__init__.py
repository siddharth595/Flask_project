from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager




app=Flask(__name__)

app.config['SECRET_KEY']='67b0b4c317c234642ba164ff2aea68ec'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'




db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
from restro import routes