from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Empleados(db.Model):
    __tablename__ = "empleados"
    id=db.Column(db.Integer,primary_key=True)
    nombre=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    email=db.Column(db.String(50))
    sueldo=db.Column(db.String(50))
    created_date=db.Column(db.DateTime,default=datetime.datetime.now)


class Pizzas(db.Model):
    __tablename__ = "pizzas"
    id=db.Column(db.Integer,primary_key=True)
    nombreCliente=db.Column(db.String(50))
    direccion=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    fechaCompra=db.Column(db.String(50))
    tamanioPizza=db.Column(db.String(50))
    ingredientes=db.Column(db.String(50))
    cantidadPizzas=db.Column(db.String(50))
    total=db.Column(db.Float)
    diaSemana=db.Column(db.String(50))
    created_date=db.Column(db.DateTime,default=datetime.datetime.now)