from restro import db


class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, primary=True)
    name=db.Column(db.String(30), nullable=False)
    email=db.Column(db.String(100), nullable=False,unique=True)
    address=db.Column(db.Text, nullable=False)
    password=db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.address}','{self.password}')"



class Table(db.Model):
    __tablename__='table' 
    id=db.Column(db.Integer, primary=True)
    number_seat=db.Column(db.Integer, nullable=False)
    email=db.Column(db.String(100), nullable=False,unique=True)
    address=db.Column(db.Text, nullable=False)
    password=db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return f"User('{self.name}','{self.email}','{self.address}','{self.password}')"
