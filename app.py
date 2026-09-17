from flask import Flask, render_template, request, jsonify, send_from_directory
import mysql.connector
import os

app = Flask(__name__, template_folder='.', static_folder='.')

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "tu_password"  
}
DB_NAME = "club_ciencias"

def inicializar_bd():
    """Crea la base de datos y la tabla 'usuarios' si no existen."""
    try:
        # Conexión inicial sin especificar base de datos
        db = mysql.connector.connect(**DB_CONFIG)
        cursor = db.cursor()
        
        # Crea la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        cursor.execute(f"USE {DB_NAME}")
        
        # Crea tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255) NOT NULL,
                fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        db.commit()
        cursor.close()
        db.close()
        print("Base de datos y tabla creadas")
    except mysql.connector.Error as err:
        print(f"Error al inicializar la base de datos: {err}")

def conectar():
    """Conecta directamente a la base de datos club_ciencias."""
    config = DB_CONFIG.copy()
    config["database"] = DB_NAME
    return mysql.connector.connect(**config)

# Ruta principal de index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Servir archivos estáticos como styles.css y script.js
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)

# Endpoint que consume el js vía AJAX/Fetch
@app.route("/api/guardar-nombre", methods=["POST"])
def guardar_api():
    data = request.get_json()
    if not data or "nombre" not in data:
        return jsonify({"status": "error", "message": "Nombre no proporcionado"}), 400
    
    nombre = data["nombre"]
    
    try:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        db.commit()
        cursor.close()
        db.close()
        return jsonify({"status": "success", "message": "Nombre guardado con éxito"}), 200
    except mysql.connector.Error as err:
        print(f"Error en MySQL: {err}")
        return jsonify({"status": "error", "message": str(err)}), 500

# Ruta original por formulario tradicional
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form.get("nombre")
    if nombre:
        db = conectar()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        db.commit() 
        db.close()
    return redirect("/")

if __name__ == "__main__":
    # Inicializa la BD al arrancar la pagina :V
    inicializar_bd()
    # Cambiado al puerto 3000 que es el que busca la seccion script.js
    app.run(host="localhost", port=3000, debug=True)