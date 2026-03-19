from abc import ABC, abstractmethod
from datetime import datetime

class Material(ABC):  #aqui definimos con abc que material sera una clase abstracta
    def __init__(self,titulo,codigo_id): #creamos el constructor 
        self._titulo = titulo #atributos protegidos 
        self._codigo_id = codigo_id #estos son los parametros 
        #atributo privado 
        self.__disponible = True #alamacena un valor booleano, indica que esta listo para ser prestado
        
        
    #metodos abstractos 
    @abstractmethod # se usa para declarar metodos que deben ser implementados en subclase
    def es_prestamo_permitido(self):
        pass
    
    
    @abstractmethod
    def get_tipo_material(self):
        pass
    
    
    #metodo concreto
    
    def mostrar_info(self):
        
        disponibilidad = "disponible" if self.__disponible else "prestado"
        return f"titulo : {self._titulo} | ID :{self._codigo_id} | estado : {disponibilidad}"
            
    #getters y setters para encapsulamiento
    @property
    def get_titulo(self):  #metodo para acceder a un atributo protegido 
        return self._titulo
    
    
    @property
    def get_codigo_id(self):
        return self._codigo_id
    
    
    #metodos privados
    
    def __cambiar_el_estado_dispo(self,estado):
        #metodo privado para cambiar estado de disponibilidad
        #metodo privado dentro de una clase para modificar un atributo privado
        #esto hace parte de encapsulacion 
        self.__disponible = estado 
        
        
    def prestar(self): #El método verifica dos cosas antes de hacer  el préstamo
        #self.es_prestamo_permitido() revisa el tipo de material puede prestarse
        if self.es_prestamo_permitido() and self.__disponible:
            self.__cambiar_el_estado_dispo(False) #marca como material no disponible 
            print(f"{self.get_tipo_material()} '{self._titulo}' ha sido prestado.")
            return True
        
        
        elif not self.__disponible: #Si __disponible es False, significa que ya alguien lo prestó antes
            print(f"{self.get_tipo_material()} '{self._titulo}' ya esta prestado.")
            
            return False
        else:
            print(f"{self.get_tipo_material()} '{self._titulo}' es solo de consulta y no se puede prestar")
            
            return False
        
        #metodo para que marca el material como disponible de nuevo 
        #imprime un mensaje de que ha sido devuelto
        
    def devolver(self):
        self.__cambiar_el_estado_dispo(True) #cambia el estado a disponible otra vez 
        print(f"- {self.get_tipo_material()} '{self._titulo}' ha sido devuelto")
        
        

# 1 clase abstracta

class publicacion(Material):
    def __init__(self, titulo, codigo_id, año_publicacion, editorial):
        super().__init__(titulo, codigo_id) #reutilizamos atributos anterios de material
        self._año_publicacion = año_publicacion
        self._editorial = editorial
        
        
        
    
    @property
    def año_publicacion(self):
        return self._año_publicacion
        
        
    #sobreescritura del metodo concreto
    
    
    
    #setter con una validacion (encapsulamiento)
    #para modificar un atributo
    @año_publicacion.setter
    def año_publicacion(self, año):
        
        #valida que el año no sea futuro
        #la validacion es para que si alguien pone años muy lejanos o asigna un año mayor al que estamos
        # el codigo no lo va permitir
        if año > datetime.now().year:
            raise ValueError("el año de publicacion no puede ser a años futuros ")
        self._año_publicacion = año #se ejecuta si la validacion pasa
    
    # Método para cambiar el año (alternativo al setter)
    def set_anio_publicacion(self, año):
        self.año_publicacion = año
    
    @property
    def editorial(self):
        return self._editorial
    
    @editorial.setter
    def editorial(self, nueva_editorial):
        self._editorial = nueva_editorial
        
        
        
# 2 clase abstracta
class Obra_literaria(publicacion):
    def __init__(self, titulo, codigo_id, año_publicacion, editorial, autor):
        super().__init__(titulo, codigo_id, año_publicacion, editorial)
        self._autor = autor
        
    @property
    def autor(self):
        return self._autor
    
    @autor.setter
    def autor(self, nuevo_autor):
        self._autor = nuevo_autor
        
    #todo el material es prestable aqui se aplica tambien polimorfismo 
    def es_prestamo_permitido(self):
        return True
        
        
    #aqui aplicamos la ultima herencia 
class libro(Obra_literaria):
    def __init__(self, titulo, codigo_id, año_publicacion, editorial, autor, numero_paginas, isbn):
        super().__init__(titulo, codigo_id, año_publicacion, editorial, autor)
        self._numero_paginas = numero_paginas
        self._isbn = isbn
        
    #getter para numero_paginas 
    def get_tipo_material(self):
        return "libro"
    
    @property
    def numero_paginas(self):
        return self._numero_paginas
    
    @numero_paginas.setter
    def numero_paginas(self, numero_paginas):
        #Valida que el número de páginas sea positivo
        if numero_paginas <= 0: #tiene que se mayor a 0 
            raise ValueError(" El número de páginas debe ser un valor positivo.")
        self._numero_paginas = numero_paginas
    
    # Método para cambiar número de páginas (alternativo al setter)
    def set_num_paginas(self, numero_paginas):
        self.numero_paginas = numero_paginas
        
    # GETTER solo lectura para isbn
    @property
    def isbn(self):
        return self._isbn
    
    
    
    
class Libro_texto(libro):
    def __init__(self, titulo, codigo_id, año_publicacion, editorial, autor, numero_paginas, isbn, curso_asociado):
        super().__init__(titulo, codigo_id, año_publicacion, editorial, autor, numero_paginas, isbn)
        self._curso_asociado = curso_asociado
        
        
    def get_tipo_material(self): #sobre escritura cambia el tipo de material 
        return "Libro de Texto"
    
    
    @property
    def curso_asociado(self):
        return self._curso_asociado
    
    @curso_asociado.setter
    def curso_asociado(self, nuevo_curso):
        self._curso_asociado = nuevo_curso
        
    
    
    
    
        
        
    
    
        