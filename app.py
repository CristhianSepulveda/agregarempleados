from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'empleados.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agregar_empleado', methods=['GET', 'POST'])
def agregar_empleado():
    if request.method == 'POST':
        # Lógica para agregar empleado a la base de datos
        return redirect(url_for('index'))
    return render_template('agregar_empleado.html')

@app.route('/listar_empleados')
def listar_empleados():
    # Lógica para obtener lista de empleados desde la base de datos
    return render_template('listar_empleados.html', empleados=empleados)

@app.route('/eliminar_empleado/<int:id>', methods=['POST'])
def eliminar_empleado(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM empleados WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar_empleados'))

@app.route('/actualizar_empleado/<int:id>', methods=['GET', 'POST'])
def actualizar_empleado(id):
    if request.method == 'POST':
        # Lógica para actualizar empleado en la base de datos
        return redirect(url_for('listar_empleados'))
    return render_template('actualizar_empleado.html', empleado=empleado)

@app.route('/buscar_empleado', methods=['POST'])
def buscar_empleado():
    # Lógica para buscar empleado por ID
    return render_template('buscar_empleado.html', empleado=empleado)

if __name__ == '__main__':
    app.run(debug=True)
