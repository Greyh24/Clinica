import tkinter as tk
import pandas as pd
import openpyxl
from tkcalendar import DateEntry
from tkinter import ttk, filedialog, messagebox
from time import strftime
from datetime import datetime
from openpyxl import load_workbook


class VentanaNinos(tk.Frame):
    def center_window(self):
        # Obtener el ancho y alto de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calcular la posición x, y para centrar la ventana
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2

        # Establecer la posición de la ventana
        self.winfo_toplevel().geometry("+{}+{}".format(x, y))
        
    def __init__(self, root):
        super().__init__(root, width=1300, height=620)
        self.root = root

        # Agregar un canvas para hacer la ventana scrollable
        self.canvas = tk.Canvas(self, bg='#CDD8FF', width=1300, height=620)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Agregar un frame al canvas
        self.scrollable_frame = tk.Frame(self.canvas, bg='#CDD8FF')
        self.scrollable_frame.grid(row=0, column=3, sticky="nsew")

        # Configurar el canvas para que sea scrollable
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        # Configurar barras de desplazamiento
        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=3, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=self.scrollbar_x.set)

        # Configurar eventos de desplazamiento
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Llamar al método camposPacienteNiño dentro del canvas
        self.camposPacienteNiño()

        # Crear y configurar la tabla
        self.create_table()
        self.load_data_to_table()
        self.center_window()

    def on_canvas_configure(self, event):
        # Configurar la región de desplazamiento del canvas cuando cambia el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Configurar la región de desplazamiento del frame interior cuando cambia el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_table(self):
        # Crear la tabla usando ttk.Treeview
        self.table = ttk.Treeview(self.scrollable_frame, columns=("Columna1", "Columna2", "Columna3", "Columna4", "Columna5", "Columna6", "Columna7", "Columna8", "Columna9", "Columna10", "Columna11", "Columna12", "Columna13", "Columna14", "Columna15", "Columna16", "Columna17", "Columna18", "Columna19", "Columna20", "Columna21", "Columna22", "Columna23", "Columna24", "Columna25", "Columna26", "Columna27", "Columna28", "Columna29", "Columna30", "Columna31", "Columna32", "Columna33", "Columna34", "Columna35", "Columna36", "Columna37", "Columna38"))
        
        # Configurar encabezados de columnas
        self.table.heading("#0", text="ID")
        self.table.heading("Columna1", text="Nº de HC")
        self.table.heading("Columna2", text="Médico")
        self.table.heading("Columna3", text="Especialidad")
        self.table.heading("Columna4", text="Fecha de Atención")
        self.table.heading("Columna5", text="Hora de Atención")
        self.table.heading("Columna6", text="Paciente")
        self.table.heading("Columna7", text="DNI")
        self.table.heading("Columna8", text="Sexo")
        self.table.heading("Columna9", text="Edad")
        self.table.heading("Columna10", text="Fecha de Nacimiento")
        self.table.heading("Columna11", text="Grupo Sanguineo")
        self.table.heading("Columna12", text="Rh")
        self.table.heading("Columna13", text="Dirección")
        self.table.heading("Columna14", text="Ocupación")
        self.table.heading("Columna15", text="Nombre del Padre")
        self.table.heading("Columna16", text="DNI del Padre")
        self.table.heading("Columna17", text="Telefono del Padre")
        self.table.heading("Columna18", text="Nombre de la Madre")
        self.table.heading("Columna19", text="DNI de la Madre")
        self.table.heading("Columna20", text="Telefono de la Madre")
        self.table.heading("Columna21", text="Datos del Apoderado")
        self.table.heading("Columna22", text="DNI del Apoderado")
        self.table.heading("Columna23", text="Telefono del Apoderado")
        self.table.heading("Columna24", text="Vinculo con el Menor")
        self.table.heading("Columna25", text="Otros")
        self.table.heading("Columna26", text="Antecedentes Personales")
        self.table.heading("Columna27", text="Antecedentes Familiares")
        self.table.heading("Columna28", text="RAM/Alergias")
        self.table.heading("Columna29", text="Motivo de la Consulta")
        self.table.heading("Columna30", text="Forma de Inicio")
        self.table.heading("Columna31", text="Tiempo de Enfermedad")
        self.table.heading("Columna32", text="Signos y Síntomas Principales")
        self.table.heading("Columna33", text="Frecuencia Cardíaca")
        self.table.heading("Columna34", text="Frecuencia Respiratoria")
        self.table.heading("Columna35", text="Presión Arterial")
        self.table.heading("Columna36", text="Temperatura")
        self.table.heading("Columna37", text="Peso")
        self.table.heading("Columna38", text="Talla")

        # Configurar las columnas
        self.table.column("#0", stretch=tk.NO, width=0)  # ID
        self.table.column("Columna1", anchor=tk.CENTER, width=100)
        self.table.column("Columna2", anchor=tk.CENTER, width=100)
        self.table.column("Columna3", anchor=tk.CENTER, width=100)
        self.table.column("Columna4", anchor=tk.CENTER, width=100)
        self.table.column("Columna5", anchor=tk.CENTER, width=100)
        self.table.column("Columna6", anchor=tk.CENTER, width=100)
        self.table.column("Columna7", anchor=tk.CENTER, width=100)
        self.table.column("Columna8", anchor=tk.CENTER, width=100)
        self.table.column("Columna9", anchor=tk.CENTER, width=100)
        self.table.column("Columna10", anchor=tk.CENTER, width=100)
        self.table.column("Columna11", anchor=tk.CENTER, width=100)
        self.table.column("Columna12", anchor=tk.CENTER, width=100)
        self.table.column("Columna13", anchor=tk.CENTER, width=100)
        self.table.column("Columna14", anchor=tk.CENTER, width=100)
        self.table.column("Columna15", anchor=tk.CENTER, width=100)
        self.table.column("Columna16", anchor=tk.CENTER, width=100)
        self.table.column("Columna17", anchor=tk.CENTER, width=100)
        self.table.column("Columna18", anchor=tk.CENTER, width=100)
        self.table.column("Columna19", anchor=tk.CENTER, width=100)
        self.table.column("Columna20", anchor=tk.CENTER, width=100)
        self.table.column("Columna21", anchor=tk.CENTER, width=100)
        self.table.column("Columna22", anchor=tk.CENTER, width=100)
        self.table.column("Columna23", anchor=tk.CENTER, width=100)
        self.table.column("Columna24", anchor=tk.CENTER, width=100)
        self.table.column("Columna25", anchor=tk.CENTER, width=100)
        self.table.column("Columna26", anchor=tk.CENTER, width=100)
        self.table.column("Columna27", anchor=tk.CENTER, width=100)
        self.table.column("Columna28", anchor=tk.CENTER, width=100)
        self.table.column("Columna29", anchor=tk.CENTER, width=100)
        self.table.column("Columna30", anchor=tk.CENTER, width=100)
        self.table.column("Columna31", anchor=tk.CENTER, width=100)
        self.table.column("Columna32", anchor=tk.CENTER, width=100)
        self.table.column("Columna33", anchor=tk.CENTER, width=100)
        self.table.column("Columna34", anchor=tk.CENTER, width=100)
        self.table.column("Columna35", anchor=tk.CENTER, width=100)
        self.table.column("Columna36", anchor=tk.CENTER, width=100)
        self.table.column("Columna37", anchor=tk.CENTER, width=100)
        self.table.column("Columna38", anchor=tk.CENTER, width=100)
        
        # Colocar la tabla en la posición deseada
        self.table.grid(row=30, column=0, columnspan=38, padx=5, pady=10)

        # Establecer un ancho fijo de 10 para cada columna
        for col in self.table["columns"]:
            self.table.column(col, width=100)
        
    def yview(self, *args):
        pass
    
    def validate_number(self, value):
        # Función de validación para aceptar solo números
        return value.isdigit() or value == ""
    
    def validate_decimal(self, value):
        # Función de validación para aceptar números decimales
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def validate_letter(self, value):
        # Función de validación para aceptar solo letras
        return all(c.isalpha() or c.isspace() for c in value) or value == ""
    
    def actualizar_hora(self):
        hora_actual = strftime('%H:%M %p')
        self.entryHDA.delete(0, tk.END)
        self.entryHDA.insert(0, hora_actual)
    
    def limpiar_datos(self):
        # Vaciar o deseleccionar los datos de los StringVar
        self.svHC.set('')
        self.svMd.set('')
        self.sveEspe.set('')
        self.svFDA.set('')
        self.svHDA.set('')
        self.svPaci.set('')
        self.svDNI.set('')
        self.svedad.set('')
        self.svFDN.set('')
        self.svGS.set('')
        self.svRH.set('')
        self.svDireccion.set('')
        self.svOcup.set('')
        self.svDpadre.set('')
        self.svDNIp.set('')
        self.svTelefP.set('')
        self.svDMadre.set('')
        self.svDNIMadre.set('')
        self.svTelefonoMadre.set('')
        self.svDatosApo.set('')
        self.svDNIDDA.set('')
        self.svTelefonoApoderado.set('')
        self.svVinculo.set('')
        self.svOTROS.set('')
        self.svAntecedentesP.set('')
        self.svAntecedentesF.set('')
        self.svRA.set('')
        self.svMC.set('')
        self.svFdI.set('')
        self.svTdE.set('')
        self.svSySP.set('')
        self.svFC.set('')
        self.svFR.set('')
        self.svPresionA.set('')
        self.svTC.set('')
        self.svPeso.set('')
        self.svTalla.set('')

        # Deseleccionar los datos de los BooleanVar
        self.svsexo_m.set(0)
        self.svsexo_f.set(0)
        self.svBCG.set(False)
        self.svHVB.set(False)
        self.svPENTAVALENTE.set(False)
        self.svANTIPOLIO.set(False)
        self.svANTINEUMOCOCICA.set(False)
        self.svDT.set(False)
        self.svSPR.set(False)
        self.svROTAVIRUS.set(False)
        self.svINFLUENZA_PED.set(False)
        self.svVARICELA.set(False)
        self.svDPR.set(False)
        self.svAPO.set(False)
        self.svANTIAMARILICA.set(False)

    def camposPacienteNiño(self):
       
        #labels
        self.lblHC =tk.Label(self.scrollable_frame, text='Historia Clinica: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=0, padx=(0, 1), pady=5)

        self.lblMd =tk.Label(self.scrollable_frame, text='Médico: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=1, padx=(0, 1), pady=0)

        self.lblEspe =tk.Label(self.scrollable_frame, text='Especialidad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=1, padx=(0, 1), pady=0)
      
        self.lblFDA =tk.Label(self.scrollable_frame, text='Fecha de Atención: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=2, padx=(0, 1), pady=0)

        self.lblHDA =tk.Label(self.scrollable_frame, text='Hora de Atención: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=2,padx=(0, 1), pady=5)
        
        self.lblDA =tk.Label(self.scrollable_frame, text='DATOS GENERALES: ',font=('ARIAL',12,'bold'), bg='#CDD8FF').grid(column=0, row=3, padx=0, pady=5)

        self.lblPaci =tk.Label(self.scrollable_frame, text='Paciente: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=4, padx=(0, 1), pady=5)

        self.lblDNI =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=4, padx=(0, 5), pady=5)

        self.lblSexo =tk.Label(self.scrollable_frame, text='Sexo: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=4, padx=(0, 1), pady=5)

        self.lbledad =tk.Label(self.scrollable_frame, text='Edad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=5, padx=(0, 1), pady=5)

        self.lblFDN =tk.Label(self.scrollable_frame, text='Fecha de nacimiento: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=5, padx=(0, 10), pady=5)
        
        self.lblGS =tk.Label(self.scrollable_frame, text='Grupo Sanguineo: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=5, padx=(0, 10), pady=5)

        self.lblRH =tk.Label(self.scrollable_frame, text='Rh: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=6, padx=(0, 1), pady=5)

        self.lblDireccion =tk.Label(self.scrollable_frame, text='Dirección: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=6, padx=(0, 1), pady=5)

        self.lblOcup =tk.Label(self.scrollable_frame, text='Ocupación: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=6, padx=(0, 10), pady=5)

        self.lblDPYOA =tk.Label(self.scrollable_frame, text='DATOS DE LOS PADRES Y/O APODERADO: ',font=('ARIAL',12,'bold'), bg='#CDD8FF').grid(column=0, row=7, padx=0, pady=5)
        
        self.lblDpadre =tk.Label(self.scrollable_frame, text='Datos del Padre: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=8, padx=(0, 1), pady=5)

        self.lblDNIp =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=8, padx=(0, 1), pady=5)

        self.lblTelefP =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=8, padx=(0, 1), pady=5)

        self.lblDMadre =tk.Label(self.scrollable_frame, text='Datos de la Madre: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=9, padx=(0, 1), pady=5)

        self.lblDNIMadre =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=9, padx=(0, 1), pady=5)

        self.lblTelefonoMadre =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=9,  padx=(0, 1), pady=5)

        self.lblDatosApo =tk.Label(self.scrollable_frame, text='Datos del Apoderado: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=10,padx=(0, 1), pady=5)

        self.lblDNIDDA =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=10, padx=(0, 1), pady=5)

        self.lblTelefonoApoderado =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=10,  padx=(0, 1), pady=5)

        self.lblVinculo =tk.Label(self.scrollable_frame, text='Vinculo con el menor: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=11, padx=(0, 1), pady=5)

        self.lblESQUEMAV =tk.Label(self.scrollable_frame, text='ESQUEMA DE VACUNACIÓN: ',font=('ARIAL',12,'bold'), bg='#CDD8FF').grid(column=0, row=12, padx=0, pady=5)
        
        self.lblOTROS =tk.Label(self.scrollable_frame, text='Otros: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=16, padx=(0, 20), pady=5)

        self.lblAntecedentes =tk.Label(self.scrollable_frame, text='ANTECEDENTE: ',font=('ARIAL',12,'bold'), bg='#CDD8FF').grid(column=0, row=17, padx=0, pady=5)

        self.lblAntecedentesP =tk.Label(self.scrollable_frame, text='Antecedentes Personales: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=18, padx=(0, 20), pady=5)

        self.lblAntecedentesF =tk.Label(self.scrollable_frame, text='Antecedentes Familiares: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=18, padx=(0, 20), pady=5)

        self.lblRA =tk.Label(self.scrollable_frame, text='RAM / Alergias: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=2, row=18, padx=(0, 20), pady=5)

        self.lblANAMNESIS =tk.Label(self.scrollable_frame, text='ANAMNESIS: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=19, padx=(0, 20), pady=5)

        self.lblMC =tk.Label(self.scrollable_frame, text='Motivo de consulta: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=20, padx=(0, 20), pady=5)

        self.lblFdI =tk.Label(self.scrollable_frame, text='Forma de Inicio: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=20, padx=(0, 20), pady=5)

        self.lblTdE =tk.Label(self.scrollable_frame, text='Tiempo de enfermedad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=21, padx=(0, 20), pady=5)

        self.lblSySP =tk.Label(self.scrollable_frame, text='Signos y síntomas principales: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=21, padx=(0, 20), pady=5)

        self.lblExamenF =tk.Label(self.scrollable_frame, text='EXAMEN FÍSICO: ',font=('ARIAL',12,'bold'), bg='#CDD8FF').grid(column=0, row=22, padx=0, pady=5)

        self.lblFC =tk.Label(self.scrollable_frame, text='Frecuencia Cardíaca (x min): ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=23, padx=(0, 20), pady=5)

        self.lblFR =tk.Label(self.scrollable_frame, text='Frecuencia Respiratoria (x min): ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=23, padx=(0, 20), pady=5)

        self.lblPresionA =tk.Label(self.scrollable_frame, text='Presión Arterial (mmHg): ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=24, padx=(0, 20), pady=5)

        self.lblTC =tk.Label(self.scrollable_frame, text='Temp (ºC): ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=24, padx=(0, 20), pady=5)

        self.lblPeso =tk.Label(self.scrollable_frame, text='Peso: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=25, padx=(0, 20), pady=5)

        self.lblTalla =tk.Label(self.scrollable_frame, text='Talla: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=1, row=25, padx=(0, 20), pady=5)

        self.lblBuscar =tk.Label(self.scrollable_frame, text='Buscar por Hc o DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF').grid(column=0, row=27,  padx=(0, 20), pady=5)

        #entry
        self.svHC = tk.StringVar()
        self.entryHC = tk.Entry(self.scrollable_frame, textvariable= self.svHC,width=20, font=('ARIAL',10))
        self.entryHC.grid(column=1, row=0, padx=(290, 0), pady=5)

        self.svMd = tk.StringVar()
        self.entryMd = tk.Entry(self.scrollable_frame, textvariable= self.svMd,width=20, font=('ARIAL',10))
        self.entryMd.grid(column=0, row=1, padx=(190, 0), pady=5)

        self.sveEspe = tk.StringVar()
        self.entryEspe = tk.Entry(self.scrollable_frame, textvariable= self.sveEspe,width=20, font=('ARIAL',10))
        self.entryEspe.grid(column=1, row=1, padx=(290, 0), pady=5)

        self.svFDA = tk.StringVar()
        self.entryFDA = DateEntry(self.scrollable_frame, textvariable= self.svFDA,width=20, font=('ARIAL',10),date_pattern='dd-mm-yyyy')
        self.entryFDA.grid(column=0, row=2, padx=(290, 0), pady=5)

        self.svHDA = tk.StringVar()
        self.entryHDA = ttk.Entry(self.scrollable_frame, textvariable=self.svHDA, width=20, font=('ARIAL', 10))
        self.entryHDA.grid(column=1, row=2, padx=(290, 0), pady=5)
        self.actualizar_hora()

        self.svPaci = tk.StringVar()
        self.entryPaci = tk.Entry(self.scrollable_frame, textvariable= self.svPaci,width=20, font=('ARIAL',10))
        self.entryPaci.grid(column=0, row=4, padx=(290, 0), pady=5)
        
        self.svDNI = tk.StringVar()
        self.entryDNI = tk.Entry(self.scrollable_frame, textvariable= self.svDNI,width=20, font=('ARIAL',10))
        self.entryDNI.grid(column=1, row=4, padx=(290, 0), pady=5)

        # checkboxes para el género
        self.svsexo_m = tk.IntVar()
        self.checkbox_masculino = tk.Checkbutton(self.scrollable_frame, text='M', variable=self.svsexo_m, font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_masculino.grid(column=2, row=4,columnspan=2, padx=(0,10), pady=5)

        self.svsexo_f = tk.IntVar()
        self.checkbox_femenino = tk.Checkbutton(self.scrollable_frame, text='F', variable=self.svsexo_f, font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_femenino.grid(column=2, row=4,columnspan=2, padx=(119, 0), pady=5)

        self.svedad = tk.StringVar()
        self.entryedad = tk.Entry(self.scrollable_frame, textvariable= self.svedad,width=20, font=('ARIAL',10))
        self.entryedad.grid(column=0, row=5, padx=(290, 0), pady=5)

        self.svFDN = tk.StringVar()
        self.entryFDN = DateEntry(self.scrollable_frame, textvariable= self.svFDN,width=20, font=('ARIAL',10))
        self.entryFDN.grid(column=1, row=5, padx=(290, 0), pady=5)

        self.svGS = tk.StringVar()
        self.entryGS = tk.Entry(self.scrollable_frame, textvariable= self.svGS,width=20, font=('ARIAL',10))
        self.entryGS.grid(column=2, row=5, padx=(290, 0), pady=5)

        self.svRH = tk.StringVar()
        self.entryRH = tk.Entry(self.scrollable_frame, textvariable= self.svRH,width=20, font=('ARIAL',10))
        self.entryRH.grid(column=0, row=6, padx=(290, 0), pady=5)

        self.svDireccion = tk.StringVar()
        self.entryDireccion = tk.Entry(self.scrollable_frame, textvariable= self.svDireccion,width=20, font=('ARIAL',10))
        self.entryDireccion.grid(column=1, row=6, padx=(290, 0), pady=5)

        self.svOcup = tk.StringVar()
        self.entryOcup = tk.Entry(self.scrollable_frame, textvariable= self.svOcup,width=20, font=('ARIAL',10))
        self.entryOcup.grid(column=2, row=6, padx=(290, 0), pady=5)

        self.svDpadre = tk.StringVar()
        self.entryDpadre = tk.Entry(self.scrollable_frame, textvariable= self.svDpadre,width=20, font=('ARIAL',10))
        self.entryDpadre.grid(column=0, row=8, padx=(290, 0), pady=5)
       
        self.svDNIp = tk.StringVar()
        self.entryDNIp = tk.Entry(self.scrollable_frame, textvariable= self.svDNIp,width=20, font=('ARIAL',10))
        self.entryDNIp.grid(column=1, row=8, padx=(290, 0), pady=5)

        self.svTelefP = tk.StringVar()
        self.entryTelefP = tk.Entry(self.scrollable_frame, textvariable= self.svTelefP,width=20, font=('ARIAL',10))
        self.entryTelefP.grid(column=2, row=8, padx=(290, 0), pady=5)

        self.svDMadre = tk.StringVar()
        self.entryDMadre = tk.Entry(self.scrollable_frame, textvariable= self.svDMadre,width=20, font=('ARIAL',10))
        self.entryDMadre.grid(column=0, row=9, padx=(290, 0), pady=5)

        self.svDNIMadre = tk.StringVar()
        self.entryDNIMadre = tk.Entry(self.scrollable_frame, textvariable= self.svDNIMadre,width=20, font=('ARIAL',10))
        self.entryDNIMadre.grid(column=1, row=9, padx=(290, 0), pady=5)

        self.svTelefonoMadre = tk.StringVar()
        self.entryTelefonoMadre = tk.Entry(self.scrollable_frame, textvariable= self.svTelefonoMadre,width=20, font=('ARIAL',10))
        self.entryTelefonoMadre.grid(column=2, row=9, padx=(290, 0), pady=5)

        self.svDatosApo = tk.StringVar()
        self.entryDatosApo = tk.Entry(self.scrollable_frame, textvariable= self.svDatosApo,width=20, font=('ARIAL',10))
        self.entryDatosApo.grid(column=0, row=10, padx=(290, 0), pady=5)

        self.svDNIDDA = tk.StringVar()
        self.entryDNIDDA = tk.Entry(self.scrollable_frame, textvariable= self.svDNIDDA,width=20, font=('ARIAL',10))
        self.entryDNIDDA.grid(column=1, row=10, padx=(290, 0), pady=5)

        self.svTelefonoApoderado = tk.StringVar()
        self.entryTelefonoApoderado = tk.Entry(self.scrollable_frame, textvariable= self.svTelefonoApoderado,width=20, font=('ARIAL',10))
        self.entryTelefonoApoderado.grid(column=2, row=10, padx=(290, 0), pady=5)

        self.svVinculo = tk.StringVar()
        self.entryVinculo = tk.Entry(self.scrollable_frame, textvariable= self.svVinculo,width=20, font=('ARIAL',10))
        self.entryVinculo.grid(column=0, row=11, padx=(290, 0), pady=5)
        
        self.svBCG = tk.BooleanVar()
        self.entryBCG = tk.Checkbutton(self.scrollable_frame, text="BCG", variable=self.svBCG, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryBCG.grid(column=0, row=13, padx=(0, 20), pady=5)

        self.svHVB = tk.BooleanVar()
        self.entryHVB = tk.Checkbutton(self.scrollable_frame, text="HVB", variable=self.svHVB, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryHVB.grid(column=0, row=13, padx=(290, 0), pady=5)

        self.svPENTAVALENTE = tk.BooleanVar()
        self.entryPENTAVALENTE = tk.Checkbutton(self.scrollable_frame, text="PENTAVALENTE", variable=self.svPENTAVALENTE, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryPENTAVALENTE.grid(column=1, row=13, padx=(0, 20), pady=5)

        self.svANTIPOLIO = tk.BooleanVar()
        self.entryANTIPOLIO = tk.Checkbutton(self.scrollable_frame, text="ANTIPOLIO", variable=self.svANTIPOLIO, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTIPOLIO.grid(column=1, row=13, padx=(290, 0), pady=5)

        self.svANTINEUMOCOCICA = tk.BooleanVar()
        self.entryANTINEUMOCOCICA = tk.Checkbutton(self.scrollable_frame, text="ANTINEUMOCOCICA", variable=self.svANTINEUMOCOCICA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTINEUMOCOCICA.grid(column=2, row=13, padx=(0, 20), pady=5)

        self.svDT = tk.BooleanVar()
        self.entryDT = tk.Checkbutton(self.scrollable_frame, text="DT", variable=self.svDT, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryDT.grid(column=2, row=13, padx=(290, 0), pady=5)

        self.svSPR = tk.BooleanVar()
        self.entrySPR = tk.Checkbutton(self.scrollable_frame, text="SPR", variable=self.svSPR, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entrySPR.grid(column=0, row=14, padx=(0, 20), pady=5)

        self.svROTAVIRUS = tk.BooleanVar()
        self.entryROTAVIRUS = tk.Checkbutton(self.scrollable_frame, text="ROTAVIRUS", variable=self.svROTAVIRUS, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryROTAVIRUS.grid(column=0, row=14, padx=(290, 0), pady=5)

        self.svINFLUENZA_PED = tk.BooleanVar()
        self.entryINFLUENZA_PED = tk.Checkbutton(self.scrollable_frame, text="INFLUENZA PED.", variable=self.svINFLUENZA_PED, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryINFLUENZA_PED.grid(column=1, row=14, padx=(0, 20), pady=5)

        self.svVARICELA = tk.BooleanVar()
        self.entryVARICELA = tk.Checkbutton(self.scrollable_frame, text="VARICELA", variable=self.svVARICELA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryVARICELA.grid(column=1, row=14, padx=(290, 0), pady=5)

        self.svDPR = tk.BooleanVar()
        self.entryDPR = tk.Checkbutton(self.scrollable_frame, text="DPR", variable=self.svDPR, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryDPR.grid(column=2, row=14, padx=(0, 20), pady=5)

        self.svAPO = tk.BooleanVar()
        self.entryAPO = tk.Checkbutton(self.scrollable_frame, text="APO", variable=self.svAPO, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryAPO.grid(column=2, row=14, padx=(290, 0), pady=5)

        self.svANTIAMARILICA = tk.BooleanVar()
        self.entryANTIAMARILICA = tk.Checkbutton(self.scrollable_frame, text="ANTIAMARILICA", variable=self.svANTIAMARILICA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTIAMARILICA.grid(column=0, row=15, padx=(0, 20), pady=5)

        self.svOTROS = tk.StringVar()
        self.entryOTROS = tk.Entry(self.scrollable_frame, textvariable= self.svOTROS,width=20, font=('ARIAL',10))
        self.entryOTROS.grid(column=0, row=16, padx=(290, 0), pady=5)
 
        self.svAntecedentesP = tk.StringVar()
        self.entryAntecedentesP = tk.Entry(self.scrollable_frame, textvariable= self.svAntecedentesP,width=20, font=('ARIAL',10))
        self.entryAntecedentesP.grid(column=0, row=18, padx=(290, 0), pady=5)
        
        self.svAntecedentesF = tk.StringVar()
        self.entryAntecedentesF = tk.Entry(self.scrollable_frame, textvariable= self.svAntecedentesF,width=20, font=('ARIAL',10))
        self.entryAntecedentesF.grid(column=1, row=18, padx=(290, 0), pady=5)

        self.svRA = tk.StringVar()
        self.entryRA = tk.Entry(self.scrollable_frame, textvariable= self.svRA,width=20, font=('ARIAL',10))
        self.entryRA.grid(column=2, row=18, padx=(290, 0), pady=5)

        self.svMC = tk.StringVar()
        self.entryMC = tk.Entry(self.scrollable_frame, textvariable= self.svMC,width=20, font=('ARIAL',10))
        self.entryMC.grid(column=0, row=20, padx=(290, 0), pady=5)

        self.svFdI = tk.StringVar()
        self.entryFdI = tk.Entry(self.scrollable_frame, textvariable= self.svFdI,width=20, font=('ARIAL',10))
        self.entryFdI.grid(column=1, row=20, padx=(320, 0), pady=5)

        self.svTdE = tk.StringVar()
        self.entryTdE = tk.Entry(self.scrollable_frame, textvariable= self.svTdE,width=20, font=('ARIAL',10))
        self.entryTdE.grid(column=0, row=21, padx=(290, 0), pady=5)

        self.svSySP = tk.StringVar()
        self.entrySySP = tk.Entry(self.scrollable_frame, textvariable= self.svSySP,width=20, font=('ARIAL',10))
        self.entrySySP.grid(column=1, row=21, padx=(320, 0), pady=5)

        self.svFC = tk.StringVar()
        self.entryFC = tk.Entry(self.scrollable_frame, textvariable= self.svFC,width=20, font=('ARIAL',10))
        self.entryFC.grid(column=0, row=23, padx=(320, 0), pady=5)

        self.svFR = tk.StringVar()
        self.entryFR = tk.Entry(self.scrollable_frame, textvariable= self.svFR,width=20, font=('ARIAL',10))
        self.entryFR.grid(column=1, row=23, padx=(330, 0), pady=5)

        self.svPresionA = tk.StringVar()
        self.entryPresionA = tk.Entry(self.scrollable_frame, textvariable= self.svPresionA,width=20, font=('ARIAL',10))
        self.entryPresionA.grid(column=0, row=24, padx=(320, 0), pady=5)

        self.svTC = tk.StringVar()
        self.entryTC = tk.Entry(self.scrollable_frame, textvariable= self.svTC,width=20, font=('ARIAL',10))
        self.entryTC.grid(column=1, row=24, padx=(330, 0), pady=5)

        self.svPeso = tk.StringVar()
        self.entryPeso = tk.Entry(self.scrollable_frame, textvariable= self.svPeso,width=20, font=('ARIAL',10))
        self.entryPeso.grid(column=0, row=25, padx=(320, 0), pady=5)

        self.svTalla = tk.StringVar()
        self.entryTalla = tk.Entry(self.scrollable_frame, textvariable= self.svTalla,width=20, font=('ARIAL',10))
        self.entryTalla.grid(column=1, row=25, padx=(330, 0), pady=5)

        self.svBuscar = tk.StringVar()
        self.entryBuscar = tk.Entry(self.scrollable_frame, textvariable= self.svBuscar,width=20, font=('ARIAL',10))
        self.entryBuscar.grid(column=0, row=27, padx=(290, 0), pady=5)
        
        # Añadir este código en el constructor __init__ o en algún lugar donde se configuren tus widgets
        self.svBuscar.trace_add("write", lambda *args: self.verificar_y_cargar_tabla())

        # validación para aceptar solo números
        self.entryDNI.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryedad.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryDNIp.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryTelefP.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryDNIMadre.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryTelefonoMadre.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryDNIDDA.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        self.entryTelefonoApoderado.config(validate="key", validatecommand=(self.root.register(self.validate_number), '%P'))
        
        # validación para aceptar números decimales
        self.entryFC.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        self.entryFR.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        self.entryPresionA.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        self.entryTC.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        self.entryPeso.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        self.entryTalla.config(validate="key", validatecommand=(self.register(self.validate_decimal), "%P"))
        
        # validación para aceptar solo letras
        self.entryMd.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryEspe.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryPaci.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryOcup.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDpadre.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDMadre.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDatosApo.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryVinculo.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))

        #BOTON
        self.btnGuardar = tk.Button(self.scrollable_frame, text='Guardar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#158645',cursor='hand2', activebackground='#35BD6F',command=self.guardar_datos_en_excel).grid(column=0, row=26, padx=(0, 20), pady=5)

        self.btnModificar = tk.Button(self.scrollable_frame, text='Modificar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#1658A2',cursor='hand2', activebackground='#3D69F0').grid(column=0, row=26, padx=(200, 0), pady=5)

        self.btnEliminar = tk.Button(self.scrollable_frame, text='Eliminar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#D32F2F',cursor='hand2', activebackground='#E72D40',command=self.eliminar_seleccionado).grid(column=0, row=26, padx=(400, 0), pady=5)

        self.btnImportar = tk.Button(self.scrollable_frame, text='Importar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#CF811E',cursor='hand2', activebackground='#E72D40',command=self.importar_desde_excel).grid(column=1, row=26, padx=(0, 20), pady=5)

        self.btnExportar = tk.Button(self.scrollable_frame, text='Exportar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#CF811E',cursor='hand2', activebackground='#E72D40',command=self.exportar_a_excel).grid(column=1, row=26, padx=(200, 0), pady=5)

        self.btnBuscar = tk.Button(self.scrollable_frame, text='Buscar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#0F1010',cursor='hand2', activebackground='#FFFEFE', command=self.search_data).grid(column=0, row=27, padx=(550, 0), pady=5)

    def guardar_datos_en_excel(self):
        # Obtener la fecha actual en el formato deseado ("dd-mm-yyyy")
        fecha_actual = datetime.now().strftime("%d-%m-%Y")

        # Mapear el valor de sexo
        sexo = 'Masculino' if self.svsexo_m.get() else 'Femenino' if self.svsexo_f.get() else ''

        # Mapear los valores de vacunación
        vacunas = [
            'BCG' if self.svBCG.get() else None,
            'HVB' if self.svHVB.get() else None,
            'PENTAVALENTE' if self.svPENTAVALENTE.get() else None,
            'ANTIPOLIO' if self.svANTIPOLIO.get() else None,
            'ANTINEUMOCOCICA' if self.svANTINEUMOCOCICA.get() else None,
            'DT' if self.svDT.get() else None,
            'SPR' if self.svSPR.get() else None,
            'ROTAVIRUS' if self.svROTAVIRUS.get() else None,
            'INFLUENZA_PED' if self.svINFLUENZA_PED.get() else None,
            'VARICELA' if self.svVARICELA.get() else None,
            'DPR' if self.svDPR.get() else None,
            'APO' if self.svAPO.get() else None,
            'ANTIAMARILICA' if self.svANTIAMARILICA.get() else None,
        ]

        # Filtrar las vacunas seleccionadas (eliminando los elementos None)
        vacunas_seleccionadas = [vacuna for vacuna in vacunas if vacuna is not None]

        # Agregar el valor ingresado en "Otros_Vacunas" si se ha ingresado algo
        otros_vacunas_valor = self.svOTROS.get().strip()  # Eliminar espacios en blanco
        if otros_vacunas_valor:
            vacunas_seleccionadas.append(otros_vacunas_valor)

        # Crear un diccionario con los datos recopilados
        datos = {
            'Historia_Clinica': [self.svHC.get()],
            'Medico': [self.svMd.get()],
            'Especialidad': [self.sveEspe.get()],
            'Fecha_Atencion': [self.svFDA.get()],
            'Hora_Atencion': [self.svHDA.get()],
            'Paciente': [self.svPaci.get()],
            'DNI': [self.svDNI.get()],
            'Sexo': [sexo],
            'Edad': [self.svedad.get()],
            'Fecha_Nacimiento': [self.svFDN.get()],
            'Grupo_Sanguineo': [self.svGS.get()],
            'Rh': [self.svRH.get()],
            'Direccion': [self.svDireccion.get()],
            'Ocupacion': [self.svOcup.get()],
            'Datos_Padre': [self.svDpadre.get()],
            'DNI_Padre': [self.svDNIp.get()],
            'Telefono_Padre': [self.svTelefP.get()],
            'Datos_Madre': [self.svDMadre.get()],
            'DNI_Madre': [self.svDNIMadre.get()],
            'Telefono_Madre': [self.svTelefonoMadre.get()],
            'Datos_Apoderado': [self.svDatosApo.get()],
            'DNI_Apoderado': [self.svDNIDDA.get()],
            'Telefono_Apoderado': [self.svTelefonoApoderado.get()],
            'Vinculo_Apoderado': [self.svVinculo.get()],
            'Esquema_de_Vacunas': [vacunas_seleccionadas],
            'Antecedentes_Personales': [self.svAntecedentesP.get()],
            'Antecedentes_Familiares': [self.svAntecedentesF.get()],
            'RAM_Alergias': [self.svRA.get()],
            'Motivo_Consulta': [self.svMC.get()],
            'Forma_Inicio': [self.svFdI.get()],
            'Tiempo_Enfermedad': [self.svTdE.get()],
            'Signos_Sintomas_Principales': [self.svSySP.get()],
            'Frecuencia_Cardiaca': [self.svFC.get()],
            'Frecuencia_Respiratoria': [self.svFR.get()],
            'Presion_Arterial': [self.svPresionA.get()],
            'Temperatura': [self.svTC.get()],
            'Peso': [self.svPeso.get()],
            'Talla': [self.svTalla.get()],
        }

        # Crear un DataFrame de pandas
        df = pd.DataFrame(datos)

        # Intentar cargar un DataFrame existente si el archivo ya existe
        try:
            df_existente = pd.read_csv('datos_Niños.csv')
        except FileNotFoundError:
            df_existente = pd.DataFrame()

        # Concatenar el DataFrame existente con el nuevo DataFrame (df en lugar de DFAState)
        df_final = pd.concat([df_existente, df], ignore_index=True)

        # Guardar el DataFrame combinado en el archivo CSV
        df_final.to_csv('datos_Niños.csv', index=False)
        print('Datos agregados correctamente en el archivo CSV.')
        
        self.limpiar_datos()
        self.load_data_to_table()

    def load_data_to_table(self):
        # Intentar cargar el archivo CSV existente
        try:
            df = pd.read_csv('datos_Niños.csv')
        except FileNotFoundError:
            print("El archivo 'datos_Niños.csv' no se encuentra.")

        # Rellenar NaN con un valor específico (por ejemplo, cadena vacía)
        df = df.fillna('')

        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.table.get_children():
            self.table.delete(item)

        # Insertar los datos en la tabla
        for index, row in df.iterrows():
            self.table.insert("", "end", values=row.tolist()[0:]) 
        
    def eliminar_seleccionado(self):
        # Obtener las filas seleccionadas
        seleccion = self.table.selection()

        if not seleccion:
            print("Por favor, selecciona al menos una fila para eliminar.")
            return

        try:
            # Intentar cargar el DataFrame existente
            self.df = pd.read_csv('datos_Niños.csv')
        except FileNotFoundError:
            print("El archivo 'datos_Niños.csv' no se encuentra.")
            return

        # Eliminar las filas seleccionadas del DataFrame
        self.df = self.df.drop(self.table.index(seleccion), axis=0)

        # Limpiar la tabla antes de cargar nuevos datos
        for item in self.table.get_children():
            self.table.delete(item)

        # Rellenar valores nulos con cadena vacía
        self.df = self.df.fillna('')

        # Insertar los datos actualizados en la tabla
        for index, row in self.df.iterrows():
            self.table.insert("", "end", values=row.tolist())

        # Guardar el DataFrame actualizado en el archivo CSV
        self.df.to_csv('datos_Niños.csv', index=False)
        print('Datos eliminados correctamente en el archivo CSV.')

    def search_data(self):
        # Obtener el valor ingresado en el Entry
        search_value = self.svBuscar.get()

        # Limpiar la tabla
        for item in self.table.get_children():
            self.table.delete(item)

        # Cargar datos desde el archivo CSV
        try:
            df = pd.read_csv('datos_Niños.csv')
        except FileNotFoundError:
            print("El archivo 'datos_Niños.csv' no se encuentra.")

        # Rellenar NaN con un valor específico (por ejemplo, cadena vacía)
        df = df.fillna('')

        # Buscar en los datos y actualizar la tabla
        for index, row in df.iterrows():
            # Convertir cada valor a una cadena y buscar la coincidencia
            if any(search_value.lower() in str(value).lower() for value in row):
                self.table.insert("", "end", values=row.tolist())

    def verificar_y_cargar_tabla(self):
        # Verificar si svBuscar o EntryBuscar está vacío
        if not self.svBuscar.get():
            # Si está vacío, cargar la tabla con todos los datos originales
            self.load_data_to_table()
            return

    def exportar_a_excel(self):
        # Obtener los datos de la tabla
        datos_tabla = []
        for iid in self.table.get_children():
            valores = [self.table.item(iid, 'values')[0]]  # Obtener el ID
            valores.extend(self.table.item(iid, 'values')[1:])  # Obtener los demás valores
            datos_tabla.append(valores)

        # Obtener los encabezados de las columnas
        encabezados = [self.table.heading(col)["text"] for col in self.table["columns"]]

        # Crear un DataFrame de pandas con los datos y encabezados
        df = pd.DataFrame(datos_tabla, columns=encabezados)

        # Pedir al usuario que seleccione la ubicación y el nombre del archivo
        archivo_guardado = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Archivos Excel", "*.xlsx"), ("Todos los archivos", "*.*")],
            title="Guardar archivo Excel"
        )

        # Verificar si el usuario seleccionó un archivo
        if archivo_guardado:
            # Guardar el DataFrame como un archivo Excel
            df.to_excel(archivo_guardado, index=False)

    def importar_desde_excel(importar_datos_nuevos):
        pass

