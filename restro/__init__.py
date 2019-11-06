from flask import Flask
from flask_sqlalchemy import SQLAlchemy





app=Flask(__name__)

app.config['SECRET_KEY']='67b0b4c317c234642ba164ff2aea68ec'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db=SQLAlchemy(app)

from restro import routes