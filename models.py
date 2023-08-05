import funciones
from db import Base,session
from sqlalchemy import Column, Integer,String

import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL,'es-ES')
date=datetime.now()
fecha_pedido=date.strftime("%d-%m-%y  %H:%M:%S")



class Producto(): #Se tendran que crear objetos productos que se pasaran a la clase pedido para añadirlo.


     def __init__(self,cod_prod,cantidad_pedida):

        self.cod_prod = cod_prod
        self.cantidad_pedida = cantidad_pedida

     def __repr__(self):
         return "{}x{} \n".format(self.cantidad_pedida,self.cod_prod)


class Pedido():

     lista_productos=[]

     def __init__(self):

         pass

     def addProducto(self,p):

         self.lista_productos.append(p)

     def mostrarproductos(self):

         for p in self.lista_productos:
            print(p)


class PedidoLanzado(Pedido): #Esta clase es una clase intermedia que va a contener una lista con todos aquellos
                          #productos que quiere el cliente que enviemos a fabricación.

    def __init__(self):

       self.lista = super().lista_productos

       for i in self.lista:
          a= i.cod_prod
          b= i.cantidad_pedida
          c= fecha_pedido
          u=InsertarPedidoBDD(a,b,c)
          session.add(u)
          funciones.restar_stock(a,b)
          print("Se ha modificado el stock del producto {} correctamente".format(a))

       session.commit()
       print("se ha añadido el pedido a la BDD")

class InsertarPedidoBDD(Base):

     __tablename__ = "PedidosLanzados"
     __table_args__ = {"sqlite_autoincrement": True}
     id = Column(Integer, primary_key=True)  # Identificador único de cada movimiento de mercancia.
     # (no puede haber dos numeros de pedidos iguales) por eso es primary key)
     cod_prod = Column(String(100), nullable=False)  # nombre del producto
     cantidad_pedida = Column(Integer)  # numero entero
     fecha = Column(String(50))

     def __init__(self,cod_prod,cantidad_pedida,fecha):

         self.cod_prod = cod_prod
         self.cantidad_pedida = cantidad_pedida
         self.fecha = fecha

     def __str__(self):

         return "{}x{} fecha/hora registro:{}\n".format(self.cantidad_pedida, self.cod_prod,self.fecha)



