from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mini'


mysql = MySQL(app)


@app.route('/')
def index():
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuario")
    usuarios = cur.fetchall()
    cur.close()
    return render_template('index.html', usuarios=usuarios)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        
        nombre = request.form['nombre']
        email = request.form['email']

       
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuario (nombre, email) VALUES (%s, %s)", (nombre, email))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    return render_template('agregar.html')


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
      
        nombre = request.form['nombre']
        email = request.form['email']

      
        cur.execute("UPDATE usuario SET nombre = %s, email = %s WHERE id = %s", (nombre, email, id))
        mysql.connection.commit()
        cur.close()
        return redirect('/')
    else:
     
        cur.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        usuario = cur.fetchone()
        cur.close()
        return render_template('editar.html', usuario=usuario)


@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM usuario WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect('/')


if __name__ == '__main__':
    app.run()
