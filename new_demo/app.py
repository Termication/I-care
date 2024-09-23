from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret_key'
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
    school_name = db.Column(db.String(100), nullable=False)
    student_number = db.Column(db.String(50), nullable=False)
    
    # new 
    role = db.Column(db.String(10), nullable=False, default='student')  # either 'student' or 'doctor'
    # Relationships (if needed)
    doctor_profile = db.relationship('DoctorProfile', backref='user_profile', uselist=False)


 
# Review model  
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # doctor = db.relationship('Doctor', backref='reviews')
    user = db.relationship('User', backref='reviews')

# DoctorProfile model
class DoctorProfile(db.Model):
    __tablename__ = 'doctor_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    specialty = db.Column(db.String(150), nullable=False)
    practice_number = db.Column(db.String(50), nullable=False)
    
    # user = db.relationship('User', backref='doctor_profile', uselist=False)

"""
# Doctor model
class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    specialty = db.Column(db.String(150))
    contact = db.Column(db.String(150)) 
"""
    
# Chat model    
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor_profiles.id'), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='chats')
    doctor = db.relationship('DoctorProfile', backref='chats')

# Post model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    user = db.relationship('User', backref='posts')

# Comment model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post = db.relationship('Post', backref='comments')
    content = db.Column(db.String(500), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    post = db.relationship('Post', back_populates='comments')
    user = db.relationship('User', backref='comments')

# Like model
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    post = db.relationship('Post', backref='likes')
    user = db.relationship('User', backref='likes')

# Report model
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.String(255))

    post = db.relationship('Post', backref='reports')
    user = db.relationship('User', backref='reports')

# Create the database and seed the doctor data if the table is empty
with app.app_context(): 
    db.create_all()
    """if DoctorProfile.query.count() == 0:
        doctor_profile = [
            DoctorProfile(user_id=1, specialty="Psychologist"),
            DoctorProfile(user_id=2, specialty="Counselor"),
            DoctorProfile(user_id=3, specialty="Therapist"),
        ]
        db.session.add_all(doctor_profile)
        db.session.commit()"""

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
            if user.role == 'doctor':
                return redirect(url_for('dashboard'))
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
        role = request.form.get('role', 'student')  # Defaults to 'student'
        user_exists = User.query.filter_by(email=email).first()

        if user_exists:
            flash('Email already exists. Please log in.', 'warning')
            return redirect(url_for('login'))

        # Use pbkdf2:sha256 as the hash method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        if role == 'doctor':
            specialty = request.form['specialty']
            doctor_profile = DoctorProfile(user_id=new_user.id, specialty=specialty)
            db.session.add(doctor_profile)
            db.session.commit()
        
        flash('Sign-Up successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/reviews/<int:doctor_id>/add', methods=['POST'])
@login_required
def add_review(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    rating = int(request.form.get('rating'))
    comment = request.form.get('comment')

    if rating < 1 or rating > 5:
        flash('Rating must be between 1 and 5', 'danger')
        return redirect(url_for('show_reviews', doctor_id=doctor_id))

    new_review = Review(
        doctor_id=doctor_id,
        user_id=current_user.id,
        rating=rating,
        comment=comment
    )
    
    db.session.add(new_review)
    db.session.commit()
    flash('Your review has been added!', 'success')
    return redirect(url_for('show_reviews', doctor_id=doctor_id))


# Dashboard route (protected route)
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'doctor':
        # Fetch the doctor's profile and reviews if the current user is a doctor
        doctor_profile = current_user.doctor_profile
        reviews = Review.query.filter_by(doctor_id=doctor_profile.id).all()
        return render_template('dashboard.html', doctor_profile=doctor_profile, reviews=reviews, is_doctor=True)
    else:
        # Fetch all doctors for students and show recommendations and recent posts
        doctors = DoctorProfile.query.join(User).all()
        recommendations = get_recommendations(current_user)
        recent_posts = Post.query.order_by(Post.date_posted.desc()).limit(5).all()
        return render_template('dashboard.html', doctors=doctors, recommendations=recommendations, recent_posts=recent_posts, is_doctor=False)

"""
@app.route('/doctor_dashboard')
@login_required
def doctor_dashboard():
    doctor_profile = current_user.doctor_profile
    if not doctor_profile:
        flash('Doctor profile not found. Please create a profile.', 'warning')
        return redirect(url_for('dashboard'))  # Redirect to general dashboard if no profile

    # Fetch additional data
    reviews = Review.query.filter_by(doctor_id=doctor_profile.id).all()
    return render_template('doctor_dashboard.html', doctor_profile=doctor_profile, reviews=reviews)
"""
# Recommendation logic (can be expanded)
def get_recommendations(user):
    return DoctorProfile.query.limit(2).all()

@app.route('/chat/request/<int:doctor_id>', methods=['POST'])
@login_required
def request_chat(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    return redirect(url_for('chat', doctor_id=doctor_id))

@app.route('/chat/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def chat(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    
    if request.method == 'POST':
        message = request.form.get('message')
        if message:
            new_message = Chat(user_id=current_user.id, doctor_id=doctor_id, message=message)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent!', 'success')    
    # Fetch chat messages between current user and the doctor
    messages = Chat.query.filter_by(user_id=current_user.id, doctor_id=doctor_id).order_by(Chat.timestamp).all()
    return render_template('chat.html', doctor=doctor, messages=messages)

# Route to display all posts
@app.route('/community', methods=['GET', 'POST'])
@login_required
def community():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        if title and content:
            new_post = Post(title=title, content=content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('community'))
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('community.html', posts=posts)

# Route to view a single post and its comments
@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        content = request.form.get('comment')
        if content:
            new_comment = Comment(content=content, user_id=current_user.id, post_id=post.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added successfully!', 'success')
            return redirect(url_for('view_post', post_id=post_id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('view_post.html', post=post, comments=comments)

# Route to delete a post
@app.route('/post/delete/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('community'))

# Route to like a post
@app.route('/post/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        flash('Like removed', 'info')
    else:
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        flash('Post liked!', 'success')
    
    db.session.commit()
    return redirect(url_for('view_post', post_id=post_id))

# Route to report a post
@app.route('/post/report/<int:post_id>', methods=['POST'])
@login_required
def report_post(post_id):
    post = Post.query.get_or_404(post_id)
    reason = request.form.get('reason')

    new_report = Report(user_id=current_user.id, post_id=post_id, reason=reason)
    db.session.add(new_report)
    db.session.commit()
    flash('Post reported', 'warning')
    
    return redirect(url_for('view_post', post_id=post_id))


@app.route('/api/reviews/<int:doctor_id>', methods=['GET'])
def get_reviews(doctor_id):
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    return {
        "reviews": [
            {"user": review.user.name, "rating": review.rating, "comment": review.comment}
            for review in reviews
        ]
    }
    
@app.route('/reviews/<int:doctor_id>', methods=['GET'])
def show_reviews(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    reviews = Review.query.filter_by(doctor_id=doctor_id).all()
    return render_template('reviews.html', doctor=doctor, reviews=reviews)

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

