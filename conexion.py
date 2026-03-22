import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",  #es porque Mysql esta en docker
        port=3308,    #este es el puerto por defecto de Mysql
        user="root",  #mi ususario de Mysql
        password="1234", # esta es mi contraseña de Mysql
        database="biblioteca" 
        
    )
    
