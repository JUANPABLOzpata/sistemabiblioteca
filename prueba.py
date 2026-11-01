# CASOS DE PRUEBA (Uso y Demostración del Sistema de Biblioteca)

from materiales import Libro, LibroTexto, RevistaCientifica
from personas import Estudiante, Profesor
from biblioteca import SistemaBiblioteca


def ejecutar_pruebas():
    biblioteca = SistemaBiblioteca()
    print("=" * 60)
    print(" SISTEMA DE GESTIÓN DE BIBLIOTECA (POO + MySQL)")
    print("=" * 60)

    # 1. PRUEBA DE HERENCIA Y CLASES ABSTRACTAS
    print("\n" + "=" * 60)
    print(" 1. DEMOSTRACIÓN DE HERENCIA Y SOBRESCRITURA")
    print("=" * 60)

    libro_poo = LibroTexto(
        titulo="Programación Orientada a Objetos",
        codigo_id=1001,
        año_publicacion=2024,
        editorial="JUANPISFI",
        autor="J. Pérez",
        numero_paginas=450,
        isbn="978-0123456789",
        curso_asociado="Programación IV",
    )

    libro_novela = Libro(
        titulo="Cien años de soledad",
        codigo_id=1002,
        año_publicacion=1967,
        editorial="Sudamericana",
        autor="G. García Márquez",
        numero_paginas=400,
        isbn="978-0000000001",
    )

    revista_ia = RevistaCientifica(
        titulo="IEEE Transactions on AI",
        codigo_id=1003,
        año_publicacion=2025,
        editorial="IEEE",
        issn="1234-5678",
    )

    biblioteca.registrar_material_libro(libro_poo)
    biblioteca.registrar_material_libro(libro_novela)
    biblioteca.registrar_material(revista_ia)

    print("\n-> Resultado de Herencia y Sobrescritura de mostrar_info():")
    print(libro_poo.mostrar_info())
    print(libro_novela.mostrar_info())
    print(revista_ia.mostrar_info())
    print(f"Tipo: {libro_poo.get_tipo_material()} | ¿Es prestable?: {libro_poo.es_prestamo_permitido()}")
    print(f"Tipo: {revista_ia.get_tipo_material()} | ¿Es prestable?: {revista_ia.es_prestamo_permitido()}")

    # 2. PRUEBA DE POLIMORFISMO Y SOBRECARGA SIMULADA
    print("\n" + "=" * 60)
    print(" 2. DEMOSTRACIÓN DE POLIMORFISMO EN BÚSQUEDA")
    print("=" * 60)

    biblioteca.buscar_material(1001)       # Búsqueda por ID (int)
    biblioteca.buscar_material("Objetos")  # Búsqueda por Título (str)

    # 3. PRUEBA DE ENCAPSULAMIENTO Y VALIDACIONES
    print("\n" + "=" * 60)
    print(" 3. DEMOSTRACIÓN DE ENCAPSULAMIENTO Y VALIDACIONES")
    print("=" * 60)

    est_juan = Estudiante(nombre="Juan Pérez", identificacion="1234567890", carrera="Sistemas")
    biblioteca.registrar_usuario(est_juan)

    print("\n-> Validación 1: Intentar cambiar a año futuro (2030)...")
    try:
        libro_poo.set_anio_publicacion(2030)
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    print("\n-> Validación 2: Intentar cambiar páginas a 0...")
    try:
        libro_novela.set_num_paginas(0)
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    print("\n-> Validación 3: Intentar cambiar ID a un valor corto ('123')...")
    try:
        est_juan.set_identificacion("123")
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    # 4. PRUEBA DE POLIMORFISMO EN PRÉSTAMOS Y DEVOLUCIONES
    print("\n" + "=" * 60)
    print(" 4. DEMOSTRACIÓN DE PRÉSTAMOS, REGLAS Y DEVOLUCIONES")
    print("=" * 60)

    prof_ana = Profesor(nombre="Ana Gómez", identificacion="1122334455", departamento="Ingeniería")
    biblioteca.registrar_usuario(prof_ana)

    print("\n-> Préstamo 1: Libro a Estudiante (Juan Pérez)")
    biblioteca.prestar_material(1002, "1234567890")

    print("\n-> Préstamo 2: Libro de Texto a Profesor (Ana Gómez)")
    biblioteca.prestar_material(1001, "1122334455")

    print("\n-> Intento de préstamo de material de solo consulta (Revista Científica):")
    biblioteca.prestar_material(1003, "1234567890")

    print("\n--- Estado Actual de Préstamos en Memoria ---")
    print(f"Juan Pérez (Estudiante) tiene prestados: {[m.titulo for m in est_juan.materiales_prestados]}")
    print(f"Ana Gómez (Profesor) tiene prestados: {[m.titulo for m in prof_ana.materiales_prestados]}")

    print("\n-> Devolución de material (Libro 1002 por Juan Pérez)")
    biblioteca.devolver_material(1002, "1234567890")
    print(f"Juan Pérez ahora tiene prestados: {[m.titulo for m in est_juan.materiales_prestados]}")


if __name__ == "__main__":
    ejecutar_pruebas()