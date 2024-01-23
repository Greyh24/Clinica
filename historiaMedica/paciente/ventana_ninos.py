import tkinter as tk
from tkcalendar import DateEntry
from tkinter import ttk
from time import strftime

class VentanaNinos(tk.Frame):
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

        # Configurar eventos de desplazamiento
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        # Llamar al método camposPacienteNiño dentro del canvas
        self.camposPacienteNiño()

    def on_canvas_configure(self, event):
        # Configurar la región de desplazamiento del canvas cuando cambia el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_frame_configure(self, event):
        # Configurar la región de desplazamiento del frame interior cuando cambia el tamaño
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

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
    
    def camposPacienteNiño(self):
       
        #labels
        self.lblHC =tk.Label(self.scrollable_frame, text='Historia Clinica: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblHC.grid(column=2, row=0, padx=0, pady=5)

        self.lblMd =tk.Label(self.scrollable_frame, text='Médico: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblMd.grid(column=0, row=1, padx=0, pady=0)

        self.lblEspe =tk.Label(self.scrollable_frame, text='Especialidad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblEspe.grid(column=2, row=1, padx=0, pady=0)

        self.lblFDA =tk.Label(self.scrollable_frame, text='Fecha de Atención: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblFDA.grid(column=0, row=2, padx=0, pady=0)

        self.lblHDA =tk.Label(self.scrollable_frame, text='Hora de Atención: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblHDA.grid(column=2, row=2, padx=0, pady=5)
        
        self.lblDA =tk.Label(self.scrollable_frame, text='DATOS GENERALES: ',font=('ARIAL',12,'bold'), bg='#CDD8FF')
        self.lblDA.grid(column=0, row=3, padx=0, pady=5)

        self.lblPaci =tk.Label(self.scrollable_frame, text='Paciente: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblPaci.grid(column=0, row=4, padx=0, pady=5)

        self.lblDNI =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDNI.grid(column=2, row=4, padx=0, pady=5)

        self.lblSexo =tk.Label(self.scrollable_frame, text='Sexo: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblSexo.grid(column=4, row=4, padx=0, pady=5)

        self.lbledad =tk.Label(self.scrollable_frame, text='Edad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lbledad.grid(column=0, row=5, padx=0, pady=5)

        self.lblFDN =tk.Label(self.scrollable_frame, text='Fecha de nacimiento: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblFDN.grid(column=2, row=5, padx=0, pady=5)
        
        self.lblGS =tk.Label(self.scrollable_frame, text='Grupo Sanguineo: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblGS.grid(column=4, row=5, padx=0, pady=5)

        self.lblRH =tk.Label(self.scrollable_frame, text='Rh: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblRH.grid(column=0, row=6, padx=0, pady=5)

        self.lblDireccion =tk.Label(self.scrollable_frame, text='Dirección: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDireccion.grid(column=2, row=6, padx=0, pady=5)

        self.lblOcup =tk.Label(self.scrollable_frame, text='Ocupación: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblOcup.grid(column=4, row=6, padx=0, pady=5)

        self.lblDPYOA =tk.Label(self.scrollable_frame, text='DATOS DE LOS PADRES Y/O APODERADO: ',font=('ARIAL',12,'bold'), bg='#CDD8FF')
        self.lblDPYOA.grid(column=0, row=7, padx=0, pady=5)
        
        self.lblDpadre =tk.Label(self.scrollable_frame, text='Datos del Padre: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDpadre.grid(column=0, row=8, padx=0, pady=5)

        self.lblDNIp =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDNIp.grid(column=2, row=8, padx=0, pady=5)

        self.lblTelefP =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTelefP.grid(column=4, row=8, padx=0, pady=5)

        self.lblDMadre =tk.Label(self.scrollable_frame, text='Datos de la Madre: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDMadre.grid(column=0, row=9, padx=0, pady=5)

        self.lblDNIMadre =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDNIMadre.grid(column=2, row=9, padx=0, pady=5)

        self.lblTelefonoMadre =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTelefonoMadre.grid(column=4, row=9, padx=0, pady=5)

        self.lblDatosApo =tk.Label(self.scrollable_frame, text='Datos del Apoderado: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDatosApo.grid(column=0, row=10, padx=0, pady=5)

        self.lblDNIDDA =tk.Label(self.scrollable_frame, text='DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblDNIDDA.grid(column=2, row=10, padx=0, pady=5)

        self.lblTelefonoApoderado =tk.Label(self.scrollable_frame, text='Telefono: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTelefonoApoderado.grid(column=4, row=10, padx=0, pady=5)

        self.lblVinculo =tk.Label(self.scrollable_frame, text='Vinculo con el menor: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblVinculo.grid(column=0, row=11, padx=0, pady=5)

        self.lblESQUEMAV =tk.Label(self.scrollable_frame, text='ESQUEMA DE VACUNACIÓN: ',font=('ARIAL',12,'bold'), bg='#CDD8FF')
        self.lblESQUEMAV.grid(column=0, row=12, padx=0, pady=5)
        
        self.lblOTROS =tk.Label(self.scrollable_frame, text='Otros: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblOTROS.grid(column=0, row=16, padx=0, pady=5)

        self.lblAntecedentes =tk.Label(self.scrollable_frame, text='ANTECEDENTE: ',font=('ARIAL',12,'bold'), bg='#CDD8FF')
        self.lblAntecedentes.grid(column=0, row=17, padx=0, pady=5)

        self.lblAntecedentesP =tk.Label(self.scrollable_frame, text='Antecedentes Personales: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblAntecedentesP.grid(column=0, row=18, padx=0, pady=5)

        self.lblAntecedentesF =tk.Label(self.scrollable_frame, text='Antecedentes Familiares: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblAntecedentesF.grid(column=2, row=18, padx=0, pady=5)

        self.lblRA =tk.Label(self.scrollable_frame, text='RAM / Alergias: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblRA.grid(column=4, row=18, padx=0, pady=5)

        self.lblANAMNESIS =tk.Label(self.scrollable_frame, text='ANAMNESIS: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblANAMNESIS.grid(column=0, row=19, padx=0, pady=5)

        self.lblMC =tk.Label(self.scrollable_frame, text='Motivo de consulta: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblMC.grid(column=0, row=20, padx=0, pady=5)

        self.lblFdI =tk.Label(self.scrollable_frame, text='Forma de Inicio: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblFdI.grid(column=2, row=20, padx=0, pady=5)

        self.lblTdE =tk.Label(self.scrollable_frame, text='Tiempo de enfermedad: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTdE.grid(column=0, row=21, padx=0, pady=5)

        self.lblSySP =tk.Label(self.scrollable_frame, text='Signos y síntomas principales: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblSySP.grid(column=2, row=21, padx=0, pady=5)

        self.lblExamenF =tk.Label(self.scrollable_frame, text='EXAMEN FÍSICO: ',font=('ARIAL',12,'bold'), bg='#CDD8FF')
        self.lblExamenF.grid(column=0, row=22, padx=0, pady=5)

        self.lblFC =tk.Label(self.scrollable_frame, text='Frecuencia Cardíaca (x min): ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblFC.grid(column=0, row=23, padx=0, pady=5)

        self.lblFR =tk.Label(self.scrollable_frame, text='Frecuencia Respiratoria (x min): ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblFR.grid(column=2, row=23, padx=0, pady=5)

        self.lblPresionA =tk.Label(self.scrollable_frame, text='Presión Arterial (mmHg): ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblPresionA.grid(column=0, row=24, padx=0, pady=5)

        self.lblTC =tk.Label(self.scrollable_frame, text='Tº (ºC): ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTC.grid(column=2, row=24, padx=0, pady=5)

        self.lblPeso =tk.Label(self.scrollable_frame, text='Peso: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblPeso.grid(column=0, row=25, padx=0, pady=5)

        self.lblTalla =tk.Label(self.scrollable_frame, text='Talla: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblTalla.grid(column=2, row=25, padx=0, pady=5)

        self.lblBhc =tk.Label(self.scrollable_frame, text='Buscar por Hc: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblBhc.grid(column=0, row=27, padx=0, pady=5)

        self.lblBdni =tk.Label(self.scrollable_frame, text='Buscar por DNI: ',font=('ARIAL',10,'bold'), bg='#CDD8FF')
        self.lblBdni.grid(column=0, row=28, padx=0, pady=5)

        #entry
        self.svHC = tk.StringVar()
        self.entryHC = tk.Entry(self.scrollable_frame, textvariable= self.svHC,width=20, font=('ARIAL',10))
        self.entryHC.grid(column=3, row=0, padx=0, pady=5)

        self.svMd = tk.StringVar()
        self.entryMd = tk.Entry(self.scrollable_frame, textvariable= self.svMd,width=20, font=('ARIAL',10))
        self.entryMd.grid(column=1, row=1, padx=0, pady=5)

        self.sveEspe = tk.StringVar()
        self.entryEspe = tk.Entry(self.scrollable_frame, textvariable= self.sveEspe,width=20, font=('ARIAL',10))
        self.entryEspe.grid(column=3, row=1, padx=0, pady=5)

        self.svFDA = tk.StringVar()
        self.entryFDA = DateEntry(self.scrollable_frame, textvariable= self.svFDA,width=20, font=('ARIAL',10))
        self.entryFDA.grid(column=1, row=2, padx=0, pady=5)

        self.svHDA = tk.StringVar()
        self.entryHDA = ttk.Entry(self.scrollable_frame, textvariable=self.svHDA, width=20, font=('ARIAL', 10))
        self.entryHDA.grid(column=3, row=2, padx=0, pady=5)
        self.actualizar_hora()

        self.svPaci = tk.StringVar()
        self.entryPaci = tk.Entry(self.scrollable_frame, textvariable= self.svPaci,width=20, font=('ARIAL',10))
        self.entryPaci.grid(column=1, row=4, padx=0, pady=5)
        
        self.svDNI = tk.StringVar()
        self.entryDNI = tk.Entry(self.scrollable_frame, textvariable= self.svDNI,width=20, font=('ARIAL',10))
        self.entryDNI.grid(column=3, row=4, padx=0, pady=5)

        # checkboxes para el género
        self.svsexo_m = tk.IntVar()
        self.checkbox_masculino = tk.Checkbutton(self.scrollable_frame, text='H', variable=self.svsexo_m, font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_masculino.grid(column=5, row=4, padx=(0,1), pady=5)

        self.svsexo_f = tk.IntVar()
        self.checkbox_femenino = tk.Checkbutton(self.scrollable_frame, text='M', variable=self.svsexo_f, font=('ARIAL', 10, 'bold'), bg='#CDD8FF')
        self.checkbox_femenino.grid(column=5, row=4, padx=(90, 0), pady=5)

        self.svedad = tk.StringVar()
        self.entryedad = tk.Entry(self.scrollable_frame, textvariable= self.svedad,width=20, font=('ARIAL',10))
        self.entryedad.grid(column=1, row=5, padx=0, pady=5)

        self.svFDN = tk.StringVar()
        self.entryFDN = DateEntry(self.scrollable_frame, textvariable= self.svFDN,width=20, font=('ARIAL',10))
        self.entryFDN.grid(column=3, row=5, padx=0, pady=5)

        self.svGS = tk.StringVar()
        self.entryGS = tk.Entry(self.scrollable_frame, textvariable= self.svGS,width=20, font=('ARIAL',10))
        self.entryGS.grid(column=5, row=5, padx=0, pady=5)

        self.svRH = tk.StringVar()
        self.entryRH = tk.Entry(self.scrollable_frame, textvariable= self.svRH,width=20, font=('ARIAL',10))
        self.entryRH.grid(column=1, row=6, padx=0, pady=5)

        self.svDireccion = tk.StringVar()
        self.entryDireccion = tk.Entry(self.scrollable_frame, textvariable= self.svDireccion,width=20, font=('ARIAL',10))
        self.entryDireccion.grid(column=3, row=6, padx=0, pady=5)

        self.svOcup = tk.StringVar()
        self.entryOcup = tk.Entry(self.scrollable_frame, textvariable= self.svOcup,width=20, font=('ARIAL',10))
        self.entryOcup.grid(column=5, row=6, padx=0, pady=5)

        self.svDpadre = tk.StringVar()
        self.entryDpadre = tk.Entry(self.scrollable_frame, textvariable= self.svDpadre,width=20, font=('ARIAL',10))
        self.entryDpadre.grid(column=1, row=8, padx=0, pady=5)
       
        self.svDNIp = tk.StringVar()
        self.entryDNIp = tk.Entry(self.scrollable_frame, textvariable= self.svDNIp,width=20, font=('ARIAL',10))
        self.entryDNIp.grid(column=3, row=8, padx=0, pady=5)

        self.svTelefP = tk.StringVar()
        self.entryTelefP = tk.Entry(self.scrollable_frame, textvariable= self.svTelefP,width=20, font=('ARIAL',10))
        self.entryTelefP.grid(column=5, row=8, padx=0, pady=5)

        self.svDMadre = tk.StringVar()
        self.entryDMadre = tk.Entry(self.scrollable_frame, textvariable= self.svDMadre,width=20, font=('ARIAL',10))
        self.entryDMadre.grid(column=1, row=9, padx=0, pady=5)

        self.svDNIMadre = tk.StringVar()
        self.entryDNIMadre = tk.Entry(self.scrollable_frame, textvariable= self.svDNIMadre,width=20, font=('ARIAL',10))
        self.entryDNIMadre.grid(column=3, row=9, padx=0, pady=5)

        self.svTelefonoMadre = tk.StringVar()
        self.entryTelefonoMadre = tk.Entry(self.scrollable_frame, textvariable= self.svTelefonoMadre,width=20, font=('ARIAL',10))
        self.entryTelefonoMadre.grid(column=5, row=9, padx=0, pady=5)

        self.svDatosApo = tk.StringVar()
        self.entryDatosApo = tk.Entry(self.scrollable_frame, textvariable= self.svDatosApo,width=20, font=('ARIAL',10))
        self.entryDatosApo.grid(column=1, row=10, padx=0, pady=5)

        self.svDNIDDA = tk.StringVar()
        self.entryDNIDDA = tk.Entry(self.scrollable_frame, textvariable= self.svDNIDDA,width=20, font=('ARIAL',10))
        self.entryDNIDDA.grid(column=3, row=10, padx=0, pady=5)

        self.svTelefonoApoderado = tk.StringVar()
        self.entryTelefonoApoderado = tk.Entry(self.scrollable_frame, textvariable= self.svTelefonoApoderado,width=20, font=('ARIAL',10))
        self.entryTelefonoApoderado.grid(column=5, row=10, padx=0, pady=5)

        self.svVinculo = tk.StringVar()
        self.entryVinculo = tk.Entry(self.scrollable_frame, textvariable= self.svVinculo,width=20, font=('ARIAL',10))
        self.entryVinculo.grid(column=1, row=11, padx=0, pady=5)
        
        self.svBCG = tk.BooleanVar()
        self.entryBCG = tk.Checkbutton(self.scrollable_frame, text="BCG", variable=self.svBCG, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryBCG.grid(column=0, row=13, padx=0, pady=5)

        self.svHVB = tk.BooleanVar()
        self.entryHVB = tk.Checkbutton(self.scrollable_frame, text="HVB", variable=self.svHVB, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryHVB.grid(column=1, row=13, padx=0, pady=5)

        self.svPENTAVALENTE = tk.BooleanVar()
        self.entryPENTAVALENTE = tk.Checkbutton(self.scrollable_frame, text="PENTAVALENTE", variable=self.svPENTAVALENTE, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryPENTAVALENTE.grid(column=2, row=13, padx=0, pady=5)

        self.svANTIPOLIO = tk.BooleanVar()
        self.entryANTIPOLIO = tk.Checkbutton(self.scrollable_frame, text="ANTIPOLIO", variable=self.svANTIPOLIO, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTIPOLIO.grid(column=3, row=13, padx=0, pady=5)

        self.svANTINEUMOCOCICA = tk.BooleanVar()
        self.entryANTINEUMOCOCICA = tk.Checkbutton(self.scrollable_frame, text="ANTINEUMOCOCICA", variable=self.svANTINEUMOCOCICA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTINEUMOCOCICA.grid(column=4, row=13, padx=0, pady=5)

        self.svDT = tk.BooleanVar()
        self.entryDT = tk.Checkbutton(self.scrollable_frame, text="DT", variable=self.svDT, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryDT.grid(column=0, row=14, padx=0, pady=5)

        self.svSPR = tk.BooleanVar()
        self.entrySPR = tk.Checkbutton(self.scrollable_frame, text="SPR", variable=self.svSPR, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entrySPR.grid(column=1, row=14, padx=0, pady=5)

        self.svROTAVIRUS = tk.BooleanVar()
        self.entryROTAVIRUS = tk.Checkbutton(self.scrollable_frame, text="ROTAVIRUS", variable=self.svROTAVIRUS, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryROTAVIRUS.grid(column=2, row=14, padx=0, pady=5)

        self.svINFLUENZA_PED = tk.BooleanVar()
        self.entryINFLUENZA_PED = tk.Checkbutton(self.scrollable_frame, text="INFLUENZA PED.", variable=self.svINFLUENZA_PED, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryINFLUENZA_PED.grid(column=3, row=14, padx=0, pady=5)

        self.svVARICELA = tk.BooleanVar()
        self.entryVARICELA = tk.Checkbutton(self.scrollable_frame, text="VARICELA", variable=self.svVARICELA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryVARICELA.grid(column=4, row=14, padx=0, pady=5)

        self.svDPR = tk.BooleanVar()
        self.entryDPR = tk.Checkbutton(self.scrollable_frame, text="DPR", variable=self.svDPR, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryDPR.grid(column=0, row=15, padx=0, pady=5)

        self.svAPO = tk.BooleanVar()
        self.entryAPO = tk.Checkbutton(self.scrollable_frame, text="APO", variable=self.svAPO, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryAPO.grid(column=1, row=15, padx=0, pady=5)

        self.svANTIAMARILICA = tk.BooleanVar()
        self.entryANTIAMARILICA = tk.Checkbutton(self.scrollable_frame, text="ANTIAMARILICA", variable=self.svANTIAMARILICA, width=20, font=('ARIAL', 10), bg='#CDD8FF')
        self.entryANTIAMARILICA.grid(column=2, row=15, padx=0, pady=5)

        self.svOTROS = tk.StringVar()
        self.entryOTROS = tk.Entry(self.scrollable_frame, textvariable= self.svOTROS,width=20, font=('ARIAL',10))
        self.entryOTROS.grid(column=1, row=16, padx=0, pady=5)
 
        self.svAntecedentesP = tk.StringVar()
        self.entryAntecedentesP = tk.Entry(self.scrollable_frame, textvariable= self.svAntecedentesP,width=20, font=('ARIAL',10))
        self.entryAntecedentesP.grid(column=1, row=18, padx=0, pady=5)
        
        self.svAntecedentesF = tk.StringVar()
        self.entryAntecedentesF = tk.Entry(self.scrollable_frame, textvariable= self.svAntecedentesF,width=20, font=('ARIAL',10))
        self.entryAntecedentesF.grid(column=3, row=18, padx=0, pady=5)

        self.svRA = tk.StringVar()
        self.entryRA = tk.Entry(self.scrollable_frame, textvariable= self.svRA,width=20, font=('ARIAL',10))
        self.entryRA.grid(column=5, row=18, padx=0, pady=5)

        self.svMC = tk.StringVar()
        self.entryMC = tk.Entry(self.scrollable_frame, textvariable= self.svMC,width=20, font=('ARIAL',10))
        self.entryMC.grid(column=1, row=20, padx=0, pady=5)

        self.svFdI = tk.StringVar()
        self.entryFdI = tk.Entry(self.scrollable_frame, textvariable= self.svFdI,width=20, font=('ARIAL',10))
        self.entryFdI.grid(column=3, row=20, padx=0, pady=5)

        self.svTdE = tk.StringVar()
        self.entryTdE = tk.Entry(self.scrollable_frame, textvariable= self.svTdE,width=20, font=('ARIAL',10))
        self.entryTdE.grid(column=1, row=21, padx=0, pady=5)

        self.svSySP = tk.StringVar()
        self.entrySySP = tk.Entry(self.scrollable_frame, textvariable= self.svSySP,width=20, font=('ARIAL',10))
        self.entrySySP.grid(column=3, row=21, padx=0, pady=5)

        self.svFC = tk.StringVar()
        self.entryFC = tk.Entry(self.scrollable_frame, textvariable= self.svFC,width=20, font=('ARIAL',10))
        self.entryFC.grid(column=1, row=23, padx=0, pady=5)

        self.svFR = tk.StringVar()
        self.entryFR = tk.Entry(self.scrollable_frame, textvariable= self.svFR,width=20, font=('ARIAL',10))
        self.entryFR.grid(column=3, row=23, padx=0, pady=5)

        self.svPresionA = tk.StringVar()
        self.entryPresionA = tk.Entry(self.scrollable_frame, textvariable= self.svPresionA,width=20, font=('ARIAL',10))
        self.entryPresionA.grid(column=1, row=24, padx=0, pady=5)

        self.svTC = tk.StringVar()
        self.entryTC = tk.Entry(self.scrollable_frame, textvariable= self.svTC,width=20, font=('ARIAL',10))
        self.entryTC.grid(column=3, row=24, padx=0, pady=5)

        self.svPeso = tk.StringVar()
        self.entryPeso = tk.Entry(self.scrollable_frame, textvariable= self.svPeso,width=20, font=('ARIAL',10))
        self.entryPeso.grid(column=1, row=25, padx=0, pady=5)

        self.svTalla = tk.StringVar()
        self.entryTalla = tk.Entry(self.scrollable_frame, textvariable= self.svTalla,width=20, font=('ARIAL',10))
        self.entryTalla.grid(column=3, row=25, padx=0, pady=5)

        self.svBhc = tk.StringVar()
        self.entryBhc = tk.Entry(self.scrollable_frame, textvariable= self.svBhc,width=20, font=('ARIAL',10))
        self.entryBhc.grid(column=1, row=27, padx=0, pady=5)

        self.svBdni = tk.StringVar()
        self.entryBdni = tk.Entry(self.scrollable_frame, textvariable= self.svBdni,width=20, font=('ARIAL',10))
        self.entryBdni.grid(column=1, row=28, padx=0, pady=5)
        
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
        self.entryDireccion.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryOcup.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDpadre.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDMadre.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryDatosApo.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryVinculo.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryOTROS.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryAntecedentesP.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryAntecedentesF.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryRA.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryMC.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryFdI.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entryTdE.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))
        self.entrySySP.config(validate="key", validatecommand=(self.root.register(self.validate_letter), '%P'))

        #BOTON
        self.btnGuardar = tk.Button(self.scrollable_frame, text='Guardar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#158645',cursor='hand2', activebackground='#35BD6F') 
        self.btnGuardar.grid(column=0, row=26, padx=0, pady=5)

        self.btnModificar = tk.Button(self.scrollable_frame, text='Modificar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#1658A2',cursor='hand2', activebackground='#3D69F0')
        self.btnModificar.grid(column=1, row=26, padx=0, pady=5)

        self.btnEliminar = tk.Button(self.scrollable_frame, text='Eliminar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#D32F2F',cursor='hand2', activebackground='#E72D40')
        self.btnEliminar.grid(column=2, row=26, padx=0, pady=5)

        self.btnImportar = tk.Button(self.scrollable_frame, text='Importar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#CF811E',cursor='hand2', activebackground='#E72D40')
        self.btnImportar.grid(column=3, row=26, padx=0, pady=5)

        self.btnExportar = tk.Button(self.scrollable_frame, text='Exportar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#CF811E',cursor='hand2', activebackground='#E72D40')
        self.btnExportar.grid(column=4, row=26, padx=15, pady=5)

        self.btnBuscarhc = tk.Button(self.scrollable_frame, text='Buscar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#0F1010',cursor='hand2', activebackground='#FFFEFE')
        self.btnBuscarhc.grid(column=2, row=27, padx=15, pady=5)

        self.btnBuscardni = tk.Button(self.scrollable_frame, text='Buscar',width=10, font=('Arial',10,'bold'), fg='#FFFEFE', bg='#0F1010',cursor='hand2', activebackground='#FFFEFE')
        self.btnBuscardni.grid(column=2, row=28, padx=0, pady=5)
