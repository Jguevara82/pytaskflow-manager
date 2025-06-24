from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
 
from backend.models import User, db # Importar User para usar sus métodos
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Ruta para el registro de nuevos usuarios."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Falta nombre de usuario o contraseña"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "El nombre de usuario ya existe"}), 400

    new_user = User(username=username) # Crear usuario sin hashear aún
    new_user.set_password(password) # Usar el método set_password para hashear y asignar
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado exitosamente"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Ruta para el login de usuarios."""
    data = request.get_json()
    username = data.get('username')  # Obtiene el nombre de usuario del JSON
    password = data.get('password')  # Obtiene la contraseña del JSON

    user = User.query.filter_by(username=username).first()  # Busca el usuario por nombre de usuario

    if user and user.check_password(password): # Usar check_password para verificar
        access_token = create_access_token(identity=str(user.id)) # Genera el token JWT
        return jsonify({"message": "Login exitoso", "access_token": access_token}), 200
    else:
        # Devuelve un mensaje de error si las credenciales son incorrectas
        return jsonify({"message": "Nombre de usuario o contraseña incorrectos"}), 401
