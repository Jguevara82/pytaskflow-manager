from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from backend.auth.__init__ import auth_bp # Corregir la importación
from backend.tasks.__init__ import tasks_bp # Corregir la importación
from backend.models import db, User, Task

from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')


# Configuración y inicialización de Flask-JWT-Extended
app.config["JWT_SECRET_KEY"] = "super-secret" # Cambiar esto a una variable de entorno en producción
app.config['STRICT_SLASHES'] = False # Desactivar redirecciones automáticas de barras finales
jwt = JWTManager(app)

# Manejadores de errores para Flask-JWT-Extended
@jwt.unauthorized_loader
def custom_unauthorized_response(callback):
    return jsonify({"message": "Falta el encabezado de autorización o el token es inválido"}), 401

@jwt.invalid_token_loader
def custom_invalid_token_response(callback):
    return jsonify({"message": "El token proporcionado es inválido o ha expirado"}), 422

app.register_blueprint(tasks_bp, url_prefix='/tasks') # Registrar el blueprint de tareas

@app.route('/')
def index():
	return "TaskFlow Manager Backend - Welcome"

app.add_url_rule('/', endpoint='index', view_func=index)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		app.run(debug=True)
