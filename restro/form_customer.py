from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,FloatField,IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from restro.models import User


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
    item_name = StringField('Name of item',
                        validators=[DataRequired()])
    content = TextAreaField('Your Review', validators=[DataRequired()])
    
    submit = SubmitField('Submit Your Review')



class New_Review_food(FlaskForm):
    item_name_food = StringField('Name of food item',
                        validators=[DataRequired()])
    content_food = TextAreaField('Your Review', validators=[DataRequired()])
    rating_food= IntegerField('Rating out of 5', validators=[DataRequired()])
    submit = SubmitField('Submit Your Review')