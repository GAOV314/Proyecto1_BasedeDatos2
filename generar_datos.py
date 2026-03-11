from pymongo import MongoClient
from bson.objectid import ObjectId
from faker import Faker
from datetime import datetime
import random

# Conexion con la base de datos
uri = "mongodb+srv://amb231140_db_user:Z38UiHe08aFoPuDa@proyecto01.9kgjqy1.mongodb.net/"
client = MongoClient(uri)
db = client["restaurantes_db"]

fake = Faker()


# Codigo para limpiar las colecciones

def limpiar_colecciones():
    db.usuarios.delete_many({})
    db.restaurantes.delete_many({})
    db.articulos_menu.delete_many({})
    db.ordenes.delete_many({})
    db.resenas.delete_many({})
    print("Colecciones limpiadas")


# Generador de usuarios
def generar_usuarios(n=10000):

    usuarios = []

    for _ in range(n):
        usuarios.append({
            "nombre": fake.name(),
            "email": fake.unique.email(),
            "password": "123456",
            "telefono": fake.phone_number(),
            "direccion": {
                "calle": fake.street_address(),
                "ciudad": fake.city(),
                "referencia": fake.word()
            },
            "fecha_registro": fake.date_time_this_decade(),
            "rol": random.choice(["cliente", "admin"])
        })

    db.usuarios.insert_many(usuarios)
    print(f"{n} usuarios insertados")

# Generador de restaurantes
def generar_restaurantes(n=2000):

    restaurantes = []

    categorias_base = ["italiana", "china", "mexicana", "peruana", "americana", "vegana"]

    for _ in range(n):
        lat = random.uniform(-12.2, -11.8)
        lon = random.uniform(-77.2, -76.8)

        restaurantes.append({
            "nombre": fake.company(),
            "descripcion": fake.text(max_nb_chars=100),
            "categorias": random.sample(categorias_base, k=random.randint(1,3)),
            "ubicacion": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "rating_promedio": round(random.uniform(1,5),2),
            "activo": random.choice([True, False]),
            "fecha_creacion": fake.date_time_this_decade()
        })

    db.restaurantes.insert_many(restaurantes)
    print(f"{n} restaurantes insertados")

# Generador de articulos
def generar_articulos(n=15000):

    restaurantes = list(db.restaurantes.find({}, {"_id": 1}))

    articulos = []

    for _ in range(n):
        restaurante = random.choice(restaurantes)["_id"]

        articulos.append({
            "restaurante_id": restaurante,
            "nombre": fake.word().capitalize(),
            "descripcion": fake.text(max_nb_chars=80),
            "precio": round(random.uniform(10,100),2),
            "categoria": random.choice(["entrada", "plato_fondo", "postre", "bebida"]),
            "disponible": random.choice([True, False])
        })

    db.articulos_menu.insert_many(articulos)
    print(f"{n} articulos insertados")

# Generador de ordenes
def generar_ordenes(n=50000):

    usuarios = list(db.usuarios.find({}, {"_id": 1}))
    restaurantes = list(db.restaurantes.find({}, {"_id": 1}))
    articulos = list(db.articulos_menu.find({}, {"_id": 1}))

    ordenes = []

    for _ in range(n):

        usuario_id = random.choice(usuarios)["_id"]
        restaurante_id = random.choice(restaurantes)["_id"]

        articulo_id = random.choice(articulos)["_id"]
        cantidad = random.randint(1,5)
        precio = round(random.uniform(10,100),2)

        subtotal = cantidad * precio

        ordenes.append({
            "usuario_id": usuario_id,
            "restaurante_id": restaurante_id,
            "items": [{
                "articulo_id": articulo_id,
                "cantidad": cantidad,
                "precio_unitario": precio,
                "subtotal": subtotal
            }],
            "total": subtotal,
            "estado": random.choice(["pendiente", "pagado", "enviado", "cancelado"]),
            "metodo_pago": random.choice(["tarjeta", "efectivo", "yape"]),
            "fecha": fake.date_time_this_year()
        })

    db.ordenes.insert_many(ordenes)
    print(f"{n} ordenes insertadas")

# Generador de reseñas
def generar_resenas(n=20000):

    usuarios = list(db.usuarios.find({}, {"_id": 1}))
    restaurantes = list(db.restaurantes.find({}, {"_id": 1}))

    resenas = []

    for _ in range(n):
        resenas.append({
            "usuario_id": random.choice(usuarios)["_id"],
            "restaurante_id": random.choice(restaurantes)["_id"],
            "rating": random.randint(1,5),
            "comentario": fake.sentence(),
            "fecha": fake.date_time_this_year()
        })

    db.resenas.insert_many(resenas)
    print(f"{n} reseñas insertadas")

# Main para ejecutar generación automática de
if __name__ == "__main__":

    print("Generando datos...")

    limpiar_colecciones()

    generar_usuarios()
    generar_restaurantes()
    generar_articulos()
    generar_ordenes()      # 50,000
    generar_resenas()

    print("Datos generados correctamente")