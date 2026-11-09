from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

# Base de datos (se crea sola en la misma carpeta)
DATABASE = 'kronox_gym.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inscripciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            telefono TEXT NOT NULL,
            plan TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/inscribir', methods=['POST'])
def inscribir():
    datos = request.get_json()
    if not datos or not all(k in datos for k in ('nombre', 'email', 'telefono', 'plan')):
        return jsonify({'error': 'Faltan datos obligatorios'}), 400
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO inscripciones (nombre, email, telefono, plan) VALUES (?, ?, ?, ?)',
            (datos['nombre'], datos['email'], datos['telefono'], datos['plan'])
        )
        conn.commit()
        conn.close()
        return jsonify({'mensaje': '¡Inscripción guardada exitosamente!'}), 201
    except Exception as e:
        return jsonify({'error': f'Error al guardar: {str(e)}'}), 500

# Ruta extra para que TÚ veas los datos guardados (útil para tu demo de IHC)
@app.route('/admin/inscripciones')
def ver_inscripciones():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, email, telefono, plan, fecha_registro FROM inscripciones ORDER BY id DESC')
    filas = cursor.fetchall()
    conn.close()
    html = "<h1>Inscripciones Registradas</h1><table border='1' cellpadding='8'>"
    html += "<tr><th>ID</th><th>Nombre</th><th>Email</th><th>Teléfono</th><th>Plan</th><th>Fecha</th></tr>"
    for f in filas:
        html += f"<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td><td>{f[4]}</td><td>{f[5]}</td></tr>"
    html += "</table><br><a href='/'>Volver al inicio</a>"
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)