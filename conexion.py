import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def conectar():
    """Establece y retorna una conexión a la base de datos MySQL usando variables de entorno."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "biblioteca_db"),
        )
        return conexion
    except Error as e:
        raise ConnectionError(f"Error al conectar a la base de datos MySQL: {e}") from e
    
