from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, bcrypt
from models import User, Expense, Budget
import datetime

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

# Helper — fetches dashboard data from MySQL
def get_dashboard_data(user_id):
    now = datetime.datetime.now()

    # Get this month's expenses
    expenses = Expense.query.filter_by(user_id=user_id).filter(
        db.extract('month', Expense.date) == now.month,
        db.extract('year', Expense.date) == now.year
    ).order_by(Expense.date.desc()).all()

    # Calculate total spent
    total_spent = sum(e.amount for e in expenses)

    # Find top category
    if expenses:
        category_totals = {}
        for e in expenses:
            category_totals[e.category] = category_totals.get(e.category, 0) + e.amount
        top_category = max(category_totals, key=category_totals.get)
    else:
        top_category = 'N/A'

    # Calculate budget remaining
    budgets = Budget.query.filter_by(user_id=user_id, month=now.month, year=now.year).all()
    total_budget = sum(b.monthly_limit for b in budgets)

    if total_budget > 0:
        budget_remaining = f'₹{total_budget - total_spent:,.2f}'
    else:
        budget_remaining = 'No budget set'

    return {
        'transactions': expenses,
        'total_spent': f'₹{total_spent:,.2f}',
        'transaction_count': len(expenses),
        'top_category': top_category,
        'budget_remaining': budget_remaining
    }

# Student Dashboard
@app.route('/dashboard/student')
@login_required
def student_dashboard():
    data = get_dashboard_data(current_user.id)
    return render_template('dashboard.html', user=current_user, **data)

# Family Dashboard
@app.route('/dashboard/family')
@login_required
def family_dashboard():
    data = get_dashboard_data(current_user.id)
    return render_template('dashboard.html', user=current_user, **data)

# Daily Wager Dashboard
@app.route('/dashboard/daily-wager')
@login_required
def dailywager_dashboard():
    data = get_dashboard_data(current_user.id)
    return render_template('dashboard.html', user=current_user, **data)

# Salaried Dashboard
@app.route('/dashboard/salaried')
@login_required
def salaried_dashboard():
    data = get_dashboard_data(current_user.id)
    return render_template('dashboard.html', user=current_user, **data)

# Business Dashboard
@app.route('/dashboard/business')
@login_required
def business_dashboard():
    data = get_dashboard_data(current_user.id)
    return render_template('dashboard.html', user=current_user, **data)

# Add expense via quick entry
@app.route('/add-entry', methods=['POST'])
@login_required
def add_entry():
    entry = request.form.get('entry', '').strip().split(' ', 1)
    try:
        amount = float(entry[0])
        description = entry[1] if len(entry) > 1 else 'Other'
        db.session.add(Expense(
            user_id=current_user.id,
            amount=amount,
            category='Other',
            description=description,
            payment_method='Cash',
            date=datetime.date.today()
        ))
        db.session.commit()
        flash('Expense added!', 'success')
    except:
        flash('Invalid format. Try: 250 Zomato', 'danger')

    return redirect(url_for('dashboard'))
# Budget Page
@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    now = datetime.datetime.now()
    
    # Define fixed categories
    category_names = ['Food', 'Transport', 'Shopping', 'Medical', 'Education', 'Entertainment', 'Other']

    if request.method == 'POST':
        for category_name in category_names:
            limit_value = request.form.get(f'limit_{category_name}')
            if limit_value:
                # Check if budget already exists for this category
                existing = Budget.query.filter_by(
                    user_id=current_user.id,
                    category=category_name,
                    month=now.month,
                    year=now.year
                ).first()

                if existing:
                    # Update existing budget
                    existing.monthly_limit = float(limit_value)
                else:
                    # Create new budget
                    db.session.add(Budget(
                        user_id=current_user.id,
                        category=category_name,
                        monthly_limit=float(limit_value),
                        month=now.month,
                        year=now.year
                    ))
        db.session.commit()
        flash('Budget updated successfully!', 'success')
        return redirect(url_for('budget'))

    # Build category data for template
    categories = []
    for category_name in category_names:
        # Get budget limit for this category
        budget_entry = Budget.query.filter_by(
            user_id=current_user.id,
            category=category_name,
            month=now.month,
            year=now.year
        ).first()

        limit = float(budget_entry.monthly_limit) if budget_entry else 0

        # Get total spent in this category this month
        expenses = Expense.query.filter_by(
            user_id=current_user.id,
            category=category_name
        ).filter(
            db.extract('month', Expense.date) == now.month,
            db.extract('year', Expense.date) == now.year
        ).all()

        spent = float(sum(e.amount for e in expenses))

        # Calculate percentage
        if limit > 0:
            percentage = min(round((spent / limit) * 100), 100)
        else:
            percentage = 0

        categories.append({
            'name': category_name,
            'limit': limit,
            'spent': spent,
            'percentage': percentage
        })

    return render_template('budget.html', user=current_user, categories=categories)