from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from backend.auth.__init__ import auth_bp # Corregir la importación
from backend.models import db, User, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taskflow.db'
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

# Nuevo blueprint para tareas
tasks_bp = Blueprint('tasks', __name__)
app.register_blueprint(tasks_bp, url_prefix='/tasks') # Registrar el blueprint de tareas

@app.route('/')

# Lógica para las rutas de tareas
@tasks_bp.route('/', methods=['GET', 'POST']) # La ruta base del blueprint ya es /tasks
def tasks(): # ¡Necesitas definir la función aquí!
    if request.method == 'GET':
        all_tasks = Task.query.all()
        return jsonify([{'id': task.id, 'title': task.title, 'description': task.description, 'status': task.status, 'user_id': task.user_id} for task in all_tasks])

    elif request.method == 'POST':
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        status = data.get('status', 'pending') # Estado por defecto

        if not title:
            return jsonify({'message': 'El título de la tarea es obligatorio'}), 400

        new_task = Task(title=title, description=description, status=status, user_id=1) # **TEMPORAL: Asociar a un user_id fijo**
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'title': new_task.title, 'description': new_task.description, 'status': new_task.status, 'user_id': new_task.user_id}), 201

@tasks_bp.route('/<int:task_id>', methods=['GET', 'PUT', 'DELETE'])
def task(task_id):
    task = Task.query.get_or_404(task_id)

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


def index():
	return "TaskFlow Manager Backend - Welcome"

app.add_url_rule('/', endpoint='index', view_func=index)

if __name__ == '__main__':
	with app.app_context():
		db.create_all()
		app.run(debug=True)
