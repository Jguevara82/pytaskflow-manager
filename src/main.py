from flask import Flask, send_file
from peticiones import insertar, query # Importa las funciones desde handlers.py

app = Flask(__name__)

@app.route("/")
def index():
    return send_file('index.html')

# Define tus otras funciones o configuraciones aquí

@app.route('/clientes', methods=['POST'])
def handle_insert_to_bigquery(): # Puedes renombrar las funciones aquí si quieres
    return insertar()

@app.route('/clientes', methods=['GET']) # Asumiendo que quieres leer con un método GET
def handle_leer_bigquery(): # Puedes renombrar las funciones aquí si quieres
    return query()

if __name__ == '__main__':
    app.run(debug=True) # O como inicies tu aplicación Flask
