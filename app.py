from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:srg@2005@localhost/smart_expense_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'smartexpense123'

db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Smart Expense System is running!"

if __name__ == "__main__":
    app.run(debug=True)