import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import openpyxl
from datetime import datetime
import csv

class VentanaAdultos(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1250, height=620)
        self.root = root

        self.frame_info = tk.Frame(self, bg='#CDD8FF')
        self.frame_info.grid(row=0, column=0, sticky="nsew")

        self.frame_tabla = tk.Frame(self, bg='#CDD8FF')
        self.frame_tabla.grid(row=1, column=0, sticky="nsew")

        self.frame_tabla_visualizacion = tk.Frame(self, bg='#CDD8FF')
        self.frame_tabla_visualizacion.grid(row=2, column=0, sticky="nsew")

        self.datos_originales = []

        self.inicializar_gui()

    def inicializar_gui(self):
        self.campos_paciente()
        self.crear_tabla()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def yview(self, *args):
        pass

    def validate_number(self, value):
        return value.isdigit() or value == ""

    def validate_letter(self, value):
        return all(c.isalpha() or c.isspace() for c in value) or value == ""
    
    def on_select(self, event):

        # Get the selected item
        selected_item = self.tabla.selection()

        if selected_item:
            # Do something with the selected item
            print(f"Selected item: {self.tabla.item(selected_item)}")


    def campos_paciente(self):
        self.scrollbar_y = tk.Scrollbar(self.frame_info, orient="vertical", command=self.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")

        self.canvas = tk.Canvas(self.frame_info, bg='#CDD8FF', yscrollcommand=self.scrollbar_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollable_frame = tk.Frame(self.canvas, bg='#CDD8FF')
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        self.frame_info.columnconfigure(0, weight=2, minsize=900)

        self.lblHC = tk.Label(self.scrollable_frame, text='Historia Clinica: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblHC.grid(column=0, row=0, padx=5, pady=5)

        self.lblfecha = tk.Label(self.scrollable_frame, text='Fecha: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblfecha.grid(column=2, row=0, padx=5, pady=5)

        self.lbledad = tk.Label(self.scrollable_frame, text='Edad: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lbledad.grid(column=0, row=1, padx=5, pady=5)

        self.lblsexo = tk.Label(self.scrollable_frame, text='Sexo: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblsexo.grid(column=2, row=1, padx=5, pady=5)

        self.lblNombre = tk.Label(self.scrollable_frame, text='Nombre: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblNombre.grid(column=0, row=2, padx=5, pady=5)

        self.lblApellido = tk.Label(self.scrollable_frame, text='Apellido: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblApellido.grid(column=2, row=2, padx=5, pady=5)

        self.lblFechaN = tk.Label(self.scrollable_frame, text='Fecha de Nacimiento: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblFechaN.grid(column=0, row=3, padx=5, pady=5)

        self.lblDNI = tk.Label(self.scrollable_frame, text='DNI: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblDNI.grid(column=2, row=3, padx=5, pady=5)

        self.lbltelef = tk.Label(self.scrollable_frame, text='Telefono: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lbltelef.grid(column=0, row=4, padx=5, pady=5)

        self.lblDNI = tk.Label(self.scrollable_frame, text='Buscar por Hc: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lblDNI.grid(column=0, row=6, padx=5, pady=5)

        self.lbltelef = tk.Label(self.scrollable_frame, text='Buscar por DNI: ', font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.lbltelef.grid(column=3, row=6, padx=5, pady=15)

        self.svHC = tk.StringVar()
        self.entryHC = tk.Entry(self.scrollable_frame, textvariable=self.svHC, width=20, font=('ARIAL', 10))
        self.entryHC.grid(column=1, row=0, padx=5, pady=5)

        self.svfecha = tk.StringVar()
        self.entryfecha = DateEntry(self.scrollable_frame, textvariable=self.svfecha, width=20, font=('ARIAL', 10), date_pattern='dd-mm-yyyy')
        self.entryfecha.grid(column=3, row=0, padx=5, pady=5)

        self.svedad = tk.StringVar()
        self.entryedad = tk.Entry(self.scrollable_frame, textvariable=self.svedad, width=20, font=('ARIAL', 10))
        self.entryedad.grid(column=1, row=1, padx=5, pady=5)

        self.svsexo_m = tk.IntVar()
        self.checkbox_masculino = tk.Checkbutton(self.scrollable_frame, text='M', variable=self.svsexo_m,
                                                  font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_masculino.grid(column=3, row=1, padx=(0, 1), pady=5)

        self.svsexo_f = tk.IntVar()
        self.checkbox_femenino = tk.Checkbutton(self.scrollable_frame, text='F', variable=self.svsexo_f,
                                                 font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_femenino.grid(column=3, row=1, padx=(90, 0), pady=5)

        self.svNombre = tk.StringVar()
        self.entryNombre = tk.Entry(self.scrollable_frame, textvariable=self.svNombre, width=20, font=('ARIAL', 10))
        self.entryNombre.grid(column=1, row=2, padx=5, pady=5)

        self.svApellido = tk.StringVar()
        self.entryApellido = tk.Entry(self.scrollable_frame, textvariable=self.svApellido, width=20, font=('ARIAL', 10))
        self.entryApellido.grid(column=3, row=2, padx=5, pady=5)

        self.svFechaN = tk.StringVar()
        self.entryFechaN = DateEntry(self.scrollable_frame, textvariable=self.svFechaN, width=20, font=('ARIAL', 10), date_pattern='dd-mm-yyyy')
        self.entryFechaN.grid(column=1, row=3, padx=5, pady=5)

        self.svDNI = tk.StringVar()
        self.entryDNI = tk.Entry(self.scrollable_frame, textvariable=self.svDNI, width=20, font=('ARIAL', 10))
        self.entryDNI.grid(column=3, row=3, padx=5, pady=5)

        self.svtelef = tk.StringVar()
        self.entrytelef = tk.Entry(self.scrollable_frame, textvariable=self.svtelef, width=20, font=('ARIAL', 10))
        self.entrytelef.grid(column=1, row=4, padx=5, pady=5)
        self.datos_originales = []


        self.svBuscHC = tk.StringVar()
        self.entryBuscHC = tk.Entry(self.scrollable_frame, textvariable=self.svBuscHC, width=20, font=('ARIAL', 10))
        self.entryBuscHC.grid(column=1, row=6, padx=5, pady=5)

        self.svBuscDNI = tk.StringVar()
        self.entryBuscDNI = tk.Entry(self.scrollable_frame, textvariable=self.svBuscDNI, width=20, font=('ARIAL', 10))
        self.entryBuscDNI.grid(column=4, row=6, padx=5, pady=15)

        self.btnGuardar = tk.Button(self.scrollable_frame, text='Guardar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#158645', cursor='hand2', activebackground='#35BD6F',command=self.guardar_datos)
        self.btnGuardar.grid(column=1, row=5, padx=5, pady=5)

        self.btnModificar = tk.Button(self.scrollable_frame, text='Modificar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#1658A2', cursor='hand2', activebackground='#3D69F0')
        self.btnModificar.grid(column=2, row=5, padx=5, pady=5)

        self.btnEliminar = tk.Button(self.scrollable_frame, text='Eliminar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#D32F2F', cursor='hand2', activebackground='#E72D40')
        self.btnEliminar.grid(column=3, row=5, padx=5, pady=5)

        self.btnImportar = tk.Button(self.scrollable_frame, text='Importar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#CF811E', cursor='hand2', activebackground='#E72D40')
        self.btnImportar.grid(column=4, row=5, padx=5, pady=5)

        self.btnExportar = tk.Button(self.scrollable_frame, text='Exportar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#CF811E', cursor='hand2', activebackground='#E72D40')
        self.btnExportar.grid(column=5, row=5, padx=15, pady=5)

        self.btnBuscarhc = tk.Button(self.scrollable_frame, text='Buscar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE')
        self.btnBuscarhc.grid(column=2, row=6, padx=15, pady=15)

        self.btnBuscardni = tk.Button(self.scrollable_frame, text='Buscar', width=10, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE')
        self.btnBuscardni.grid(column=5, row=6, padx=5, pady=15)


    def crear_tabla(self):
        # Crear la tabla con el widget Treeview
        self.tabla = ttk.Treeview(self.frame_tabla, columns=("HC", "Fecha", "Edad", "Sexo", "Nombre", "Apellido", "FechaN", "DNI", "Telefono"))

        # Definir encabezados
        self.tabla.heading("#0", text="ID")
        self.tabla.heading("HC", text="Historia Clínica")
        self.tabla.heading("Fecha", text="Fecha")
        self.tabla.heading("Edad", text="Edad")
        self.tabla.heading("Sexo", text="Sexo")
        self.tabla.heading("Nombre", text="Nombre")
        self.tabla.heading("Apellido", text="Apellido")
        self.tabla.heading("FechaN", text="Fecha de Nacimiento")
        self.tabla.heading("DNI", text="DNI")
        self.tabla.heading("Telefono", text="Teléfono")

        # Configurar las columnas
        self.tabla.column("#0", stretch=tk.NO, width=0)  # ID
        self.tabla.column("HC", anchor=tk.CENTER, width=100)
        self.tabla.column("Fecha", anchor=tk.CENTER, width=100)
        self.tabla.column("Edad", anchor=tk.CENTER, width=50)
        self.tabla.column("Sexo", anchor=tk.CENTER, width=50)
        self.tabla.column("Nombre", anchor=tk.W, width=100)
        self.tabla.column("Apellido", anchor=tk.W, width=100)
        self.tabla.column("FechaN", anchor=tk.CENTER, width=100)
        self.tabla.column("DNI", anchor=tk.CENTER, width=80)
        self.tabla.column("Telefono", anchor=tk.CENTER, width=80)

        # Configurar la barra de desplazamiento
        scrollbar_y = ttk.Scrollbar(self.frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar_y.set)
        scrollbar_y.grid(row=0, column=1, sticky="ns")

        # Ubicar la tabla en el grid
        self.tabla.grid(row=0, column=0, sticky="nsew")

        # Configurar la barra de desplazamiento horizontal
        self.frame_tabla.columnconfigure(0, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)

        # Manejar la selección de fila
        self.tabla.bind("<ButtonRelease-1>", self.on_select)
        self.cargar_formulario()
    

    def guardar_datos(self):
        try:
            hc = self.svHC.get()
            fecha = self.svfecha.get()
            edad = self.svedad.get()
            sexo = 'Masculino' if self.svsexo_m.get() else 'Femenino'
            nombre = self.svNombre.get()
            apellido = self.svApellido.get()
            fecha_nacimiento = self.svFechaN.get()
            dni = self.svDNI.get()
            telefono = self.svtelef.get()

            # Validar campos antes de guardar
            if not hc or not fecha or not edad or not sexo or not nombre or not apellido or not fecha_nacimiento or not dni or not telefono:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
                return

            nuevo_paciente = {
                'HC': hc,
                'Fecha': fecha,
                'Edad': edad,
                'Sexo': sexo,
                'Nombre': nombre,
                'Apellido': apellido,
                'FechaN': fecha_nacimiento,
                'DNI': dni,
                'Telefono': telefono
            }

            # Verificar si ya existe un paciente con la misma Historia Clínica
            if any(paciente['HC'] == hc for paciente in self.datos_originales):
                messagebox.showwarning("Advertencia", "Ya existe un paciente con la misma Historia Clínica.")
                return

            # Guardar en la lista de datos_originales
            self.datos_originales.append(nuevo_paciente)

            # Insertar en la tabla y guardar en el archivo CSV
            row_data = [nuevo_paciente[field] for field in ['HC', 'Fecha', 'Edad', 'Sexo', 'Nombre', 'Apellido', 'FechaN', 'DNI', 'Telefono']]
            self.tabla.insert("", "end", values=row_data, tags=(hc,))
            self.guardar_en_csv(row_data)

            # Limpiar los campos después de guardar
            for entry in [self.entryHC, self.entryfecha, self.entryedad, self.checkbox_masculino, self.checkbox_femenino,
                        self.entryNombre, self.entryApellido, self.entryFechaN, self.entryDNI, self.entrytelef]:
                entry.delete(0, tk.END)

        except Exception as e:
            print("Error", f"Error al guardar datos: {str(e)}")

    def guardar_en_csv(self, datos):
        try:
            with open("datos_adultos.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(datos)
        except Exception as e:
            print("Error", f"Error al guardar en CSV: {str(e)}")

        # Get the selected item
        selected_item = self.tabla.selection()

        if selected_item:
            # Do something with the selected item
            print(f"Selected item: {self.tabla.item(selected_item)}")

    def actualizar_archivo_csv(self):
        with open("datos_adultos.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Historia Clínica", "Fecha", "Edad", "Sexo", "Nombres", "Apellidos", "Fecha de Nacimiento", "Teléfono", "DNI"])
            for fila_tabla in self.tabla.get_children():
                datos_fila = self.tabla.item(fila_tabla)['values']
                writer.writerow(datos_fila)

    def actualizar_tabla(self):
        # Clear the table before updating
        self.tabla.delete(*self.tabla.get_children())

        # Update the table with the latest data
        for row in self.datos_originales:
            self.tabla.insert("", "end", values=row, tags=(row[0],))

    def cargar_formulario(self):
       
        self.actualizar_tabla()
        self.cargar_formulario
        try:
            with open("datos_adultos.csv", mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader, None)
                datos = [row for row in reader]
                self.datos_originales = sorted(datos, key=lambda x: datetime.strptime(x[1], '%d-%m-%Y'), reverse=True)

                # Limpiar la tabla antes de cargar los datos ordenados
                self.tabla.delete(*self.tabla.get_children())

                for row in self.datos_originales:
                    self.tabla.insert("", "end", values=row, tags=(row[0],))
        except FileNotFoundError:
            pass
        
                
if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaAdultos(root)
    app.mainloop()
