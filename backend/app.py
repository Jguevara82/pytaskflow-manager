from flask import Flask
from backend.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def index():
    return "TaskFlow Manager Backend - Welcome"

if __name__ == '__main__':
    app.run(debug=True)
