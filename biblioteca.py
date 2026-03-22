from materiales import *
from personas import *
from conexion import conectar

class SistemaBiblioteca:
    
    def registrar_material(self, material):
        
        conexion = conectar()
        cursor = conexion.cursor()
        
        
        try:
            cursor.execute("""
                INSERT INTO materiales 
                (id, titulo, tipo, disponible, autor, editorial, año_publicacion, numero_paginas, isbn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                material.get_codigo_id,
                material.get_titulo,
                material.get_tipo_material(),
                True,
                material._autor,
                material._editorial,
                material._año_publicacion,
                material._numero_paginas,
                material._isbn
            ))
            conexion.commit()
            print(f"Material '{material.get_titulo}' registrado en la BD.")
            
        except Exception as e:
            print(f"Error al registrar: {e}")
            
        finally:
            cursor.close()
            conexion.close()
            
    def registrar_material_libro(self, libro):
        return self.registrar_material(libro)

    def registrar_usuario(self, usuario):
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            # el campo extra guarda carrera o departamento según el tipo
            extra = usuario.carrera if hasattr(usuario, 'carrera') else usuario.departamento
            
            cursor.execute("""
                INSERT INTO usuarios (identificacion, nombre, tipo, extra)
                VALUES (%s, %s, %s, %s)
            """, (
                usuario.identificacion,
                usuario.nombre,
                usuario.get_tipo_usuario(),
                extra
            ))
            conexion.commit()
            print(f"Usuario '{usuario.nombre}' registrado en la BD.") #se registro en la base de datos
            
        except Exception as e:
            print(f"Error al registrar usuario: {e}")
            
        finally:
            cursor.close()
            conexion.close()

    def prestar_material(self, id_material, id_usuario):
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            # Actualiza disponibilidad en la BD
            cursor.execute("""
                UPDATE materiales SET disponible = FALSE WHERE id = %s
            """, (id_material,))
            
            # Registra el préstamo
            cursor.execute("""
                INSERT INTO prestamos (id_material, id_usuario, fecha)
                VALUES (%s, %s, CURDATE())
            """, (id_material, id_usuario))
            
            conexion.commit()
            print(f"Préstamo registrado en la BD.")
            
        except Exception as e:
            print(f"Error al prestar: {e}")
            
        finally:
            cursor.close()
            conexion.close()
        
    def devolver_material(self, id_material, id_usuario):
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            # Verificar que el préstamo existe
            cursor.execute("""
                SELECT * FROM prestamos 
                WHERE id_material = %s AND id_usuario = %s
            """, (id_material, id_usuario))
            
            prestamo = cursor.fetchall()
            
            if not prestamo:
                print(f"Error: No se encontró préstamo del material {id_material} para el usuario {id_usuario}.")
                return
            
            # Eliminar el préstamo
            cursor.execute("""
                DELETE FROM prestamos 
                WHERE id_material = %s AND id_usuario = %s
            """, (id_material, id_usuario))
            
            # Marcar material como disponible
            cursor.execute("""
                UPDATE materiales SET disponible = TRUE 
                WHERE id = %s
            """, (id_material,))
            
            conexion.commit()
            print(f"Devolución exitosa del material {id_material} por usuario {id_usuario}.")
            
        except Exception as e:
            print(f"Error al devolver: {e}")
        finally:
            cursor.close()
            conexion.close()

    
    # ENCAPSULAMIENTO: MÉTODO PRIVADO INTERNA
    
    def __notificar_prestamo(self, usuario, material):
        #Método privado para simular una notificación interna
        print(f"Notificación Interna: Se registró el préstamo de ID {material.get_codigo_id} a {usuario.identificacion}")

    # Búsqueda polimórfica simple (Sobrecarga simulada con chequeo de tipo)
    def buscar_material(self, criterio):
        conexion = conectar()
        cursor = conexion.cursor()
        
        try:
            # Búsqueda por ID
            try:
                codigo_id = int(criterio)
                cursor.execute("SELECT * FROM materiales WHERE id = %s", (codigo_id,))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"\n--- Búsqueda por ID {codigo_id} exitosa ---")
                    print(f"titulo: {resultado[1]} | ID: {resultado[0]} | estado: {'disponible' if resultado[3] else 'prestado'}")
                    return resultado
            except ValueError:
                pass
            
            # Búsqueda por título
            titulo_buscado = str(criterio).lower()
            print(f"\n--- Buscando por Título que contenga: '{titulo_buscado}' ---")
            cursor.execute("SELECT * FROM materiales WHERE LOWER(titulo) LIKE %s", (f"%{titulo_buscado}%",))
            resultado = cursor.fetchone()
            if resultado:
                print(f"¡Material encontrado!")
                print(f"titulo: {resultado[1]} | ID: {resultado[0]} | estado: {'disponible' if resultado[3] else 'prestado'}")
                return resultado
            
            print(f"Material con criterio '{criterio}' no encontrado.")
            return None
            
        except Exception as e:
            print(f"Error al buscar: {e}")
        finally:
            cursor.close()
            conexion.close()