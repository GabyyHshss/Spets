# -- El siguiente bloque de código es para iniciar un Servidor
# Modulo e Importamos el Framework 'Flask'
from flask import Flask, render_template, request, redirect, url_for, flash
#Modulo flask_mysqldb y framework MySQL
from flask_mysqldb import MySQL
#
app = Flask(__name__)

#Configuramos nuestra Conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flask_spets'
#
mysql = MySQL(app)
# settings
app.secret_key = 'mysecretkey'
#Una vez que entra a ESTA  -ruta- principal, daremos la siguiente respuesta.
@app.route('/')
#Función para enviar el mensaje 
def Index():
    #Hacemos la consulta para llenar la tabla y le pasamos los datos.
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)
#Creamos una ruta secundaria
@app.route('/add_contact', methods=['POST'])
#Devolverá un mensaje al ingresar a esa ruta
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s,%s,%s)',
                    (fullname,phone,email))
        mysql.connection.commit()
        flash('Añadido con Exito')
        return redirect(url_for('Index'))
#Creamos otra ruta
@app.route('/edit/<id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])
# Creamos la ruta que nos va a permitir completar la edición.
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor() 
        cur.execute("""
                    UPDATE contacts 
                    SET fullname = %s,
                        phone = %s,
                        email = %s
                        WHERE id = %s
                    """,(fullname, phone, email, id))
        mysql.connection.commit()
        flash('Contacto Modificado Sastifactoriamente')
        return redirect(url_for('Index'))
#Volvemos a crear otra ruta
@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado exitosamente')
    return redirect(url_for('Index'))
# Validar que se ejecuta el archivo principal
if __name__ == '__main__':
    app.run(port = 3000, debug = True)
