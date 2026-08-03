from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from models import User

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('register'))

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Save new user to database
        new_user = User(name=name, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# Dashboard - redirects based on role

@app.route('/dashboard')
@login_required
def dashboard():
    role = current_user.role
    if role == 'Student':
        return redirect(url_for('student_dashboard'))
    elif role == 'Head of Family':
        return redirect(url_for('family_dashboard'))
    elif role == 'Daily Wager':
        return redirect(url_for('dailywager_dashboard'))
    elif role == 'Salaried Employee':
        return redirect(url_for('salaried_dashboard'))
    elif role == 'Business Owner':
        return redirect(url_for('business_dashboard'))

# Student Dashboard
@app.route('/dashboard/student')
@login_required
def student_dashboard():
    return render_template('dashboard.html', user=current_user)

# Family Dashboard
@app.route('/dashboard/family')
@login_required
def family_dashboard():
    return render_template('dashboard.html', user=current_user)

# Daily Wager Dashboard
@app.route('/dashboard/daily-wager')
@login_required
def dailywager_dashboard():
    return render_template('dashboard.html', user=current_user)

# Salaried Dashboard
@app.route('/dashboard/salaried')
@login_required
def salaried_dashboard():
    return render_template('dashboard.html', user=current_user)

# Business Dashboard
@app.route('/dashboard/business')
@login_required
def business_dashboard():
    return render_template('dashboard.html', user=current_user)