from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)

@maestros_bp.route("/", methods=['GET'])
def lista_maestros():
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()
        maestros = []
        for fila in datos:
            maestro = {
                "idmaestro": fila[0], 
                "nombre": fila[1],
                "apaterno": fila[2], 
                "amaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
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

def leer_maestro_bd(idmaestro):
    cursor = None
    try:
        cursor = mysql.connection.cursor()
        sql = "SELECT idmaestro, nombre, apaterno, amaterno, correo FROM maestros WHERE idmaestro = {0}".format(idmaestro)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            maestro = {
                "idmaestro": datos[0], 
                "nombre": datos[1],
                "apaterno": datos[2], 
                "amaterno": datos[3],
                "correo": datos[4]
            }
            return maestro
        else:
            return None
    except Exception as ex:
        raise ex
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route("/<id>", methods=['GET'])
def leer_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro != None:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro encontrado',
                'exito': True
            })
        else:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro no encontrado',
                'exito': False
            })
    except Exception as ex:
        return jsonify({
            'message': f"error {ex}",
            'exito': False
        })

@maestros_bp.route("/", methods=['POST'])
def registrar_maestro():
    cursor = None
    try:
        maestro = leer_maestro_bd(request.json['idmaestro'])
        
        if maestro != None:
            return jsonify({'mensaje': 'Maestro ya existe, no se puede duplicar', 'exito': False})
        else:
            cursor = mysql.connection.cursor()
            sql = """INSERT INTO maestros (idmaestro, nombre, apaterno, amaterno, correo) 
                     VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')""".format(
                request.json['idmaestro'],
                request.json['nombre'],
                request.json['apaterno'],
                request.json['amaterno'],
                request.json['correo']
            )

            cursor.execute(sql)
            mysql.connection.commit()  
            return jsonify({'mensaje': 'Maestro registrado', 'exito': True})
            
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route('/<id>', methods=['PUT'])
def actualizar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id) 
        if maestro != None:
            cursor = mysql.connection.cursor()
            sql = """UPDATE maestros SET nombre ='{0}', apaterno='{1}', amaterno='{2}', correo='{3}'
            WHERE idmaestro ={4}""".format(
                request.json['nombre'],
                request.json['apaterno'], 
                request.json['amaterno'],
                request.json['correo'],
                id
            )
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Maestro actualizado", 'exito': True})
        else:
            return jsonify({'mensaje': "Maestro no encontrado", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error {0}".format(ex), 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()

@maestros_bp.route("/<id>", methods=['DELETE'])
def eliminar_maestro(id):
    cursor = None
    try:
        maestro = leer_maestro_bd(id)
        if maestro != None:
            cursor = mysql.connection.cursor()
            sql = "DELETE FROM maestros WHERE idmaestro={0}".format(id)
            cursor.execute(sql)
            mysql.connection.commit()
            return jsonify({'mensaje': "Maestro eliminado", 'exito': True})
        else:
            return jsonify({'mensaje': "Maestro no encontrado", 'exito': False})
    except Exception as ex:
        return jsonify({'mensaje': "Error: {}".format(ex), 'exito': False})
    finally:
        if cursor is not None:
            cursor.close()