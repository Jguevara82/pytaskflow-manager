from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity # Asegúrate de importar jwt_required y get_jwt_identity
from backend.models import Task, db, User # Importar User y Task
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# Lógica para las rutas de tareas
@tasks_bp.route('/', methods=['GET', 'POST']) # La ruta base del blueprint ya es /tasks
@jwt_required()
def tasks(): # ¡Necesitas definir la función aquí!
    if request.method == 'GET':
        current_username = get_jwt_identity() # Obtener la identidad del usuario del token (username)
        current_user = User.query.filter_by(username=current_username).first()
        user_tasks = Task.query.filter_by(user_id=current_user.id).all() # Filtrar tareas por usuario autenticado
        return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'user_id': task.user_id} for task in user_tasks])

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', 'pending') # Estado por defecto

        if not title:
            return jsonify({'message': 'El título de la tarea es obligatorio'}), 400

        current_username = get_jwt_identity()
        current_user = User.query.filter_by(username=current_username).first()

        new_task = Task(title=title, description=description, status=status, user_id=current_user.id) # Asociar la tarea al usuario autenticado
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'status': new_task.status, 'user_id': new_task.user_id}), 201

@tasks_bp.route('/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def task(task_id):
    current_username = get_jwt_identity()
    current_user = User.query.filter_by(username=current_username).first()
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404() # Filtrar por user_id y verificar propiedad

    if request.method == 'GET':
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'user_id': task.user_id})

    elif request.method == 'PUT':
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)

        db.session.commit()
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'user_id': task.user_id})

    elif request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Tarea eliminada exitosamente'})
