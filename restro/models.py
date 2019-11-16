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
    review=db.relationship('Review',backref='author',lazy=True)
    review_food=db.relationship('Review_food',backref='author',lazy=True)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone_number}','{self.address}')"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.item_name}', '{self.date_posted}')"



class Review_food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name_food = db.Column(db.String(100), nullable=False)
    date_posted_food = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content_food = db.Column(db.Text, nullable=False)
    rating_food =db.Column(db.Integer,nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.item_name_food}', '{self.date_posted_food}','{self.rating_food}')"
