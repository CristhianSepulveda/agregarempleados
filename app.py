from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import base64

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'empleados',
    "port":"3306"
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
    cursor.execute("DELETE FROM empleado WHERE id = %s", (id_empleado,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(request.referrer)  # Redirecciona al usuario a la página anterior

@app.route('/formularioagregar')
def formularioagregar():
    return render_template('formularioagregar.html')

# Ruta para manejar el formulario y agregar empleado a la base de datos
@app.route("/agregar_empleado", methods=['POST'])
def agregar_empleado():
    # Recibe los datos del formulario
    nombre = request.form.get('nombre')
    apellidos = request.form.get('apellidos')
    documento = request.form.get('documentoIdentidad')
    direccion = request.form.get('direccion')
    telefono = request.form.get('telefono')
    foto = request.files['foto'].read()  # Almacena la imagen como datos binarios
    foto_binario = base64.b64encode(foto)  # Convierte la imagen a binario

    # Establece conexión a la base de datos
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Ejecuta la consulta SQL para insertar el nuevo empleado en la tabla
        cursor.execute("INSERT INTO empleado (nombre, apellidos, documento, direccion, telefono, foto) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, apellidos, documento, direccion, telefono, foto))
        
        # Guarda los cambios en la base de datos
        conn.commit()
        
        # Cierra el cursor y la conexión
        cursor.close()
        conn.close()
        
        # Redirecciona al usuario a la página anterior después de agregar el empleado
        return redirect(request.referrer)
    except Exception as e:
        # Si ocurre algún error, manejarlo apropiadamente, por ejemplo, mostrar un mensaje de error al usuario
        return render_template('error.html', error=str(e))

@app.route("/formulariolistar")
def formulariolistar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nombre, apellidos, documento, telefono, foto FROM empleado")
    empleados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("formulariolistar.html", empleados=empleados)

@app.route("/formularioactualizar")
def formularioactualizar():
    return render_template("formularioactualizar.html")

# Función para actualizar empleado
@app.route('/actualizar_empleado', methods=['POST'])
def actualizar_empleado():
    try:
        id_empleado = request.form['idEmpleado']
        campo = request.form['campo']
        nuevo_valor = request.form['nuevoValor']

        # Conectar a la base de datos
        cnx = mysql.connector.connect(**DB_CONFIG)
        cursor = cnx.cursor()

        # Preparar la consulta SQL
        update_query = f"UPDATE empleado SET {campo} = %s WHERE id = %s"
        data = (nuevo_valor, id_empleado)

        # Ejecutar la consulta
        cursor.execute(update_query, data)
        cnx.commit()

        # Cerrar la conexión
        cursor.close()
        cnx.close()

        return 'Empleado actualizado correctamente'
    except Exception as e:
        return f'Error al actualizar empleado: {str(e)}'

@app.route("/formulariobuscar")
def formulariobuscar():
    return render_template("formulariobuscar.html")
if __name__ == '__main__':
    app.run(debug=True)