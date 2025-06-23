from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.auth import auth_bp
from backend.models import db, User, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def index():
	return "TaskFlow Manager Backend - Welcome"

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		app.run(debug=True)
