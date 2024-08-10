from flask import Flask, request, jsonify
from config import config # Llamamos al diccionario del modulo config
from conn_db import insert_data # Importamos la función 'insert_data()'
from datetime import datetime # Módulo estándar de Python para manejar fechas y horas.
from authentication.auth import authenticate_api_key  # Importar la función de autenticación
from conn_db import connection_db # Importamos la función 'connection_db()'

app = Flask(__name__)


@app.route('/logs', methods=['POST'])

@authenticate_api_key  # Antes de procesar la solicitud, la API verifica si la clave de la API es válida.

def create_log():
    if request.is_json: 
        data = request.get_json() # Obtiene el contenido JSON del cuerpo de la solicitud.
        service_name = data.get('service_name') # Extrae valores específicos del JSON
        log_level = data.get('log_level')
        message = data.get('message')
        timestamp_str = data.get('timestamp')

        try:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            return jsonify({'message': 'Timestamp format is incorrect'}), 400

        if service_name and log_level and message:
            insert_data(timestamp, service_name, log_level, message) # Insertamos los datos en la db
            return jsonify({'message': 'Log entry created successfully'}), 200 #  Convierte el resultado en JSON para que sea enviado como respuesta HTTP.
        else:
            return jsonify({'message': 'Missing fields in the request'}), 400
    else: # si el request no es json
        return jsonify({'message': 'Request must be JSON'}), 400



@app.route('/logs', methods=['GET'])
def get_logs():
    
    # Obtiene los parámetros de la URL que permiten filtrar los logs según el timestamp o received_at.
    start_timestamp = request.args.get('start_timestamp')
    end_timestamp = request.args.get('end_timestamp')
    start_received_at = request.args.get('start_received_at') # Fecha en que el servidor recibe
    end_received_at = request.args.get('end_received_at')

    query = 'SELECT * FROM logs WHERE 1=1'
    params = [] # Agregaremos mas instrucciones al query

    if start_timestamp and end_timestamp:
        query += ' AND Timestamp BETWEEN ? AND ?'
        params.extend([start_timestamp, end_timestamp])

    if start_received_at and end_received_at:
        query += ' AND received_at BETWEEN ? AND ?'
        params.extend([start_received_at, end_received_at])

    conn = connection_db() # cargamos en una variable la funcion de conexion a la db
    if conn:
        try:
            cursor = conn.cursor() 
            cursor.execute(query, params) # Ejecutara el query y las demas consultas 
            logs = cursor.fetchall()
            return jsonify([dict(zip([column[0] for column in cursor.description], row)) for row in logs])
        except Exception as e:
            return jsonify({'message': f"Error retrieving logs: {str(e)}"}), 500
        finally:
            conn.close()
    else:
        return jsonify({'message': 'The connection could not be established'}), 500


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=5000)
    
    
# Ejemplo de consulta
# http://localhost:5000/logs?start_timestamp=2024-08-07&end_timestamp=2024-08-10