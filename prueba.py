
# CASOS DE PRUEBA (Uso y Demostración)

# Importar todas las clases necesarias
from materiales import libro, Libro_texto
from personas import Estudiante, Profesor
from biblioteca import SistemaBiblioteca

def ejecutar_pruebas():    
    bibloteca = SistemaBiblioteca()   #instancia del sistema(materales y usurarios)
    print("=" * 50)
    print(" SISTEMA DE BIBLIOTECA")
    print("=" * 50)
    
   
    # PRUEBA DE HERENCIA Y CLASES ABSTRACTAS
  
    print("\n" + "=" * 50)
    print(" 1. DEMOSTRACIÓN DE HERENCIA")
    print("=" * 50)
    #Libro_texto (hereda de Libro, ObraLiteraria, Publicacion, Material).
    
    libro_poo = Libro_texto(
        titulo="Programación Orientada a Objetos", 
        codigo_id=1001, 
        año_publicacion=2024, 
        editorial="JUANPISFI", 
        autor="J. Pérez", 
        numero_paginas=450, 
        isbn="978-0123456789", 
        curso_asociado="Programación IV"
    )

    #  Libro
    
    libro_novela = libro(
        titulo="Cien años de soledad", 
        codigo_id=1002, 
        año_publicacion=1967, 
        editorial="Sudamericana", 
        autor="G. García Márquez", 
        numero_paginas=400, 
        isbn="978-0000000001"
    )

    
    
    bibloteca.registrar_material_libro(libro_poo)
    bibloteca.registrar_material_libro(libro_novela)
   
    print("\n Resultado de Herencia y Sobrescritura ")
    # Demuestra reutilización y sobrescritura de mostrar_info()
    print(libro_poo.mostrar_info())
    # Demuestra el método abstracto get_tipo_material()
    print(f"Tipo: {libro_poo.get_tipo_material()}")
    print(f"¿Es prestable? {libro_poo.es_prestamo_permitido()}") #valida si el material puede prestarse


   
    #PRUEBA DE POLIMORFISMO Y SOBRECARGA
  
    print("\n" + "=" * 50)
    print("2. DEMOSTRACIÓN DE POLIMORFISMO Y SOBRECARGA")
    print("=" * 50)
    
    #Sobrecarga (simulada con métodos específicos):
    print("-> Sobrecarga de 'registrar_material':")
    
    
    # Polimorfismo en acción (buscar_material acepta ID o Título) en esta linea se hace mismo metodo distintos tipos
    bibloteca.buscar_material(1001) # Búsqueda por ID
    bibloteca.buscar_material("Objetos") # Búsqueda por Título 

    
    # 3. PRUEBA DE ENCAPSULAMIENTO Y VALIDACIONES
    
    print("\n" + "=" * 50)
    print("3. DEMOSTRACIÓN DE ENCAPSULAMIENTO Y VALIDACIONES")
    print("=" * 50)
    
    # creacion de un Usuario estudiante
    est_juan = Estudiante(nombre="Juan Pérez", identificacion="1234567890", carrera="Sistemas")
    bibloteca.registrar_usuario(est_juan)

    # VALIDACIÓN 1, Año de Publicación 
    print("\n Validación 1: Intentar cambiar a año futuro (2030)...")
    try:
        libro_poo.set_anio_publicacion(2030)
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    # VALIDACIÓN 2, Número de Páginas 
    print("\n Validación 2: Intentar cambiar páginas a 0...")
    try:
        libro_novela.set_num_paginas(0)
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    # VALIDACIÓN 3, Identificación 
    print("\n Validación 3: Intentar cambiar ID a un valor corto...")
    try:
        est_juan.set_identificacion("123")
    except ValueError as e:
        print(f"¡Excepción capturada!: {e}")

    
    # 4. PRUEBA DE POLIMORFISMO CON CLASE BASE
    
    print("\n" + "=" * 50)
    print("4. DEMOSTRACIÓN DE POLIMORFISMO EN PRESTAMOS")
    print("=" * 50)
    
    #creamos profesor 
    prof_ana = Profesor(nombre="Ana Gómez", identificacion="1122334455", departamento="Ingeniería")
    bibloteca.registrar_usuario(prof_ana)

    # Préstamo 1: Libro (prestables) a Estudiante (límite 5)
    print("\n-> Préstamo 1: Libro a Estudiante")
    bibloteca.prestar_material(1002, "1234567890") 

    # Préstamo 2: Libro_texto 
    print("\n-> Préstamo 2: Libro de Texto a Profesor")
    bibloteca.prestar_material(1001, "1122334455") 
    

    # mostramos el estado usando atributos protegidos
    print("\n--- Estado de Préstamos ---")
    print(f"Juan Pérez (Estudiante) tiene prestados: {[m.get_titulo for m in est_juan.materiales_prestados]}")
    print(f"Ana Gómez (Profesor) tiene prestados: {[m.get_titulo for m in prof_ana.materiales_prestados]}")

    # Devolución
    print("\n-> Devolución de material (Libro 1002 por Juan Pérez)")
    bibloteca.devolver_material(1002, "1234567890")

if __name__ == "__main__":
    ejecutar_pruebas()
    ejecutar_pruebas()