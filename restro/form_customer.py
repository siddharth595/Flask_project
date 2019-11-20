from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,FloatField,IntegerField,SelectField,DateTimeField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from restro.models import User
from restro.models import MAX_TABLE_CAPACITY
from datetime import datetime


class ReservationForm(FlaskForm):
    guest_name = StringField('guest_name', validators=[DataRequired()])
    guest_phone = StringField('guest_phone', validators=[DataRequired()])
    num_guests = SelectField('num_guests', coerce=int, choices = [(x, x) for x in range(1, MAX_TABLE_CAPACITY)])
    reservation_datetime = DateTimeField('reservation_datetime', default=datetime.now(),
                                         validators=[DataRequired()])

    submit = SubmitField('Sign Up')

class ShowReservationsOnDateForm(FlaskForm):
    reservation_date = DateField('reservation_date', default=datetime.now())

class AddTableForm(FlaskForm):
    table_capacity = SelectField('table_capacity', coerce=int, choices = [(x, x) for x in range(1, MAX_TABLE_CAPACITY)])

class RegistrationForm(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone_number = StringField('Mobile Number',
                           validators=[DataRequired(), Length(10)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    address = TextAreaField('Your address', validators=[DataRequired()])

    submit = SubmitField('Sign Up')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()


        if user:
            raise ValidationError('The above email is already registered.Please register with another one')


    def validate_phone_number(self,phone_number):
        user=User.query.filter_by(phone_number=phone_number.data).first()


        if user:
            raise ValidationError('The above mobile number is already registered.Please register with another one')




class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class New_Review(FlaskForm):
    item_name = StringField('Tagline or Complement',
                        validators=[DataRequired()])
    content = TextAreaField('Your Review', validators=[DataRequired()])
    
    submit = SubmitField('Submit Your Review')



class New_Review_food(FlaskForm):
    item_name_food = StringField('Name of food item',
                        validators=[DataRequired()])
    content_food = TextAreaField('Your Review', validators=[DataRequired()])
    rating_food= FloatField('Rating out of 5', validators=[DataRequired()])
    submit = SubmitField('Submit Your Review')