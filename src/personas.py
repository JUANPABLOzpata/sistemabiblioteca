from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase base abstracta que representa a un usuario del sistema de biblioteca."""

    def __init__(self, nombre: str, identificacion: str):
        if not nombre or not str(nombre).strip():
            raise ValueError("El nombre no puede estar vacío.")
        self._nombre = str(nombre).strip()
        self.identificacion = identificacion  # Valida mediante el setter
        self.__materiales_prestados = []

    def get_tipo_usuario(self) -> str:
        return "usuario general"

    @abstractmethod
    def get_max_prestamos(self) -> int:
        """Retorna el número máximo de préstamos simultáneos permitidos."""
        pass

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def identificacion(self) -> str:
        return self._identificacion

    @identificacion.setter
    def identificacion(self, identificacion: str):
        """Valida que la identificación sea una cadena numérica de exactamente 10 dígitos."""
        if not (isinstance(identificacion, str) and len(identificacion) == 10 and identificacion.isdigit()):
            raise ValueError("La identificación debe ser una cadena de 10 dígitos numéricos.")
        self._identificacion = identificacion

    def set_identificacion(self, identificacion: str):
        self.identificacion = identificacion

    @property
    def materiales_prestados(self) -> list:
        return list(self.__materiales_prestados)

    def puede_prestar(self) -> bool:
        """Verifica si el usuario aún no ha alcanzado su límite de préstamos."""
        return len(self.__materiales_prestados) < self.get_max_prestamos()

    def agregar_prestamo(self, material) -> bool:
        if not self.puede_prestar():
            raise ValueError(
                f"El usuario {self._nombre} ha alcanzado su límite de {self.get_max_prestamos()} préstamos."
            )
        if material not in self.__materiales_prestados:
            self.__materiales_prestados.append(material)
            return True
        return False

    def remover_prestamo(self, material) -> bool:
        for item in self.__materiales_prestados:
            if item == material or getattr(item, "codigo_id", None) == getattr(material, "codigo_id", material):
                self.__materiales_prestados.remove(item)
                return True
        return False

    def mostrar_info(self) -> str:
        return f"Tipo: {self.get_tipo_usuario()} | Nombre: {self.nombre} | ID: {self.identificacion}"


class Estudiante(Persona):
    """Usuario de tipo estudiante con límite de 5 préstamos."""

    def __init__(self, nombre: str, identificacion: str, carrera: str):
        super().__init__(nombre, identificacion)
        self._carrera = str(carrera).strip()
        self.__max_prestamos = 5

    def get_tipo_usuario(self) -> str:
        return "estudiante"

    def get_max_prestamos(self) -> int:
        return self.__max_prestamos

    @property
    def carrera(self) -> str:
        return self._carrera

    def mostrar_info(self) -> str:
        return (
            f"Tipo: {self.get_tipo_usuario()} | Nombre: {self.nombre} | "
            f"Carrera: {self.carrera} | ID: {self.identificacion}"
        )


class Profesor(Persona):
    """Usuario de tipo profesor con límite de 10 préstamos."""

    def __init__(self, nombre: str, identificacion: str, departamento: str):
        super().__init__(nombre, identificacion)
        self._departamento = str(departamento).strip()
        self.__max_prestamos = 10

    def get_tipo_usuario(self) -> str:
        return "profesor"

    def get_max_prestamos(self) -> int:
        return self.__max_prestamos

    @property
    def departamento(self) -> str:
        return self._departamento

    def mostrar_info(self) -> str:
        return (
            f"Tipo: {self.get_tipo_usuario().upper()} | Nombre: {self.nombre} | "
            f"Departamento: {self.departamento} | ID: {self.identificacion}"
        )

# Alias de compatibilidad
persona = Persona
        
        
        
        
        
    
        
        
        
        
    
    
    
    
        
        
    
    
        
        
    


        
        
        
        
    
        
        
        