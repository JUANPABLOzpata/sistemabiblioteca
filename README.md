# Sistema de Gestión de Biblioteca en Python (POO + MySQL)

Aplicación desarrollada en **Python** que implementa los cuatro pilares de la **Programación Orientada a Objetos (POO)** integrados con persistencia relacional en **MySQL**, acompañada de un simulador web interactivo 100% responsivo.

## Características y Arquitectura POO

| Pilar POO | Implementación en el Proyecto |
| :--- | :--- |
| **Abstracción** | Clases base abstractas (`Material` y `Persona` mediante `abc.ABC` y `@abstractmethod`) que definen contratos estrictos para todas las subclases. |
| **Herencia Multinivel** | Jerarquía `Material` → `Publicacion` → `ObraLiteraria` → `Libro` → `LibroTexto`, además de `RevistaCientifica`, y `Persona` → `Estudiante` / `Profesor`. |
| **Encapsulamiento** | Atributos protegidos (`_titulo`, `_codigo_id`) y privados (`__disponible`, `__materiales_prestados`), métodos privados (`__cambiar_el_estado_dispo`, `__notificar_prestamo`) y validaciones en `@property.setter` (año no futuro, páginas positivas, identificación de 10 dígitos). |
| **Polimorfismo** | Sobrescritura de `mostrar_info()`, `get_tipo_material()`, `es_prestamo_permitido()` y `get_max_prestamos()`, junto con búsqueda flexible (`buscar_material`) por ID numérico o por título. |

## Estructura del Proyecto

```text
├── biblioteca.py       # Controlador principal (lógica de negocio y persistencia MySQL)
├── conexion.py         # Gestión de conexión a MySQL mediante variables de entorno (.env)
├── materiales.py       # Jerarquía de clases de materiales y validaciones de dominio
├── personas.py         # Jerarquía de usuarios (Estudiante, Profesor) y control de cupos
├── prueba.py           # Suite de demostración de casos de uso y validaciones
├── schema.sql          # Script SQL para crear la base de datos y las tablas
├── index.html          # Simulador web interactivo (Desktop / Tablet / Móvil)
└── requirements.txt    # Dependencias del proyecto
```

## Requisitos Previos

- **Python** 3.10 o superior
- **MySQL Server** 8.0 o superior

## Instalación y Ejecución Paso a Paso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/TU_REPOSITORIO.git](https://github.com/TU_USUARIO/TU_REPOSITORIO.git)
   cd TU_REPOSITORIO
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar la base de datos MySQL:**
   Ejecuta el archivo `schema.sql` en tu servidor MySQL:
   ```bash
   mysql -u root -p < schema.sql
   ```

4. **Configurar las variables de entorno (`.env`):**
   Crea un archivo `.env` en la raíz del proyecto con tus credenciales:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=tu_contraseña
   DB_NAME=biblioteca_db
   ```

5. **Ejecutar las pruebas de demostración:**
   ```bash
   python prueba.py
   ```