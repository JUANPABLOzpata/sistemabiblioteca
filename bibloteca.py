from materiales import *
from personas import *

class SistemaBiblioteca:   
    def __init__(self): 
        self.__materiales = {} #hacemos este diccionario para guardar materiales usando su llave
        self.__usuarios = {}  

   
    def registrar_material(self, material):
    #vamos a vereficar si el material ya existe usando codigo id
        if material.get_codigo_id in self.__materiales:
            print(f"Error: El material con ID {material.get_codigo_id} ya existe.")
            return False
        
        self.__materiales[material.get_codigo_id] = material
        print(f"Material '{material.get_titulo}' registrado con éxito.")
        return True

    # Sobrecarga: Registrar Libro y este lo registra en el diccionario
    def registrar_material_libro(self, libro):
        return self.registrar_material(libro)

    # Método para registrar usuario
    def registrar_usuario(self, usuario):
        #vereficamos si el usuario ya existe por su identificacion
        if usuario.identificacion in self.__usuarios:
            print(f"Error: El usuario con ID {usuario.identificacion} ya existe.")
            return False
        
        self.__usuarios[usuario.identificacion] = usuario
        print(f"Usuario '{usuario.nombre}' registrado con éxito.")
        return True
    
    
    # POLIMORFISMO: CLASE BASE EN MÉTODOS
   
    def prestar_material(self, id_material, id_usuario):
      
        material = self.__materiales.get(id_material)
        usuario = self.__usuarios.get(id_usuario)

        #hacemos validaciones para saber su existencia 
        if not material:
            print(f"Error: Material con ID {id_material} no encontrado.")
            return
        if not usuario:
            print(f"Error: Usuario con ID {id_usuario} no encontrado.")
            return
        
        # Uso del polimorfismo 
        if not material.es_prestamo_permitido():
            print(f"Préstamo Denegado: '{material.get_titulo}' es solo para consulta.")
            return

        # Uso del polimorfismo 
        #cada usuario definimos el propio limite de prestamos 
        if len(usuario.materiales_prestados) >= usuario.get_max_prestamos():
            print(f"Préstamo Denegado: {usuario.get_tipo_usuario()} {usuario.nombre} ha alcanzado el límite de {usuario.get_max_prestamos()} préstamos.")
            return
        
        if material.prestar(): # Llama al método interno del material
            usuario.agregar_prestamo(material)
            self.__notificar_prestamo(usuario, material) # Método privado
            print(f"Préstamo exitoso de '{material.get_titulo}' a {usuario.nombre}.")
        
    def devolver_material(self, id_material, id_usuario):
        material = self.__materiales.get(id_material)
        usuario = self.__usuarios.get(id_usuario)

        if not material or not usuario:
            print("Error: Material o Usuario no encontrado.")
            return

        if usuario.remover_prestamo(material):
            material.devolver()
            print(f"Devolución exitosa de '{material.get_titulo}' por {usuario.nombre}.")
        else:
            print(f"Error: El material {material.get_titulo} no estaba prestado a {usuario.nombre}.")


    
    # ENCAPSULAMIENTO: MÉTODO PRIVADO INTERNA
    
    def __notificar_prestamo(self, usuario, material):
        #Método privado para simular una notificación interna
        print(f"Notificación Interna: Se registró el préstamo de ID {material.get_codigo_id} a {usuario.identificacion}")

    # Búsqueda polimórfica simple (Sobrecarga simulada con chequeo de tipo)
    def buscar_material(self, criterio):
        
        #Método básico para buscar un material por ID o por Título.
        #Solo devuelve el primer resultado encontrado si busca por título.
        
       
        # Usamos try/except para manejar si el criterio NO es un número (int).
        try:
            codigo_id = int(criterio)
            material = self.__materiales.get(codigo_id)
            
            if material:
                print(f"\n--- Búsqueda por ID {codigo_id} exitosa ---")
                print(material.mostrar_info())
                return material
            
            # Si el ID no se encuentra, pasa a buscar por título.
        except ValueError:
            # Si la conversión a int falla (porque es una cadena), no hacemos nada y
            # pasamos directamente a la búsqueda por título.
            pass
            
        # 2. BÚSQUEDA POR TÍTULO 
        titulo_buscado = str(criterio).lower()
        
        print(f"\n--- Buscando por Título que contenga: '{titulo_buscado}' ---")
        
        for id_material, material in self.__materiales.items():
            # Usamos el getter de título para verificar la coincidencia
            if titulo_buscado in material.get_titulo.lower(): 
                print(f"¡Material encontrado!")
                print(material.mostrar_info())
                # En la versión simple, retornamos el PRIMER material que coincida.
                return material
                
        # 3. SI NADA FUE ENCONTRADO
        print(f"Material con criterio '{criterio}' no encontrado en la biblioteca.")
        return None