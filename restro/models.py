from restro import db,login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    #bookings=db.relationship('Booking',backref='author',lazy=True)
    review=db.relationship('Review',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone_number}','{self.address}')"
"""
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, primary_key=True)
    total_seats = db.Column(db.Integer, nullable=False)
    table_status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.total_seats}', '{self.table_status}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    b_email=db.Column(db.String(120),nullable=False)
    b_phone=db.Column(db.String(10),nullable=False)
    b_registeration_time=db.Column(db.DateTime(),nullable=False)
    num_seats=db.Column(db.Integer,nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)


    def __repr__(self):
        return f"User('{self.b_email}', '{self.b_phone}','{self.b_registeration_time}','{self.num_seats}')"

"""

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.item_name}', '{self.date_posted}')"
