from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# -----------------------------
# CONEXION
# -----------------------------

uri = "mongodb+srv://amb231140_db_user:Z38UiHe08aFoPuDa@proyecto01.9kgjqy1.mongodb.net/"

client = MongoClient(uri)

db = client["restaurantes_db"]

# -----------------------------
# FUNCIONES DE VALIDACION
# -----------------------------

def validar_sn(mensaje):

    while True:

        valor = input(mensaje).lower()

        if valor in ["s", "n"]:
            return valor

        print("Error: solo se permite 's' o 'n'")


def validar_rol():

    while True:

        rol = input("Rol (cliente/admin): ").lower()

        if rol in ["cliente", "admin"]:
            return rol

        print("Error: solo se permite 'cliente' o 'admin'")


def validar_bool(mensaje):

    while True:

        valor = input(mensaje).lower()

        if valor == "true":
            return True

        if valor == "false":
            return False

        print("Error: escriba 'true' o 'false'")


def validar_menu(opciones):

    while True:

        op = input("Seleccione: ")

        if op in opciones:
            return op

        print("Opcion invalida")


# -----------------------------
# MOSTRAR DOCUMENTOS
# -----------------------------

def mostrar_documento(doc):

    print("\n---------------------------")

    for clave, valor in doc.items():

        if clave == "_id":
            valor = str(valor)

        if isinstance(valor, dict):

            print(f"{clave}:")

            for subclave, subvalor in valor.items():
                print(f"   {subclave}: {subvalor}")

        else:
            print(f"{clave}: {valor}")

    print("---------------------------")


# -----------------------------
# CREAR DOCUMENTOS
# -----------------------------

def crear_documento(col, nombre_col):

    if nombre_col == "usuarios":

        nombre = input("Nombre: ")
        email = input("Email: ")
        password = input("Password: ")
        telefono = input("Telefono: ")

        rol = validar_rol()

        calle = input("Calle: ")
        ciudad = input("Ciudad: ")
        referencia = input("Referencia: ")

        doc = {
            "nombre": nombre,
            "email": email,
            "password": password,
            "telefono": telefono,
            "direccion": {
                "calle": calle,
                "ciudad": ciudad,
                "referencia": referencia
            },
            "fecha_registro": datetime.now(),
            "rol": rol
        }

    elif nombre_col == "restaurantes":

        nombre = input("Nombre: ")
        descripcion = input("Descripcion: ")

        categorias = input("Categorias separadas por coma: ").split(",")

        lat = float(input("Latitud: "))
        lon = float(input("Longitud: "))

        rating = float(input("Rating promedio: "))

        activo = validar_bool("Activo (true/false): ")

        doc = {
            "nombre": nombre,
            "descripcion": descripcion,
            "categorias": categorias,
            "ubicacion": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "rating_promedio": rating,
            "activo": activo,
            "fecha_creacion": datetime.now()
        }

    elif nombre_col == "articulos_menu":

        restaurante_id = input("ID restaurante: ")

        nombre = input("Nombre articulo: ")
        descripcion = input("Descripcion: ")
        precio = float(input("Precio: "))
        categoria = input("Categoria: ")

        disponible = validar_bool("Disponible (true/false): ")

        doc = {
            "restaurante_id": ObjectId(restaurante_id),
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "categoria": categoria,
            "disponible": disponible
        }

    elif nombre_col == "ordenes":

        usuario_id = input("ID usuario: ")
        restaurante_id = input("ID restaurante: ")

        articulo_id = input("ID articulo: ")
        cantidad = int(input("Cantidad: "))
        precio_unitario = float(input("Precio unitario: "))

        subtotal = cantidad * precio_unitario

        estado = input("Estado: ")
        metodo_pago = input("Metodo pago: ")

        doc = {
            "usuario_id": ObjectId(usuario_id),
            "restaurante_id": ObjectId(restaurante_id),
            "items": [{
                "articulo_id": ObjectId(articulo_id),
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": subtotal
            }],
            "total": subtotal,
            "estado": estado,
            "metodo_pago": metodo_pago,
            "fecha": datetime.now()
        }

    elif nombre_col == "resenas":

        usuario_id = input("ID usuario: ")
        restaurante_id = input("ID restaurante: ")

        rating = int(input("Rating (1-5): "))
        comentario = input("Comentario: ")

        doc = {
            "usuario_id": ObjectId(usuario_id),
            "restaurante_id": ObjectId(restaurante_id),
            "rating": rating,
            "comentario": comentario,
            "fecha": datetime.now()
        }

    resultado = col.insert_one(doc)

    print("Documento creado con ID:", resultado.inserted_id)


# -----------------------------
# LEER DOCUMENTOS
# -----------------------------

def leer_documentos(col):

    print("\n===== BUSCAR DOCUMENTOS =====")

    filtro = {}

    usar_filtro = validar_sn("¿Desea usar filtro? (s/n): ")

    if usar_filtro == "s":

        campo = input("Campo: ")
        valor = input("Valor: ")

        filtro = {campo: valor}

    proyeccion = None

    usar_proyeccion = validar_sn("¿Usar proyeccion? (s/n): ")

    if usar_proyeccion == "s":

        campos = input("Campos separados por coma: ")

        lista = campos.split(",")

        proyeccion = {}

        for campo in lista:
            proyeccion[campo.strip()] = 1

    campo_orden = None
    tipo = None

    usar_sort = validar_sn("¿Ordenar resultados? (s/n): ")

    if usar_sort == "s":

        campo_orden = input("Campo ordenar: ")

        print("1 Ascendente")
        print("2 Descendente")

        op = validar_menu(["1", "2"])

        if op == "1":
            tipo = 1
        else:
            tipo = -1

    skip = 0

    usar_skip = validar_sn("¿Usar skip? (s/n): ")

    if usar_skip == "s":
        skip = int(input("Cantidad a saltar: "))

    limit = 0

    usar_limit = validar_sn("¿Usar limit? (s/n): ")

    if usar_limit == "s":
        limit = int(input("Cantidad maxima: "))

    cursor = col.find(filtro, proyeccion)

    if campo_orden:
        cursor = cursor.sort(campo_orden, tipo)

    if skip:
        cursor = cursor.skip(skip)

    if limit:
        cursor = cursor.limit(limit)

    for doc in cursor:
        mostrar_documento(doc)


# -----------------------------
# ACTUALIZAR
# -----------------------------

def actualizar_documento(col):

    id_doc = input("ID documento: ")

    campo = input("Campo a actualizar: ")
    valor = input("Nuevo valor: ")

    resultado = col.update_one(
        {"_id": ObjectId(id_doc)},
        {"$set": {campo: valor}}
    )

    print("Documentos modificados:", resultado.modified_count)


# -----------------------------
# ELIMINAR
# -----------------------------

def eliminar_documento(col):

    id_doc = input("ID documento: ")

    resultado = col.delete_one({
        "_id": ObjectId(id_doc)
    })

    print("Documentos eliminados:", resultado.deleted_count)


# -----------------------------
# REPORTES (AGGREGATION)
# -----------------------------

#MEJORES RESTAURANTES
def mejores_restaurantes():

    pipeline = [
        {
            "$group": {
                "_id": "$restaurante_id",
                "promedio_rating": {"$avg": "$rating"},
                "total_resenas": {"$sum": 1}
            }
        },
        {"$sort": {"promedio_rating": -1}}
    ]

    resultados = db.resenas.aggregate(pipeline)

    print("\n--- Restaurantes mejor calificados ---\n")

    for r in resultados:
        print(r)

#ARTICULOS MAS VENDIDOS
def articulos_mas_vendidos():

    pipeline = [
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": "$items.articulo_id",
                "total_vendidos": {"$sum": "$items.cantidad"}
            }
        },
        {"$sort": {"total_vendidos": -1}}
    ]

    resultados = db.ordenes.aggregate(pipeline)

    print("\n--- Articulos mas vendidos ---\n")

    for r in resultados:
        print(r)

#VENTAS POR RESTAURANTE        
def ventas_por_restaurante():

    pipeline = [
        {
            "$group": {
                "_id": "$restaurante_id",
                "total_ventas": {"$sum": "$total"},
                "ordenes": {"$sum": 1}
            }
        },
        {"$sort": {"total_ventas": -1}}
    ]

    resultados = db.ordenes.aggregate(pipeline)

    print("\n--- Ventas por restaurante ---\n")

    for r in resultados:
        print(r) 

#RESEÑAS CON NOMBRE DE RESTAURANTE
def resenas_con_restaurantes():

    pipeline = [
        {
            "$lookup": {
                "from": "restaurantes",
                "localField": "restaurante_id",
                "foreignField": "_id",
                "as": "restaurante"
            }
        },
        {"$unwind": "$restaurante"},
        {
            "$project": {
                "rating": 1,
                "comentario": 1,
                "restaurante": "$restaurante.nombre"
            }
        }
    ]

    resultados = db.resenas.aggregate(pipeline)

    print("\n--- Reseñas con restaurante ---\n")

    for r in resultados:
        print(r)

# -----------------------------
# MENU REPORTES
# -----------------------------

def menu_reportes():

    while True:

        print("\n--- REPORTES ---")
        print("1 Restaurantes mejor calificados")
        print("2 Articulos mas vendidos")
        print("3 Ventas por restaurante")
        print("4 Reseñas con restaurante")
        print("0 Volver")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            mejores_restaurantes()

        elif opcion == "2":
            articulos_mas_vendidos()

        elif opcion == "3":
            ventas_por_restaurante()

        elif opcion == "4":
            resenas_con_restaurantes()

        elif opcion == "0":
            break
        
# -----------------------------
# MENU CRUD
# -----------------------------

def menu_crud(nombre_col):

    col = db[nombre_col]
while True:

        print("\n===== MENU =====")
        print("1 Crear documento")
        print("2 Leer documentos")
        print("3 Actualizar documento")
        print("4 Eliminar documento")
        print("5 Reportes")
        print("0 Salir")

        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            crear_documento()

        elif opcion == "2":
            leer_documentos()

        elif opcion == "3":
            actualizar_documento()

        elif opcion == "4":
            eliminar_documento()

        elif opcion == "5":
            menu_reportes()

        elif opcion == "0":
            break

        else:
            print("Opcion invalida")


# -----------------------------
# MENU PRINCIPAL
# -----------------------------

def menu_principal():

    while True:

        print("\n===== MENU PRINCIPAL =====")

        print("1 Usuarios")
        print("2 Restaurantes")
        print("3 Articulos Menu")
        print("4 Ordenes")
        print("5 Resenas")
        print("6 Salir")

        opcion = validar_menu(["1", "2", "3", "4", "5", "6"])

        if opcion == "6":
            break

        colecciones = {
            "1": "usuarios",
            "2": "restaurantes",
            "3": "articulos_menu",
            "4": "ordenes",
            "5": "resenas"
        }

        menu_crud(colecciones[opcion])


menu_principal()