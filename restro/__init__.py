from flask import Flask


app=Flask(__name__)

app.config['SECRET_KEY']='67b0b4c317c234642ba164ff2aea68ec'

from restro import routes