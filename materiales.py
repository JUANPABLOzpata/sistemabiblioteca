from abc import ABC, abstractmethod
from datetime import datetime


class Material(ABC):
    """Clase base abstracta que representa cualquier material de la biblioteca."""

    def __init__(self, titulo: str, codigo_id: int):
        if not titulo or not str(titulo).strip():
            raise ValueError("El título no puede estar vacío.")
        self._titulo = str(titulo).strip()
        self._codigo_id = int(codigo_id)
        self.__disponible = True

    @abstractmethod
    def es_prestamo_permitido(self) -> bool:
        """Indica si el tipo de material puede ser prestado a domicilio."""
        pass

    @abstractmethod
    def get_tipo_material(self) -> str:
        """Retorna el nombre descriptivo del tipo de material."""
        pass

    def mostrar_info(self) -> str:
        disponibilidad = "disponible" if self.__disponible else "prestado"
        return f"Título: {self._titulo} | ID: {self._codigo_id} | Estado: {disponibilidad}"

    @property
    def titulo(self) -> str:
        return self._titulo

    @property
    def get_titulo(self) -> str:
        """Alias de compatibilidad para acceder al título."""
        return self._titulo

    @property
    def codigo_id(self) -> int:
        return self._codigo_id

    @property
    def get_codigo_id(self) -> int:
        """Alias de compatibilidad para acceder al código ID."""
        return self._codigo_id

    @property
    def disponible(self) -> bool:
        return self.__disponible

    def __cambiar_el_estado_dispo(self, estado: bool):
        """Método privado de encapsulamiento para modificar la disponibilidad."""
        self.__disponible = bool(estado)

    def prestar(self) -> bool:
        """Intenta marcar el material como prestado validando sus reglas."""
        if self.es_prestamo_permitido() and self.__disponible:
            self.__cambiar_el_estado_dispo(False)
            print(f"{self.get_tipo_material()} '{self._titulo}' ha sido prestado.")
            return True
        elif not self.__disponible:
            print(f"{self.get_tipo_material()} '{self._titulo}' ya está prestado.")
            return False
        else:
            print(f"{self.get_tipo_material()} '{self._titulo}' es solo de consulta en sala y no se puede prestar.")
            return False

    def devolver(self) -> bool:
        """Marca el material como disponible nuevamente."""
        self.__cambiar_el_estado_dispo(True)
        print(f"- {self.get_tipo_material()} '{self._titulo}' ha sido devuelto.")
        return True


class Publicacion(Material):
    """Clase abstracta intermedia para materiales publicados editorialmente."""

    def __init__(self, titulo: str, codigo_id: int, año_publicacion: int, editorial: str):
        super().__init__(titulo, codigo_id)
        self.año_publicacion = año_publicacion  # Usa el setter para validar desde la creación
        self.editorial = editorial

    @property
    def año_publicacion(self) -> int:
        return self._año_publicacion

    @año_publicacion.setter
    def año_publicacion(self, año: int):
        if int(año) > datetime.now().year:
            raise ValueError("El año de publicación no puede ser un año futuro.")
        self._año_publicacion = int(año)

    def set_anio_publicacion(self, año: int):
        self.año_publicacion = año

    @property
    def editorial(self) -> str:
        return self._editorial

    @editorial.setter
    def editorial(self, nueva_editorial: str):
        if not nueva_editorial or not str(nueva_editorial).strip():
            raise ValueError("La editorial no puede estar vacía.")
        self._editorial = str(nueva_editorial).strip()

    def mostrar_info(self) -> str:
        base = super().mostrar_info()
        return f"{base} | Editorial: {self._editorial} ({self._año_publicacion})"


class ObraLiteraria(Publicacion):
    """Clase para obras con autor que permiten préstamo por defecto."""

    def __init__(self, titulo: str, codigo_id: int, año_publicacion: int, editorial: str, autor: str):
        super().__init__(titulo, codigo_id, año_publicacion, editorial)
        self.autor = autor

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, nuevo_autor: str):
        if not nuevo_autor or not str(nuevo_autor).strip():
            raise ValueError("El autor no puede estar vacío.")
        self._autor = str(nuevo_autor).strip()

    def es_prestamo_permitido(self) -> bool:
        return True

    def mostrar_info(self) -> str:
        base = super().mostrar_info()
        return f"{base} | Autor: {self._autor}"


class Libro(ObraLiteraria):
    """Clase concreta que representa un libro estándar."""

    def __init__(self, titulo: str, codigo_id: int, año_publicacion: int, editorial: str, autor: str, numero_paginas: int, isbn: str):
        super().__init__(titulo, codigo_id, año_publicacion, editorial, autor)
        self.numero_paginas = numero_paginas  # Usa el setter para validar > 0 desde el inicio
        self._isbn = str(isbn).strip()

    def get_tipo_material(self) -> str:
        return "Libro"

    @property
    def numero_paginas(self) -> int:
        return self._numero_paginas

    @numero_paginas.setter
    def numero_paginas(self, numero_paginas: int):
        if int(numero_paginas) <= 0:
            raise ValueError("El número de páginas debe ser un valor positivo mayor a 0.")
        self._numero_paginas = int(numero_paginas)

    def set_num_paginas(self, numero_paginas: int):
        self.numero_paginas = numero_paginas

    @property
    def isbn(self) -> str:
        return self._isbn

    def mostrar_info(self) -> str:
        base = super().mostrar_info()
        return f"{base} | Páginas: {self._numero_paginas} | ISBN: {self._isbn}"


class LibroTexto(Libro):
    """Subclase de Libro asociada a un curso académico."""

    def __init__(self, titulo: str, codigo_id: int, año_publicacion: int, editorial: str, autor: str, numero_paginas: int, isbn: str, curso_asociado: str):
        super().__init__(titulo, codigo_id, año_publicacion, editorial, autor, numero_paginas, isbn)
        self.curso_asociado = curso_asociado

    def get_tipo_material(self) -> str:
        return "Libro de Texto"

    @property
    def curso_asociado(self) -> str:
        return self._curso_asociado

    @curso_asociado.setter
    def curso_asociado(self, nuevo_curso: str):
        self._curso_asociado = str(nuevo_curso).strip()

    def mostrar_info(self) -> str:
        base = super().mostrar_info()
        return f"{base} | Curso: {self._curso_asociado}"


class RevistaCientifica(Publicacion):
    """Material de solo consulta en sala (demuestra polimorfismo con es_prestamo_permitido = False)."""

    def __init__(self, titulo: str, codigo_id: int, año_publicacion: int, editorial: str, issn: str):
        super().__init__(titulo, codigo_id, año_publicacion, editorial)
        self._issn = str(issn).strip()

    def get_tipo_material(self) -> str:
        return "Revista Científica"

    def es_prestamo_permitido(self) -> bool:
        return False

    @property
    def issn(self) -> str:
        return self._issn


# Alias para mantener compatibilidad exacta con nombres anteriores
publicacion = Publicacion
Obra_literaria = ObraLiteraria
libro = Libro
Libro_texto = LibroTexto
        
    
    
    
    
        
        
    
    
        