from flask import Flask,render_template,redirect,url_for,flash
from form_customer import RegistrationForm, LoginForm

app=Flask(__name__)

app.config['SECRET_KEY']='67b0b4c317c234642ba164ff2aea68ec'

@ app.route("/")
def first_page():
    return render_template("first_page.html")

@ app.route("/customer_home")
def customer_home():
    return render_template("layout.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register",methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account successfully created for {form.username.data}","success")
    return render_template("register.html" , form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

if __name__=='__main__':
    app.run(debug=True)