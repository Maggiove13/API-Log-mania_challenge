import requests
import datetime
import random
import time # para el delay
import os
from dotenv import load_dotenv # para cargar las variables de entorno

load_dotenv() # Traemos las variables de entorno desde el archivo '.env'

API_KEY = os.getenv('API_KEY')

# URL de la API
API_URL = "http://localhost:5000/logs"


# Listas de servicios y niveles de log
service_names = ['Service1', 'Service2', 'Service3', 'Service4', 'Service5']
log_types = ['INFO', 'ERROR', 'DEBUG']


# Generar logs
def send_log(log):
    try:
        # Aquí se añade la clave de API al encabezado de la solicitud para que el servidor pueda autenticarla.
        headers = {
            'Authorization': API_KEY  # Añadir el token en el header 'Authorization'
        }
        response = requests.post(API_URL, json=log, headers=headers)
        response.raise_for_status()
        print('Log sent successfully:', log)
    except requests.exceptions.RequestException as e:
        print('Error sending log:', e)


def get_random_item(array): # Esta función va a elegir aleatoriamente entre las listas dadas
    return random.choice(array)


def generate_random_log():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f') # Marca el tiempo exacto en que se generó el log. #AÑO-MES-DÍA HORA:MINUTO:SEGUNDO.MILISEGUNDOS.
    service_name = get_random_item(service_names)
    log_level = get_random_item(log_types)
    message = f"This is a {log_level.lower()} message from {service_name}"
    
    # Devuelve el resultado en formato JSON
    return {
        'timestamp': timestamp,
        'service_name': service_name,
        'log_level': log_level,
        'message': message
    }

#Este archivo solo se ejecutara si lo hace directamente y no importado como modulo
if __name__ == "__main__": 
    while True:
        log = generate_random_log()
        send_log(log)
        time.sleep(5)  # Esperar 5 segundos antes de enviar el siguiente log