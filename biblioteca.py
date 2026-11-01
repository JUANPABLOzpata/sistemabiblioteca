from materiales import Material, Libro, LibroTexto
from personas import Persona, Estudiante, Profesor
from conexion import conectar


class SistemaBiblioteca:
    """Gestiona el catálogo de materiales, usuarios y préstamos sincronizando POO y MySQL."""

    def __init__(self):
        # Catálogos en memoria para mantener sincronizados los objetos de POO con la BD
        self._catalogo_materiales: dict[int, Material] = {}
        self._usuarios_registrados: dict[str, Persona] = {}

    def registrar_material(self, material: Material):
        """Registra cualquier subclase de Material en memoria y en la base de datos."""
        self._catalogo_materiales[material.codigo_id] = material

        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # Usamos propiedades públicas y getattr seguro para soportar polimorfismo
            autor = getattr(material, "autor", None)
            editorial = getattr(material, "editorial", None)
            año_publicacion = getattr(material, "año_publicacion", None)
            numero_paginas = getattr(material, "numero_paginas", None)
            isbn = getattr(material, "isbn", getattr(material, "issn", None))

            cursor.execute(
                """
                INSERT INTO materiales 
                (id, titulo, tipo, disponible, autor, editorial, año_publicacion, numero_paginas, isbn)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    titulo = VALUES(titulo),
                    tipo = VALUES(tipo),
                    disponible = VALUES(disponible),
                    autor = VALUES(autor),
                    editorial = VALUES(editorial),
                    año_publicacion = VALUES(año_publicacion),
                    numero_paginas = VALUES(numero_paginas),
                    isbn = VALUES(isbn)
                """,
                (
                    material.codigo_id,
                    material.titulo,
                    material.get_tipo_material(),
                    material.disponible,
                    autor,
                    editorial,
                    año_publicacion,
                    numero_paginas,
                    isbn,
                ),
            )
            conexion.commit()
            print(f"Material '{material.titulo}' (ID: {material.codigo_id}) registrado en la BD.")

        except Exception as e:
            print(f"Aviso BD al registrar material '{material.titulo}': {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def registrar_material_libro(self, libro: Material):
        """Alias para registrar un libro manteniendo compatibilidad."""
        return self.registrar_material(libro)

    def registrar_usuario(self, usuario: Persona):
        """Registra un usuario (Estudiante o Profesor) en memoria y en la base de datos."""
        self._usuarios_registrados[usuario.identificacion] = usuario

        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            extra = getattr(usuario, "carrera", getattr(usuario, "departamento", None))

            cursor.execute(
                """
                INSERT INTO usuarios (identificacion, nombre, tipo, extra)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    nombre = VALUES(nombre),
                    tipo = VALUES(tipo),
                    extra = VALUES(extra)
                """,
                (
                    usuario.identificacion,
                    usuario.nombre,
                    usuario.get_tipo_usuario(),
                    extra,
                ),
            )
            conexion.commit()
            print(f"Usuario '{usuario.nombre}' (ID: {usuario.identificacion}) registrado en la BD.")

        except Exception as e:
            print(f"Aviso BD al registrar usuario '{usuario.nombre}': {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

    def prestar_material(self, id_material: int, id_usuario: str) -> bool:
        """Valida reglas de negocio en POO y registra el préstamo en la base de datos."""
        material = self._catalogo_materiales.get(int(id_material))
        usuario = self._usuarios_registrados.get(str(id_usuario))

        # 1. Validaciones en objetos de memoria (si están cargados en la sesión)
        if material is not None:
            if not material.es_prestamo_permitido():
                print(f"Error: '{material.titulo}' ({material.get_tipo_material()}) es solo de consulta en sala.")
                return False
            if not material.disponible:
                print(f"Error: El material '{material.titulo}' (ID: {id_material}) ya se encuentra prestado.")
                return False

        if usuario is not None and not usuario.puede_prestar():
            print(
                f"Error: El usuario '{usuario.nombre}' alcanzó su límite máximo de "
                f"{usuario.get_max_prestamos()} préstamos."
            )
            return False

        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # Verificar disponibilidad en BD si no estaba en memoria
            cursor.execute("SELECT disponible, titulo FROM materiales WHERE id = %s", (id_material,))
            fila_mat = cursor.fetchone()
            if not fila_mat:
                print(f"Error: El material con ID {id_material} no existe en la BD.")
                return False
            if not fila_mat[0]:
                print(f"Error: El material '{fila_mat[1]}' (ID: {id_material}) no está disponible en la BD.")
                return False

            # Verificar existencia del usuario en BD
            cursor.execute("SELECT nombre FROM usuarios WHERE identificacion = %s", (id_usuario,))
            if not cursor.fetchone():
                print(f"Error: El usuario con ID {id_usuario} no existe en la BD.")
                return False

            # Actualizar disponibilidad y registrar préstamo
            cursor.execute("UPDATE materiales SET disponible = FALSE WHERE id = %s", (id_material,))
            cursor.execute(
                """
                INSERT INTO prestamos (id_material, id_usuario, fecha)
                VALUES (%s, %s, CURDATE())
                """,
                (id_material, id_usuario),
            )
            conexion.commit()

        except Exception as e:
            print(f"Aviso BD al prestar: {e}")
            if material is None or usuario is None:
                return False

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

        # 2. Sincronizar estado de objetos en memoria y disparar notificación privada
        if material is not None:
            material.prestar()
        if usuario is not None and material is not None:
            usuario.agregar_prestamo(material)
            self.__notificar_prestamo(usuario, material)

        print("Préstamo registrado exitosamente.")
        return True

    def devolver_material(self, id_material: int, id_usuario: str) -> bool:
        """Procesa la devolución de un material en la BD y actualiza los objetos en memoria."""
        material = self._catalogo_materiales.get(int(id_material))
        usuario = self._usuarios_registrados.get(str(id_usuario))

        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id FROM prestamos 
                WHERE id_material = %s AND id_usuario = %s
                """,
                (id_material, id_usuario),
            )
            prestamo = cursor.fetchall()

            if not prestamo:
                print(f"Error: No se encontró préstamo activo del material {id_material} para el usuario {id_usuario}.")
                return False

            cursor.execute(
                """
                DELETE FROM prestamos 
                WHERE id_material = %s AND id_usuario = %s
                """,
                (id_material, id_usuario),
            )
            cursor.execute(
                """
                UPDATE materiales SET disponible = TRUE 
                WHERE id = %s
                """,
                (id_material,),
            )
            conexion.commit()

        except Exception as e:
            print(f"Aviso BD al devolver: {e}")

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()

        # Sincronizar objetos en memoria
        if material is not None:
            material.devolver()
        if usuario is not None and material is not None:
            usuario.remover_prestamo(material)

        print(f"Devolución exitosa del material {id_material} por usuario {id_usuario}.")
        return True

    def __notificar_prestamo(self, usuario: Persona, material: Material):
        """Método privado (encapsulamiento) para registrar notificación interna."""
        print(
            f"[Notificación Interna]: Préstamo de '{material.titulo}' "
            f"(ID {material.codigo_id}) asignado a {usuario.nombre} ({usuario.identificacion})."
        )

    def buscar_material(self, criterio):
        """Búsqueda polimórfica por ID numérico o coincidencia parcial en el título."""
        conexion = None
        cursor = None
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            # 1. Intentar búsqueda exacta por ID si el criterio es un entero
            if isinstance(criterio, int) or (isinstance(criterio, str) and criterio.isdigit()):
                codigo_id = int(criterio)
                cursor.execute("SELECT * FROM materiales WHERE id = %s", (codigo_id,))
                resultado = cursor.fetchone()
                if resultado:
                    print(f"\n--- Búsqueda por ID {codigo_id} exitosa ---")
                    print(
                        f"Título: {resultado[1]} | ID: {resultado[0]} | "
                        f"Estado: {'disponible' if resultado[3] else 'prestado'}"
                    )
                    return resultado

            # 2. Búsqueda por título
            titulo_buscado = str(criterio).lower()
            print(f"\n--- Buscando por Título que contenga: '{titulo_buscado}' ---")
            cursor.execute("SELECT * FROM materiales WHERE LOWER(titulo) LIKE %s", (f"%{titulo_buscado}%",))
            resultado = cursor.fetchone()
            if resultado:
                print("¡Material encontrado!")
                print(
                    f"Título: {resultado[1]} | ID: {resultado[0]} | "
                    f"Estado: {'disponible' if resultado[3] else 'prestado'}"
                )
                return resultado

            print(f"Material con criterio '{criterio}' no encontrado.")
            return None

        except Exception as e:
            print(f"Aviso BD al buscar ({e}). Buscando en catálogo en memoria...")
            # Respaldo de búsqueda en memoria si la BD no está activa
            if isinstance(criterio, int) or (isinstance(criterio, str) and criterio.isdigit()):
                mat = self._catalogo_materiales.get(int(criterio))
                if mat:
                    print(f"\n--- Búsqueda en memoria por ID {criterio} exitosa ---")
                    print(mat.mostrar_info())
                    return mat
            titulo_buscado = str(criterio).lower()
            for mat in self._catalogo_materiales.values():
                if titulo_buscado in mat.titulo.lower():
                    print(f"\n--- Búsqueda en memoria por Título '{criterio}' exitosa ---")
                    print(mat.mostrar_info())
                    return mat
            print(f"Material con criterio '{criterio}' no encontrado.")
            return None

        finally:
            if cursor:
                cursor.close()
            if conexion and conexion.is_connected():
                conexion.close()