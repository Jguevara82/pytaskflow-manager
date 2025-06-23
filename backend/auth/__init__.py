from flask import Blueprint, request, jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Ruta para el registro de nuevos usuarios."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    # Lógica de registro (pendiente de implementar)
    return jsonify({"message": "Usuario registrado (pendiente de implementar)"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Ruta para el login de usuarios."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    return jsonify({"message": "Login exitoso (pendiente de implementar)"}), 200
