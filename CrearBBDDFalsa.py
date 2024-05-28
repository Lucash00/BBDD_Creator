import os
import sqlite_utils
from faker import Faker
import random
from datetime import datetime

class BaseDeDatosFalsa:
    ROLES = ['usuario', 'asesor', 'developer', 'admin', 'marketing', 'manager']
    NUM_USUARIOS = 1000
    NUM_PRODUCTOS = 2000
    NUM_ASESORES = 100
    NUM_ADMIN = 2
    NUM_MARKETING = 20

    def __init__(self, nombre_archivo='BDFalsa.db'):
        self.nombre_archivo = nombre_archivo
        self.fake = Faker('es_ES')
        self.usuario_id_counter = 1
        self.producto_id_counter = 1
        self.venta_id_counter = 1
        self.pedido_id_counter = 1
        self.inventario_id_counter = 1
        self.chat_id_counter = 1
        self.mensaje_id_counter = 1
        self.notificacion_id_counter = 1
        self.comentario_id_counter = 1
        self.resena_id_counter = 1

    def crear_base_de_datos(self):
        if os.path.exists(self.nombre_archivo):
            os.remove(self.nombre_archivo)

        db = sqlite_utils.Database(self.nombre_archivo)
        self._crear_tablas(db)
        self._generar_roles(db)
        self._generar_usuarios(db)
        self._generar_productos(db)
        self._generar_inventario(db)
        self._generar_notificaciones(db)
        self._generar_chats(db)
        self._generar_mensajes(db)
        self._generar_comentarios(db)
        self._generar_reseñas(db)

    def _crear_tablas(self, db):
        db["roles"].create({
            "rol_id": int,
            "nombre": str,
            "descripcion": str
        }, pk="rol_id")

        db["usuarios"].create({
            "usuario_id": int,
            "nombre": str,
            "email": str,
            "telefono": str,
            "direccion": str,
            "ciudad": str,
            "codigo_postal": str,
            "es_proveedor": bool,
            "rol_id": int,
            "token_autenticacion": str,
            "fecha_creacion": datetime,
            "ultima_actividad": datetime,
            "activo": bool,
            "avatar": str,
            "fecha_nacimiento": datetime,
            "genero": str,
            "biografia": str
        }, pk="usuario_id", foreign_keys=[("rol_id", "roles", "rol_id")])

        db["productos"].create({
            "producto_id": int,
            "nombre": str,
            "descripcion": str,
            "categoria": str,
            "precio": float,
            "fecha_creacion": datetime,
            "fecha_modificacion": datetime,
            "proveedor_id": int,
            "imagen": str,
            "destacado": bool,
            "disponible": bool,
            "sku": str,
            "marca": str,
            "valoraciones": float
        }, pk="producto_id", foreign_keys=[("proveedor_id", "usuarios", "usuario_id")])

        db["ventas"].create({
            "venta_id": int,
            "producto_id": int,
            "cantidad": int,
            "precio_venta": float,
            "fecha_venta": datetime,
            "cliente_id": int,
            "metodo_pago": str,
            "direccion_facturacion": str
        }, pk="venta_id", foreign_keys=[("producto_id", "productos", "producto_id"), ("cliente_id", "usuarios", "usuario_id")])

        db["pedidos"].create({
            "pedido_id": int,
            "cliente_id": int,
            "fecha_pedido": datetime,
            "estado": str,
            "direccion_envio": str,
            "fecha_entrega_esperada": datetime,
            "monto_total": float
        }, pk="pedido_id", foreign_keys=[("cliente_id", "usuarios", "usuario_id")])

        db["inventario"].create({
            "inventario_id": int,
            "producto_id": int,
            "cantidad": int,
            "ubicacion": str,
            "fecha_llegada": datetime,
            "estado_producto": str
        }, pk="inventario_id", foreign_keys=[("producto_id", "productos", "producto_id")])

        db["chats"].create({
            "chat_id": int,
            "nombre": str
        }, pk="chat_id")

        db["mensajes"].create({
            "mensaje_id": int,
            "texto": str,
            "fecha_envio": datetime,
            "usuario_id": int,
            "chat_id": int,
            "leido": bool
        }, pk="mensaje_id", foreign_keys=[("usuario_id", "usuarios", "usuario_id"), ("chat_id", "chats", "chat_id")])

        db["notificaciones"].create({
            "notificacion_id": int,
            "tipo": str,
            "mensaje": str,
            "fecha_envio": datetime,
            "usuario_id": int,
            "estado": str,
            "origen": str
        }, pk="notificacion_id", foreign_keys=[("usuario_id", "usuarios", "usuario_id")])

        db["comentarios_productos"].create({
            "comentario_id": int,
            "producto_id": int,
            "usuario_id": int,
            "texto": str,
            "fecha_creacion": datetime,
            "me_gusta": int
        }, pk="comentario_id", foreign_keys=[("producto_id", "productos", "producto_id"), ("usuario_id", "usuarios", "usuario_id")])

        db["reseñas"].create({
            "reseña_id": int,
            "usuario_id": int,
            "asesor_o_proveedor_id": int,
            "texto": str,
            "puntuacion": int,
            "fecha_creacion": datetime
        }, pk="reseña_id", foreign_keys=[("usuario_id", "usuarios", "usuario_id"), ("asesor_o_proveedor_id", "usuarios", "usuario_id")])

    def _generar_roles(self, db):
        db["roles"].insert_all([{"nombre": rol, "descripcion": self.fake.sentence()} for rol in self.ROLES])

    def _generar_usuarios(self, db):
        usuarios = []
        for _ in range(self.NUM_USUARIOS):
            usuario = {
                "usuario_id": self.usuario_id_counter,
                "nombre": self.fake.name(),
                "email": self.fake.email(),
                "telefono": self.fake.phone_number(),
                "direccion": self.fake.address(),
                "ciudad": self.fake.city(),
                "codigo_postal": self.fake.postcode(),
                "es_proveedor": self.fake.boolean(chance_of_getting_true=50),
                "rol_id": random.randint(1, len(self.ROLES)),
                "token_autenticacion": self.fake.uuid4(),
                "fecha_creacion": datetime.now(),
                "ultima_actividad": datetime.now(),
                "activo": self.fake.boolean(chance_of_getting_true=90),
                "avatar": self.fake.image_url(),
                "fecha_nacimiento": self.fake.date_of_birth(),
                "genero": self.fake.random_element(["Masculino", "Femenino", "Otro"]),
                "biografia": self.fake.paragraph()
            }
            usuarios.append(usuario)
            self.usuario_id_counter += 1
        db["usuarios"].insert_all(usuarios)

    def _generar_productos(self, db):
        productos = []
        for _ in range(self.NUM_PRODUCTOS):
            producto = {
                "producto_id": self.producto_id_counter,
                "nombre": self.fake.word(),
                "descripcion": self.fake.sentence(),
                "categoria": self.fake.word(),
                "precio": self.fake.random_number(digits=4) / 100,
                "fecha_creacion": datetime.now(),
                "fecha_modificacion": datetime.now(),
                "proveedor_id": random.randint(1, 1000),
                "imagen": self.fake.image_url(width=640, height=480),
                "destacado": self.fake.boolean(chance_of_getting_true=10),
                "disponible": True,
                "sku": self.fake.uuid4(),
                "marca": self.fake.company(),
                "valoraciones": round(random.uniform(1, 5), 2)
            }
            productos.append(producto)
            self.producto_id_counter += 1
        db["productos"].insert_all(productos)

    def _generar_inventario(self, db):
        inventario = []
        for producto_id in range(1, self.NUM_PRODUCTOS + 1):
            cantidad = random.randint(1, 100)
            ubicacion = self.fake.random_element(["Almacén A", "Almacén B", "Almacén C"])
            fecha_llegada = datetime.now()
            disponible = cantidad > 0
            inventario.append({
                "inventario_id": self.inventario_id_counter,
                "producto_id": producto_id,
                "cantidad": cantidad,
                "ubicacion": ubicacion,
                "fecha_llegada": fecha_llegada,
                "estado_producto": "Buen estado"
            })
            db["productos"].update(producto_id, {"disponible": disponible})
            self.inventario_id_counter += 1
        db["inventario"].insert_all(inventario)

    def _generar_notificaciones(self, db):
        notificaciones = []
        tipos_notificaciones = ['mensaje', 'pedido', 'aplicacion', 'promocion']
        for _ in range(1000):
            notificacion = {
                "notificacion_id": self.notificacion_id_counter,
                "tipo": random.choice(tipos_notificaciones),
                "mensaje": self.fake.sentence(),
                "fecha_envio": datetime.now(),
                "usuario_id": random.randint(1, self.NUM_USUARIOS),
                "estado": random.choice(['leída', 'no leída']),
                "origen": self.fake.word()
            }
            notificaciones.append(notificacion)
            self.notificacion_id_counter += 1
        db["notificaciones"].insert_all(notificaciones)

    def _generar_chats(self, db):
        chats = []
        for _ in range(100):
            chat = {
                "chat_id": self.chat_id_counter,
                "nombre": self.fake.word()
            }
            chats.append(chat)
            self.chat_id_counter += 1
        db["chats"].insert_all(chats)

    def _generar_mensajes(self, db):
        mensajes = []
        for _ in range(1000):
            mensaje = {
                "mensaje_id": self.mensaje_id_counter,
                "texto": self.fake.sentence(),
                "fecha_envio": datetime.now(),
                "usuario_id": random.randint(1, self.NUM_USUARIOS),
                "chat_id": random.randint(1, 100),
                "leido": True
            }
            mensajes.append(mensaje)
            self.mensaje_id_counter += 1
        db["mensajes"].insert_all(mensajes)

    def _generar_comentarios(self, db):
        comentarios = []
        for _ in range(300):
            comentario = {
                "comentario_id": self.comentario_id_counter,
                "producto_id": random.randint(1, self.NUM_PRODUCTOS),
                "usuario_id": random.randint(1, self.NUM_USUARIOS),
                "texto": self.fake.paragraph(),
                "fecha_creacion": datetime.now(),
                "me_gusta": 0
            }
            comentarios.append(comentario)
            self.comentario_id_counter += 1
        db["comentarios_productos"].insert_all(comentarios)

    def _generar_reseñas(self, db):
        reseñas = []
        for _ in range(200):
            reseña = {
                "reseña_id": self.resena_id_counter,
                "usuario_id": random.randint(1, self.NUM_USUARIOS),
                "asesor_o_proveedor_id": random.randint(1, self.NUM_USUARIOS),
                "texto": self.fake.paragraph(),
                "puntuacion": random.randint(1, 5),
                "fecha_creacion": datetime.now()
            }
            reseñas.append(reseña)
            self.resena_id_counter += 1
        db["reseñas"].insert_all(reseñas)

if __name__ == "__main__":
    base_de_datos = BaseDeDatosFalsa()
    base_de_datos.crear_base_de_datos()
    print("Base de datos falsa creada con éxito.")
