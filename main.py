import tkinter
from tkinter import *
from tkinter import messagebox, ttk
from funciones import *
from models import *
from db import *

# --------------------------Configuración ventana principal-------------


root = Tk()
root.title('ACCESO AL CONTROL DE STOCK')
root.geometry('500x350')
root.configure(bg='#fff', background='lemon chiffon')
root.resizable(1, 1)
root.wm_iconbitmap('imagenes/imagen-app.ico')

img = PhotoImage(file='imagenes/imagen principal.png')
imagen = Label(root, image=img, bg='lemon chiffon').place(x=0, y=0, relheight=1, relwidth=0.5)

#--------------------------------FIN--------------------------------------------

def acceso():
    usuar = usuario.get()
    contra = contraseña.get()



    if usuar == 'sunoil' and contra == 'sunoil2023':

        screen = Toplevel(root)
        screen.title("Control de stock")
        screen.geometry('925x500')
        screen.configure(bg="white")
        screen.resizable(1, 1)
        screen.wm_iconbitmap('imagenes/imagen-app.ico')


        def hacer_pedido():

            vent_hacer_pedido = Toplevel(screen)
            vent_hacer_pedido.title("Hacer pedido")
            vent_hacer_pedido.geometry('350x500')
            vent_hacer_pedido.configure(bg="white")
            vent_hacer_pedido.resizable(1, 1)
            vent_hacer_pedido.wm_iconbitmap('imagenes/imagen-app.ico')

            # ---------------------Creación del contenedor de la ventana emergente vent_hecer_pedido---------------------

            frame3 = LabelFrame(vent_hacer_pedido, text="Nuevo pedido", font=('Calibri', 20, 'bold'))
            frame3.pack(fill=tkinter.BOTH, padx=20, ipady=250)

            # Label código del  producto
            etiqueta_cod_producto = Label(frame3, text="Código de producto: ", font=('Calibri', 10, 'bold'))
            etiqueta_cod_producto.pack()
            cod_producto = Entry(frame3, justify=CENTER)
            cod_producto.focus()
            cod_producto.pack(expand=True, fill=tkinter.X)

            # Label cantidad pedida del producto
            etiqueta_cantidad = Label(frame3, text="Cantidad: ",
                                      font=('Calibri', 10, 'bold'))  # Etiqueta de texto ubicada en el frame
            etiqueta_cantidad.pack()
            cantidad = Entry(frame3, justify=CENTER)
            cantidad.pack(expand=True, fill=tkinter.X)

            # Mensaje informativo para el usuario
            mensaje = Label(frame3, text='', fg='red')
            mensaje.pack()

            def get_productos(lista):

                registros_tabla = tabla.get_children()  # Obtener todos los datos de la tabla

                for fila in registros_tabla:
                    tabla.delete(fila)

                for p in lista:
                    print(p)  # print para verificar por consola los datos
                    tabla.insert('', 0, text=p)


            def add_producto():


                if consultar_codigo_unico(cod_producto.get()):

                   if controlar_stock(cod_producto.get()) == False:

                      if validacion_cantidad_introducido(cantidad.get()) == True:


                        mensaje['text'] = 'Producto {} añadido correctamente'.format(cod_producto.get())
                        p = Producto(cod_producto.get(), cantidad.get())  # Objeto de la clase Producto
                        m = Pedido()
                        m.addProducto(p)
                        global l
                        l = m.lista_productos
                        cod_producto.delete(0, END)
                        cantidad.delete(0, END)
                        get_productos(l)


                      elif validacion_cantidad_introducido(cantidad.get()) == False:

                          mensaje['text'] = 'La cantidad es obligatoria'
                          cod_producto.delete(0, END)
                          cantidad.delete(0, END)

                   else:
                       mensaje['text'] = 'No hay stock del producto {}, hacer pedido'.format(cod_producto.get())
                       cod_producto.delete(0, END)
                       cantidad.delete(0, END)
                else:

                    mensaje['text'] = 'El Producto {} no existe en nuestra base de datos'.format(cod_producto.get())
                    cod_producto.delete(0, END)
                    cantidad.delete(0, END)
            def lanzar_pedido():

                PedidoLanzado()
                vent_hacer_pedido.destroy()
                l.clear()



            # Boton Añadir Producto al pedido
            s = ttk.Style()
            s.configure('my.TButton', font=('Calibri', 12, 'bold'))
            boton_aniadir = ttk.Button(frame3, text="Añadir producto", style='my.TButton', command=add_producto)
            boton_aniadir.pack(expand=True, fill=tkinter.X)

            # Tabla de Productos que queremos pedir
            # Estilo personalizado para la tabla

            style = ttk.Style()
            style.configure("mystyle.Treeview1", highlightthickness=0, bd=0,
                            font=('Calibri', 12))  # Se modifica la fuente de la tabla

            style.configure("mystyle.Treeview1.Heading",
                            font=('Calibri', 15, 'bold', 'italic'))  # Se modifica la fuente de las cabeceras
            style.layout("mystyle.Treeview1",
                         [('mystyle.Treeview1.treearea',
                           {'sticky': 'nswe'})])  # Eliminamos los bordes # Estructura de la tabla

            # Estructura de la tabla
            tabla = ttk.Treeview(frame3, height=30, columns=(), style="mystyle.Treeview1")
            tabla.pack(expand=True, fill=tkinter.BOTH)
            tabla.heading('#0', text='Productos pedidos', anchor=CENTER)

            # scrolbar
            verscrlbar = ttk.Scrollbar(tabla, orient="vertical", command=tabla.yview)
            verscrlbar.pack(side='right', fill='y')
            tabla.configure(yscrollcommand=verscrlbar.set)

            # Boton Lanzar pedido
            s = ttk.Style()
            s.configure('my.TButton', font=('Calibri', 12, 'bold'))

            boto_lanzar_pedido = ttk.Button(frame3, text='LANZAR PEDIDO', style='my.TButton', command=lanzar_pedido)
            boto_lanzar_pedido.pack(expand=True, fill=tkinter.BOTH, side=tkinter.RIGHT)

        # --------------------------------------------FIN creacion estructura ventana hacer pedido -------------------------------------------

        # --------------------------------------------inicio creacion estructura ventana proveedores -------------------------------------------

        def proveedores():

            vent_proveedor = Toplevel(screen)
            vent_proveedor.title("Consultar datos proveedor")
            vent_proveedor.geometry('450x500')
            vent_proveedor.configure(bg="white")
            vent_proveedor.resizable(1, 1)
            vent_proveedor.wm_iconbitmap('imagenes/imagen-app.ico')

            # -----Configuracion del frame4 para consultar datos del proveedor

            frame4 = LabelFrame(vent_proveedor, bg='lemon chiffon', text='CONSULTA DATOS PROVEEDOR', font=('elephant pro', 10, 'bold'))
            frame4.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.17)

            # Label + Entry de buscar por codigo de proveedor

            etiqueta_buscar_proveedor = Label(frame4, bg='lemon chiffon', text="Código de proveedor buscado: ",
                                         font=('elephant pro', 8, 'bold'))
            etiqueta_buscar_proveedor.place(relx=0.05,rely=0.1,relwidth=0.70)
            buscar_prov = Entry(frame4, justify=CENTER)
            buscar_prov.place(relx=0.70, rely=0.1, relwidth=0.2)

            def buscar_proveedor():

                registros_tabla = tabla3.get_children()  # Obtener todos los datos de la tabla

                for fila in registros_tabla:
                    tabla3.delete(fila)

                registros =filtro_proveedores(buscar_prov.get())
                buscar_prov.delete(0, END)

                for fila in registros:
                    print(fila)  # print para verificar por consola los datos
                    tabla3.insert('', 0, text=fila[1],values=(fila[2], fila[3], fila[4],fila[5]))

            b = ttk.Style()
            b.configure('my.TButton', font=('Calibri', 10, 'bold'))
            boton_buscarpro = ttk.Button(frame4, text="Buscar", style='my.TButton',command=buscar_proveedor)
            boton_buscarpro.place(relx=0.70, rely=0.4, relwidth=0.2, relheight=0.35)



            #Tabla con los datos del proveedor

            style = ttk.Style()
            style.configure("mystyle.Treeview1", highlightthickness=0, bd=0,
                            font=('Calibri', 15))  # Se modifica la fuente de la tabla

            style.configure("mystyle.Treeview1.Heading",
                            font=('Calibri', 15, 'bold', 'italic'))  # Se modifica la fuente de las cabeceras
            style.layout("mystyle.Treeview1",
                         [('mystyle.Treeview1.treearea',
                           {'sticky': 'nswe'})])  # Eliminamos los bordes # Estructura de la tabla

            # Estructura de la tabla
            tabla3 = ttk.Treeview(vent_proveedor, columns=("#0", "#1", "#2", "#3"), style="mystyle.Treeview")
            tabla3.place(relx=0.01,rely=0.3, relwidth=0.95, relheight=0.5)
            tabla3.column('#0', width=15)
            tabla3.heading('#0', text='ID_Proveedor', anchor=CENTER)
            tabla3.column('#1', width=15)
            tabla3.heading('#1', text='Nombre', anchor=CENTER)
            tabla3.column('#2', width=15)
            tabla3.heading('#2', text='Dirección', anchor=CENTER)
            tabla3.column('#3', width=15)
            tabla3.heading('#3', text='Población', anchor=CENTER)
            tabla3.column('#4', width=15)
            tabla3.heading('#4', text='Teléfono', anchor=CENTER)


            # scrolbar
            verscrlbar = ttk.Scrollbar(tabla3, orient="vertical", command=tabla3.yview)
            verscrlbar.pack(side='right', fill='y')
            tabla3.configure(yscrollcommand=verscrlbar.set)

        #------------------Fin configuracion estructura ventana proveedores  -------------------------

        #------------------Creacion columna izquierda como el panel de control de la app
        frame1 = LabelFrame(screen, bg='lemon chiffon', text='PANEL DE CONTROL', font=('elephant pro', 10, 'bold'))
        frame1.place(relx=0, rely=0.05, relwidth=0.2, relheight=1)

        # Añadir botones en el frame1, panel de control
        hacer_pedido = ttk.Button(frame1, text="Hacer pedido", command=hacer_pedido)
        hacer_pedido.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)

        ventas = ttk.Button(frame1, text="Ventas")
        ventas.place(relx=0, rely=0.21, relwidth=1, relheight=0.1)

        compras = ttk.Button(frame1, text="Compras")
        compras.place(relx=0, rely=0.32, relwidth=1, relheight=0.1)

        proveedores = ttk.Button(frame1, text="Proveedores",command=proveedores)
        proveedores.place(relx=0, rely=0.43, relwidth=1, relheight=0.1)

        productos = ttk.Button(frame1, text="Productos")
        productos.place(relx=0, rely=0.54, relwidth=1, relheight=0.1)

        # -----Configuracion del frame2 para consultar datos del stock y movimientos de un producto---

        frame2 = LabelFrame(screen, bg='lemon chiffon', text='CONSULTA STOCK', font=('elephant pro', 10, 'bold'))
        frame2.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.17)

        # Label + Entry de buscar por codigo de producto

        etiqueta_buscar_prod = Label(frame2, bg='lemon chiffon', text="Código de producto buscado: ",
                                     font=('elephant pro', 8, 'bold'))
        etiqueta_buscar_prod.place(relx=0.1, rely=0.1, relwidth=0.3, relheight=0.2)
        buscar_prod = Entry(frame2, justify=CENTER)
        buscar_prod.place(relx=0.4, rely=0.1, relwidth=0.2)

        # Mensaje informativo para el usuario

        mensaje2 = Label(frame2, text='', fg='red', bg='lemon chiffon')
        mensaje2.place(relx=0.15, rely=0.70, relwidth=0.70, relheight=0.20)

        def consultar_estado():

            registros_tabla = tabla2.get_children()

            for fila in registros_tabla:
                tabla2.delete(fila)

            mensaje2['text'] = ''

            if consultar_codigo_unico(buscar_prod.get()):

                if consultar_compra(buscar_prod.get()):

                   registros = consultar_movimientos(buscar_prod.get())
                   buscar_prod.delete(0, END)

                   for fila in registros:
                       print(fila)  # print para verificar por consola los datos
                       tabla2.insert('', 0, text=fila[0],values=(fila[1], fila[2], fila[3], fila[4], fila[5], fila[6],fila[7]))


                else:
                    mensaje2['text'] = 'No se ha vendido este producto durante este mes'
                    registros = sin_movimiento(buscar_prod.get())
                    buscar_prod.delete(0, END)

                    for fila in registros:
                        print(fila)
                        tabla2.insert('',0, text='n/a',values=(fila[0],fila[1],'n/a','n/a',fila[2], fila[3],fila[4]))

            else:
                  mensaje2['text'] = 'El producto no existe en nuestra base de datos'
                  buscar_prod.delete(0, END)

        b = ttk.Style()
        b.configure('my.TButton', font=('Calibri', 15, 'bold'))
        boton_buscar = ttk.Button(frame2, text="Buscar", style='my.TButton', command=consultar_estado)
        boton_buscar.place(relx=0.65, rely=0.2, relwidth=0.1, relheight=0.5)

        # Mensaje informativo para el usuario
        mensaje = Label(text='', fg='red')
        mensaje.place(relx=0.65, rely=0.25)

        # Tabla de resultados de la busqueda de movimientos de los productos
        # Estilo de la tabla

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 9))

        style.configure("mystyle.Treeview.Heading",
                        font=('Calibri', 9, 'bold'))
        style.layout("mystyle.Treeview",
                     [('mystyle.Treeview.treearea',
                       {'sticky': 'nswe'})])

        # Estructura de la tabla
        tabla2 = ttk.Treeview(screen, columns=("#0", "#1", "#2", "#3", "#4", "#5", "#6"), style="mystyle.Treeview")
        tabla2.place(relx=0.25, rely=0.3, relwidth=0.7, relheight=0.5)
        tabla2.column('#0', width=20)
        tabla2.heading('#0', text='Fecha', anchor=CENTER)
        tabla2.column('#1', width=20)
        tabla2.heading('#1', text='Codigo', anchor=CENTER)
        tabla2.column('#2', width=20)
        tabla2.heading('#2', text='Descripción', anchor=CENTER)
        tabla2.column('#3', width=20)
        tabla2.heading('#3', text='Cantidad inicio mes', anchor=CENTER)
        tabla2.column('#4', width=20)
        tabla2.heading('#4', text='Cantidad pedida', anchor=CENTER)
        tabla2.column('#5', width=20)
        tabla2.heading('#5', text='Stock actual', anchor=CENTER)
        tabla2.column('#6', width=20)
        tabla2.heading('#6', text='Stock minimo', anchor=CENTER)
        tabla2.column('#7', width=20)
        tabla2.heading('#7', text='Proveedor', anchor=CENTER)

        # scrolbar
        verscrlbar = ttk.Scrollbar(tabla2, orient="vertical", command=tabla2.yview)
        verscrlbar.pack(side='right', fill='y')
        tabla2.configure(yscrollcommand=verscrlbar.set)

        screen.mainloop()



    elif usuar != 'sunoil' and contra != 'sunoil2023':
        messagebox.showerror('Invalido', 'Usuario y contraseña incorrectos')

    elif contra != 'sunoil2023':
        messagebox.showerror('Invalido', 'contraseña incorrecta ')

    elif usuar != 'sunoil':
        messagebox.showerror('Invalid', 'usuario incorrecto')


frame = Frame(root, bg='lemon chiffon')  # frame principal
frame.place(x=350, y=0, relheight=1, relwidth=0.5)
cabecera = Label(frame, text='Acceso', fg='#57a1f8', bg='lemon chiffon', font=('Microsoft YaHei UI Light', 25, 'bold'))
cabecera.place(x=30, y=0, relwidth=0.5)


def entrar(e):
    usuario.delete(0, 'end')


def salir(e):
    usuar = usuario.get()
    if usuar == '':
        usuario.insert(0, 'usuario')


usuario = Entry(frame, width=25, fg='black', border=0, bg='lemon chiffon', font=('Microsoft YaHei UI Light', 15))
usuario.place(x=10, y=80, relwidth=1)
usuario.insert(0, 'Usuario')
usuario.bind('<FocusIn>', entrar)
usuario.bind('<FocusOut>', salir)

linea_usuario = Frame(frame, width=295, height=2, bg='black').place(x=10, y=107, relwidth=0.5)


def entrar(e):
    contraseña.delete(0, 'end')


def salir(e):
    contra = contraseña.get()
    if contra == '':
        contraseña.insert(0, 'Contraseña')


contraseña = Entry(frame, fg='black', border=0, bg='lemon chiffon', font=('Microsoft YaHei UI Light', 15), show='*')
contraseña.place(x=10, y=150, relwidth=0.5)
contraseña.bind('<FocusIn>', entrar)
contraseña.bind('<FocusOut>', salir)

linea_contraseña = Frame(frame, width=295, height=2, bg='black').place(x=10, y=177, relwidth=0.5)
boton_entrar = Button(frame, width=39, pady=7, text='Acceder', bg='#57a1f8', fg='white', border=0, justify=CENTER,
                      command=acceso).place(x=10, y=204, relwidth=0.5)

if __name__ == '__main__':

    cargardatos()
    Base.metadata.create_all(engine)
    root.mainloop()

    #Estoy haciendo pruebas con git


