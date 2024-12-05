from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# User registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        mobile_no = request.form['mobile_no']
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, password=hashed_password, email=email, mobile_no=mobile_no)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# User login route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('ecommerce.home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

# User profile route
@auth.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

# User logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Log the user out
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))