from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:srg%402005@localhost/smart_expense_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'smartexpense123'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.route("/")
def home():
    return "Smart Expense System is running!"

@app.route('/test-db')
def test_db():
    try:
        db.session.execute(db.text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

if __name__ == "__main__":
    app.run(debug=True)