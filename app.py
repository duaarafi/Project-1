from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/test-db')
def test_db():
    try:
        db.session.execute(db.text('SELECT 1'))
        return 'Database connected successfully!'
    except Exception as e:
        return f'Database connection failed: {str(e)}'

from routes import *

if __name__ == "__main__":
    app.run(debug=True)