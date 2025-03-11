from flask import Flask, request, jsonify
import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv  


load_dotenv()  

app = Flask(__name__)


app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = MySQL(app)

@app.route('/adduserMYSQL', methods=['POST'])
def adduserMYSQL():
    try:
        nombre = request.json.get('nombre')
        color = request.json.get('color')
        ciudad = request.json.get('ciudad')

        cur = db.connection.cursor()
        sql = 'INSERT INTO usuarios (nombre, color, ciudad) VALUES (%s, %s, %s)'
        cur.execute(sql, (nombre, color, ciudad))
        db.connection.commit()
        cur.close()

        return jsonify({"message": "Usuario agregado con éxito"})

    except Exception as e:
        return jsonify({"error": "ERROR"})


@app.route('/deleteuserMYSQL', methods=['POST'])
def deleteuserMYSQL():
    nombre = request.json.get('nombre')
    cur = db.connection.cursor()
    sql = 'DELETE FROM usuarios WHERE nombre = %s'
    cur.execute(sql,(nombre,))
    db.connection.commit()
    cur.close()
    afectado = cur.rowcount
    if afectado > 0:
        return jsonify({"message": "Usuario eliminado con éxito"})
    else:
        return jsonify({"message": "Usuario no encontrado"})

@app.route('/updateuserMYSQL', methods=['PUT'])
def updateuserMYSQL():
    
    nombre = request.json.get('nombre')
    color = request.json.get('color')
    ciudad = request.json.get('ciudad')
    print(nombre, color, ciudad)
    cur = db.connection.cursor()
    sql = 'UPDATE usuarios SET nombre = %s, color = %s, ciudad = %s WHERE nombre = %s'
    values = (nombre, color, ciudad, nombre)
    cur.execute(sql, values)
    db.connection.commit()
    return jsonify({"message": "Usuario updated con éxito"})


@app.route('/getusersMYSQL', methods=['GET'])
def getusersMYSQL():
    cur = db.connection.cursor()
    sql = 'SELECT * FROM usuarios'
    cur.execute(sql)
    usuarios = cur.fetchall()

    return jsonify({"usuarios": usuarios})


if __name__ == "__main__":
    app.run(debug=True)
