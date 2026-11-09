from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
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
        # Feedback personalizado (IHC: Satisfacción)
        return jsonify({'mensaje': f"¡Felicidades {datos['nombre']}, ya estás inscrito en el plan {datos['plan']}!"}), 201
    except Exception as e:
        return jsonify({'error': f'Error al guardar: {str(e)}'}), 500

# --- PANEL DE ADMINISTRACIÓN CON DISEÑO (IHC: Consistencia) ---
@app.route('/admin/inscripciones')
def ver_inscripciones():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, nombre, email, telefono, plan, fecha_registro FROM inscripciones ORDER BY id DESC')
    filas = cursor.fetchall()
    conn.close()
    
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Admin - Kronox Gym</title>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #f4f4f4; color: #222; padding: 2rem; }
            h1 { color: #8B0000; text-transform: uppercase; border-bottom: 3px solid #8B0000; padding-bottom: 10px; }
            table { width: 100%; border-collapse: collapse; margin-top: 1rem; background: white; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-radius: 8px; overflow: hidden; }
            th { background: #8B0000; color: white; padding: 12px; text-align: left; }
            td { padding: 12px; border-bottom: 1px solid #ddd; }
            tr:hover { background: #f1f1f1; }
            .btn { display: inline-block; margin-top: 1rem; padding: 10px 20px; background: #8B0000; color: white; text-decoration: none; border-radius: 8px; font-weight: bold; }
            .btn:hover { background: #5c0000; }
        </style>
    </head>
    <body>
        <h1>Panel de Control - Inscripciones</h1>
        <table>
            <tr><th>ID</th><th>Nombre</th><th>Email</th><th>Teléfono</th><th>Plan</th><th>Fecha</th></tr>
    """
    for f in filas:
        html += f"<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td><td>{f[4]}</td><td>{f[5]}</td></tr>"
    html += """
        </table>
        <a href="/" class="btn">← Volver al Gimnasio</a>
    </body>
    </html>
    """
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    app.run(host='0.0.0.0', port=port, debug=True)
