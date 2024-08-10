import pyodbc # modulo para conectar a la base de datos de SQL Server
import datetime
from dotenv import load_dotenv #importar de la biblioteca de variables de entorno la funcion 'load_dotenv()'
import os # módulo para interactuar con el sistema operativo, incluyendo un metodo de acceso a variables de entorno.

load_dotenv()  # Esta función busca un archivo llamado .env
# os.getenv() permite acceder a las variables dentro del modulo '.env' 

#Cargar las constantes 
DATABASE = os.getenv('DATABASE') # Recupera el valor de la variable de entorno especificada. 
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = "localhost"


# Crear la conexion a la base de datos SQL Server
def connection_db():
    try:
        connection = pyodbc.connect( # Usamos la funcion connect del modulo pyodbc.
            'DRIVER={ODBC Driver 18 for SQL Server};' #Especifica el driver de coneion: ODBC Driver 18 for SQL Server - compatibel con SQLS -20
            'SERVER=' + HOST + ';' # Define el servidor al vamos a conectar esa db
            'DATABASE=' + DATABASE + ';' # Define a cual 'Tabla' conectarnos, y esta uardada en la variable DATABASE
            'UID=' + USER + ';' #  Define el nombre de usuario que se utilizará para la conexión. 
            'PWD=' + PASSWORD + ';' # Define la contraseña del usuario para la conexión. 
            'TrustServerCertificate=YES' #  Indica que se debe confiar en el certificado del servidor
        )
        return connection # Si la conexión es exitosa, se almacena en la variable 'connection'
    except Exception as e:
        print("Ha habido un problema al conectarse a la base de datos: " + str(e))
    return None # Si la coneion falla no hay nada que retornar


# Creamos una funcion para agregar datos a la base de datos:
def insert_data(Timestamp, Service_name, Log_level, Message):
    conn = connection_db()
    if conn:
        try:
            cursor = conn.cursor()
            received_at = datetime.datetime.now()  # Colecta el momento en el que el server recibe el log
            # Timestamp = Es el tiempo en que el evento ocurrió en el servicio que generó el log.
            cursor.execute('''
                INSERT INTO logs (Timestamp, Service_name, Log_level, Message, received_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (Timestamp, Service_name, Log_level, Message, received_at))
            conn.commit()
        except Exception as e:
            print(f"Error at insert data(): {str(e)}")
        finally:
            conn.close()
    else:
        print("The connection could not be established.")



