class persona:
    def __init__(self, nombre, identificacion):
        self._nombre = nombre
        self.identificacion = identificacion
        self.__materiales_prestados = []
        
        
    def get_tipo_usuario(self):
        return "usuario general"
    
    
    def get_max_prestamos(self):
        raise NotImplementedError(" las subclases deben definir el limite de prestamos")
    
        
    #encapsulamiento  
    #getter para nombre
    
    @property
    def nombre(self):
        return self._nombre
    
    #getter para identidicacion
    @property
    def identificacion(self):
        return self._identificacion
    
    # SETTER con VALIDACIÓN (Encapsulamiento)
    @identificacion.setter
    def identificacion(self, identificacion):
        """Valida que la identificación tenga 10 dígitos."""
        if not (isinstance(identificacion, str) and len(identificacion) == 10 and identificacion.isdigit()):
            raise ValueError(" La identificación debe ser una cadena de 10 dígitos.")
        self._identificacion = identificacion
    
    # Método para cambiar identificación (alternativo al setter)
    def set_identificacion(self, identificacion):
        self.identificacion = identificacion
        
    @property
    def materiales_prestados(self):
        return self.__materiales_prestados
    
    # Métodos para agregar y remover préstamos
    def agregar_prestamo(self, material):
        self.__materiales_prestados.append(material)
    
    def remover_prestamo(self, material):
        if material in self.__materiales_prestados:
            self.__materiales_prestados.remove(material)
            return True
        return False
    

class Estudiante(persona):
    def __init__(self, nombre, identificacion, carrera):
        super().__init__(nombre, identificacion)
        self._carrera = carrera
        self.__max_prestamos = 5
        
        #polimorfismo sobreescritura
    def get_tipo_usuario(self):
        
        return "estudiante"
        
    def get_max_prestamos(self):
        return self.__max_prestamos
    
    
        
        
        
    #getter para _carrera
    @property
    def carrera(self):
        return self._carrera
        
        
    def mostrar_info(self):
        return f"tipo: {self.get_tipo_usuario()} | nombre : {self.nombre} | carrera: {self.carrera} | id : {self.identificacion}"
        
        
class Profesor(persona):
    def __init__(self, nombre, identificacion, departamento):
        super().__init__(nombre, identificacion)
        self._departamento = departamento
        self.__max_prestamos = 10
        
    
    def get_tipo_usuario(self):
        return "profesor"
    
    def get_max_prestamos(self):
        return self.__max_prestamos
    
    
        
    #getter para _departamento
    @property
    def departamento(self):
        
        return self._departamento
        
        
    def mostrar_info(self):
        return f"TIPO: {self.get_tipo_usuario()} | NOMBRE: {self.nombre} | DEPARTAMENTO: {self.departamento} | ID: {self.identificacion}"
        
        
        
        
        
    
        
        
        
        
    
    
    
    
        
        
    
    
        
        
    


        
        
        
        
    
        
        
        