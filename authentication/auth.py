# authentication/auth.py
import os
from flask import request, jsonify
from functools import wraps # Es una función para mantener la metadata original de la función decorada, 
# algo útil cuando creamos decoradores.
from dotenv import load_dotenv

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

API_KEY = os.getenv('API_KEY')  # Cargar la API Key desde las variables de entorno

#  Esta es la función decoradora que envolverá otras funciones para añadirles la lógica de autenticación.
def authenticate_api_key(f): 
    
    @wraps(f) # asegura que la función decorada mantenga su nombre y docstring original.
    
    # Esta función interna será la que efectivamente añada la lógica de autenticación a la función decorada.
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')  # Obtener el token desde el header 'Authorization'
        if not api_key: # Si no se proporciona una api_key
            return jsonify({'message': 'API key is missing'}), 401

        if api_key != API_KEY:
            return jsonify({'message': 'Unauthorized'}), 401

        return f(*args, **kwargs) # Llamar a la función original si la API key es correcta
    return decorated_function