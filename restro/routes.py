from flask import render_template, url_for, flash, redirect, request
from restro import app, db, bcrypt
from restro.form_customer import RegistrationForm, LoginForm,New_Review,New_Review_food
from restro.models import User, Review,Review_food
from flask_login import login_user, current_user, logout_user, login_required



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