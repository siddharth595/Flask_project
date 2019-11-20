from flask import render_template, url_for, flash, redirect, request,session,g
from restro import app, db, bcrypt
from restro.form_customer import RegistrationForm, LoginForm,New_Review,New_Review_food
from restro.models import User, Review,Review_food
from flask_login import login_user, current_user, logout_user, login_required

from restro.form_customer import ReservationForm, ShowReservationsOnDateForm, AddTableForm
from restro.controller import create_reservation
from restro.models import Table, Reservation
import datetime

RESTAURANT_OPEN_TIME=16
RESTAURANT_CLOSE_TIME=22


@app.route("/")
def first_page():
    return render_template('first_page.html')


@app.route("/customer_home")
def customer_home():
    reviews=Review.query.all()
    return render_template('home.html',review=reviews)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer_home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data,phone_number=form.phone_number.data,address=form.address.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('customer_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            
            return  redirect(url_for('customer_home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('customer_home'))


@app.route("/write_review",methods=['GET', 'POST'])
@login_required
def write_review():
    form = New_Review()
    if form.validate_on_submit():
        flash(f'Thanks for your review',"success")
        review=Review(item_name=form.item_name.data,content=form.content.data,author=current_user)
        db.session.add(review)
        db.session.commit()

    return render_template('new_review.html',form=form)



@app.route("/write_review_food",methods=['GET', 'POST'])
@login_required
def write_review_food():
    form = New_Review_food()
    if form.validate_on_submit():
        flash(f'Thanks for your review',"success")
        review_food=Review_food(item_name_food=form.item_name_food.data,content_food=form.content_food.data,rating_food=form.rating_food.data, author=current_user)
        db.session.add(review_food)
        db.session.commit()

    return render_template('new_review_food.html',form=form)


    
@app.route("/show_food_review")
@login_required
def show_review():
    reviews=Review_food.query.all()
    return render_template('show_food_review.html',review=reviews)



@app.route("/menu_card")
def menu_card():
    return render_template('menu_card.html')



@app.route('/make_reservation', methods=['GET', 'POST'])
def make_reservation():
    form = ReservationForm()
    if form.validate_on_submit():
        if form.reservation_datetime.data < datetime.datetime.now():
            flash("You cannot book dates in the past","error")
            return redirect('/make_reservation')
        reservation_date = datetime.datetime.combine(form.reservation_datetime.data.date(), datetime.datetime.min.time())
        if form.reservation_datetime.data < reservation_date + datetime.timedelta(hours=RESTAURANT_OPEN_TIME) or \
        form.reservation_datetime.data > reservation_date + datetime.timedelta(hours=RESTAURANT_CLOSE_TIME):
            flash("The restaurant is closed at that hour!","error")
            return redirect('/make_reservation')
        reservation = create_reservation(form)
        if reservation:
            flash("Reservation created!")
            return redirect('/customer_home')
        else:
            flash("That time is taken!  Try another time","error")
            return redirect('/make_reservation')
    return render_template('make_reservation.html', title="Make Reservation", form=form)

@app.route('/show_tables', methods=['GET', 'POST'])
def show_tables():
    form = AddTableForm()

    if form.validate_on_submit():
        table = Table(capacity=int(form.table_capacity.data))
        db.session.add(table)
        db.session.commit()
        flash("Table created!","success")
        return redirect('/show_tables')

    tables = Table.query.all()
    return render_template('show_tables.html', title="Tables", tables=tables, form=form)

@app.route('/show_reservations', methods=['GET', 'POST'])
@app.route('/show_reservations/<reservation_date>', methods=['GET', 'POST'])
def show_reservations(reservation_date = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d")):
    form = ShowReservationsOnDateForm()
    if form.validate_on_submit():
        res_date = datetime.datetime.strftime(form.reservation_date.data, "%Y-%m-%d")
        return redirect('/show_reservations/' + res_date)
    res_date = datetime.datetime.strptime(reservation_date, "%Y-%m-%d")
    reservations = Reservation.query.filter(Reservation.reservation_time >= res_date,
                                            Reservation.reservation_time < res_date + datetime.timedelta(days=1)).all()
    total_slots = len(Table.query.all()) * (RESTAURANT_CLOSE_TIME - RESTAURANT_OPEN_TIME)
    util = (len(reservations) / float(total_slots)) * 100
    return render_template('show_reservations.html', title="Reservations", reservations=reservations, form=form, total_slots=total_slots, utilization=util)

@app.route('/admin')
def admin():
    return render_template('admin.html', title="Admin")

@app.context_processor
def utility_processor():
    def table_utilization(table):
        start_datetime = datetime.datetime.combine(datetime.datetime.date(datetime.datetime.now()), datetime.datetime.min.time())
        end_datetime = start_datetime + datetime.timedelta(days=1)
        num_reservations = len(Reservation.query.filter(Reservation.table==table, Reservation.reservation_time > start_datetime, Reservation.reservation_time < end_datetime).all())
        return (num_reservations / float(RESTAURANT_CLOSE_TIME - RESTAURANT_OPEN_TIME)) * 100

    return dict(table_utilization=table_utilization)