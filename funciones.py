import pandas as pd
from db import engine
import sqlite3


def cargardatos():

    rutaexcel = "exceldatos/tablasproductosproveedores.xlsx"

    dpd = pd.read_excel(rutaexcel,
                        sheet_name=0)  # dpd contine los datos de productos en un dataframe, extraidos del excel original

    dpv = pd.read_excel(rutaexcel,
                        sheet_name=1)  # dpv contine los datos de productos en un dataframe, extraidos del excel original
    dpd.to_sql("productos", con=engine, if_exists="replace")
    dpv.to_sql("proveedores", con=engine, if_exists="replace")
    print("Excel con datos de productos y proveedores leido y datos cargados correctamente")


def consultas(consulta):

    bdd = 'database/gestionalmacen.db'
    with sqlite3.connect(bdd) as con:
     cursor = con.cursor()
     resultado = cursor.execute(consulta)
     con.commit()  # Ejecutar la consulta SQL preparada anteriormente
    return resultado  # Retornar el resultado de la consulta SQL

def validacion_cantidad_introducido(entry):

    cantidad_introducido_por_usuario = entry
    return len(cantidad_introducido_por_usuario) != 0


def consultar_codigo_unico(p):

    consulta = "SELECT * FROM productos WHERE ID_producto = '{}'".format(p)
    resul = consultas(consulta)
    return len(resul.fetchall()) == 1

def consultar_compra(p): #Esta función comprueba si alguna vez se ha pedido un producto.

    consulta = "SELECT * FROM PedidosLanzados WHERE cod_prod = '{}'".format(p)
    resul = consultas(consulta)
    return len(resul.fetchall())!=0 #si esta funcion nos devuelve True significa que alguna vez se ha comprado este producto

def controlar_stock(a):

    consulta = "SELECT Stock_actual FROM productos WHERE ID_producto= '{}'".format(a)
    resul = consultas(consulta).fetchone()
    g = resul[0]
    return g<=0




def restar_stock(a,b):

    consulta = "SELECT Stock_actual FROM productos WHERE ID_producto= '{}'".format(a)
    resul = consultas(consulta).fetchone()
    g=resul[0]
    v=int(g)-int(b)
    modificacion_stock="UPDATE productos SET Stock_actual= '{}' WHERE ID_producto = '{}'".format(v,a)
    resul2=consultas(modificacion_stock)
    print("se ha actualizado el stock correctamente")


def consultar_movimientos(p):


    consulta = "SELECT PedidosLanzados.fecha,ID_producto,Descripción,Recuento_inicio_mes,PedidosLanzados.cantidad_pedida,Stock_actual,cantidad_minima,ID_Proveedor from productos LEFT JOIN PedidosLanzados ON productos.ID_producto = PedidosLanzados.cod_prod WHERE productos.ID_producto = '{}'ORDER BY PedidosLanzados.fecha ASC".format(p)
    conexion = consultas(consulta).fetchall()
    return conexion

def sin_movimiento(p):

    consulta = "SELECT ID_producto,Descripción,Stock_actual,cantidad_minima,ID_Proveedor from productos  WHERE ID_producto = '{}'".format(p)
    conexion = consultas(consulta).fetchall()
    return conexion

def filtro_proveedores(p):

   consulta = "SELECT* FROM proveedores WHERE ID_Proveedor = '{}'".format(p)

   conexion=consultas(consulta).fetchall()
   return conexion




