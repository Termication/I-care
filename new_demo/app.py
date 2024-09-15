from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

# Doctor model
class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    specialty = db.Column(db.String(150))
    contact = db.Column(db.String(150))

# Create the database and seed the doctor data if the table is empty
with app.app_context():
    db.create_all()
    if Doctor.query.count() == 0:
        doctors = [
            Doctor(name="Dr. Alice Smith", specialty="Psychologist", contact="alice@healthcare.com"),
            Doctor(name="Dr. John Doe", specialty="Counselor", contact="john@healthcare.com"),
            Doctor(name="Dr. Mary Johnson", specialty="Therapist", contact="mary@healthcare.com"),
        ]
        db.session.add_all(doctors)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

# Route for Sign-Up page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Email already exists. Please log in.', 'warning')
            return redirect(url_for('login'))

        # Use pbkdf2:sha256 as the hash method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Sign-Up successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

# Dashboard route (protected route)
@app.route('/dashboard')
@login_required
def dashboard():
    doctors = Doctor.query.all()
    recommendations = get_recommendations(current_user)
    
    # Debug prints
    print("Doctors:", doctors)
    print("Recommendations:", recommendations)
    
    return render_template('dashboard.html', doctors=doctors, recommendations=recommendations)

# Recommendation logic (can be expanded)
def get_recommendations(user):
    return Doctor.query.limit(2).all()

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Homepage
@app.route('/')
def home():
    return "Welcome to the I CARE platform!"

if __name__ == '__main__':
    app.run(debug=True)
