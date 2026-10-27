from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)

@alumnos_bp.route("/", methods=['GET'])
def lista_alumnos():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        alumnos = []
        for fila in datos:
            alumno = {
                "matricula": fila[0], 
                "nombre": fila[1],
                "apaterno": fila[2], 
                "amaterno": fila[3],
                "correo": fila[4]
            }
            alumnos.append(alumno)

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        })

    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })
    finally:
        if cursor is not None:
            cursor.close()

def leer_alumno_bd(matricula):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT matricula, nombre, apaterno, amaterno, correo FROM alumnos WHERE matricula = {0}".format(matricula)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            alumno = {
                "matricula": datos[0], 
                "nombre": datos[1],
                "apaterno": datos[2], 
                "amaterno": datos[3],
                "correo": datos[4]
            }
            return alumno
        else:
            return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route("/<mat>", methods=['GET'])
def leer_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            return jsonify({
                'alumno': alumno,
                'mensaje': 'Alumno encontrado',
                'exito': True
            })
        else:
            return jsonify({
                'alumno': alumno,
                'mensaje': 'Alumno no encontrado',
                'exito': False
            })
    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })

@alumnos_bp.route("/", methods=['POST'])
def registrar_alumno():
    cursor = None
    try:
        alumno = leer_alumno_bd(request.json['matricula'])
        
        if alumno != None:
            return jsonify({'mensaje': 'Alumno ya existe, no se puede duplicar', 'exito': False})
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['matricula'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )

            cursor.execute(sql)
            mysql.connection.commit()  
            return jsonify({'mensaje': 'Alumno registrado', 'exito': True})
            
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route('/<mat>', methods=['PUT'])
def actualizar_alumno(mat):
    cursor = None
    try:
        alumno = leer_alumno_bd(mat) 
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE alumnos SET nombre ='{0}', apaterno='{1}', amaterno='{2}', correo='{3}'
            WHERE matricula ={4}""".format(
                request.json['nombre'],
                request.json['apaterno'], 
                request.json['amaterno'],
                request.json['correo'],
                mat
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno actualizado", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error {0}".format(ex), 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()

@alumnos_bp.route("/<mat>", methods=['DELETE'])
def eliminar_alumno(mat):
    cursor = None
    try:
        alumno = leer_alumno_bd(mat)
        if alumno != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula={0}".format(mat)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Alumno eliminado", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()