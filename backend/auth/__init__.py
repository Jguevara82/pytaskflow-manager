from flask import Blueprint, request, jsonify

from backend.models import User, db
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

    new_user = User(username=username, password=password) # Nota: La contraseña no está hasheada aún.
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

    # Verifica si el usuario existe y la contraseña coincide (sin hashear)
    if user and user.password == password:
        # Aquí iría la lógica para generar y devolver un token (pendiente)
        return jsonify({"message": "Login exitoso", "user_id": user.id}), 200
    else:
        # Devuelve un mensaje de error si las credenciales son incorrectas
        return jsonify({"message": "Nombre de usuario o contraseña incorrectos"}), 401
