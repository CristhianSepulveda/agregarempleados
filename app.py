from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'xxxx',
    'database': 'empleado',
    "port":"3307"
}
print(DB_CONFIG)

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formularioeliminar')
def formularioeliminar():
    return render_template('formularioeliminar.html')

@app.route('/eliminar_empleado', methods=['POST'])
def eliminar_empleado():
    id_empleado = request.form.get('idEmpleado')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM empleados WHERE id = %s", (id_empleado,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))




@app.route("/formularioagregar")
def formularioagregar():
    return render_template("formularioagregar.html")


@app.route("/formulariolistar")
def formulariolistar():
    return render_template("formulariolistar.html")


@app.route("/formularioactualizar")
def formularioactualizar():
    return render_template("formularioactualizar.html")


@app.route("/formulariobuscar")
def formulariobuscar():
    return render_template("formulariobuscar.html")






if __name__ == '__main__':
    app.run(debug=True)