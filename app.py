#Importar librerias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
#Inicio del programa
app = Flask(__name__)

#Configurar nuestra base de datos
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='webapp'

#Inicializar la extensión de MySQL
mysql = MySQL(app)

#Creamos la clave secreta
app.secret_key = '123456789'

#Crear las rutas
#Ruta inicial
@app.route('/')
def inicio():
    return render_template('inicio.html')
#Ruta información
@app.route('/info')
def info():
    return render_template('info.html')
#Ruta del login o inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'usuario' in request.form and 'pass' in request.form:
        username = request.form['usuario']
        password = request.form['pass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usuarios WHERE usuario=%s AND pass=%s', (username, password))
        cuenta = cursor.fetchone()

        #Validar si se obtuvo información
        if cuenta:
            flash('Ha iniciado sesión correctamente')
            return redirect(url_for('admin'))
        else:
            flash('No es posible iniciar sesión, datos incorrectos.')
    return render_template('login.html')
#Crear la ruta Administrador
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    #Crear un usuario
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('pass')
        email = request.form.get('email')

        #Insertar información
        if usuario and password and email:
            cursor.execute('INSERT INTO usuarios (usuario, pass, correo) VALUES (%s, %s, %s)',(usuario, password, email))
            mysql.connection.commit()
            flash('Usuario registrado correctamente.')
        else:
            flash('No fue posible registrar el usuario.')
    #Listar usuarios
    cursor.execute('SELECT * FROM usuarios')
    users = cursor.fetchall()
    return render_template('admin.html', users=users)

#Método eliminar
@app.route('/borrar_usuario/<int:id>') 
def borrar_usuario(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM usuarios WHERE id = %s',(id,))
    cursor.connection.commit()
    flash('Usuario eliminado correctamente')
    return redirect(url_for('admin'))


#Arrancar nuestra aplicación
if __name__ == '__main__':
    app.run(debug=True)