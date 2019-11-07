from restro import db



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.phone_number}','{self.address}','{self.password}')"

class Table(db.Mode)
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, primary_key=True)
    total_seats = db.Column(db.Integer, nullable=False)
    table_status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"User('{self.total_seats}', '{self.table_status}')"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column()


    
