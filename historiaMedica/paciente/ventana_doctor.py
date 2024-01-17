import tkinter as tk
from tkinter import filedialog
from tkcalendar import DateEntry
from tkinter import ttk
from time import strftime
from PIL import Image, ImageTk

class VentanaDiagnosticoMedico(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=620)
        self.root = root

        self.root.title("Diagnóstico Médico")
        self.canvas = tk.Canvas(self, bg='#8C9BBA', width=1300, height=620)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollable_frame = tk.Frame(self.canvas, bg='#8C9BBA')
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.scrollbar_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)

        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)

        datos_frame = tk.Frame(self.scrollable_frame, bg='#8C9BBA')
        datos_frame.grid(column=2, row=1, padx=5, pady=5, sticky='ew')

        self.camposDiagnosticoMedico()

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
        self.entryHoraP.delete(0, tk.END)
        self.entryHoraP.insert(0, hora_actual)

    def actualizar_hora2(self):
        hora_actual = strftime('%H:%M %p')
        self.entryHoraAT.delete(0, tk.END)
        self.entryHoraAT.insert(0, hora_actual)  

    def actualizar_hora3(self):
        hora_actual = strftime('%H:%M %p')
        self.entryHoraD.delete(0, tk.END)
        self.entryHoraD.insert(0, hora_actual)   

    def mostrar_imagen(self, event, contenedor):
        # Abrir el cuadro de diálogo de selección de archivo
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])

        # Verificar si se seleccionó una imagen
        if ruta_imagen:
            imagen = Image.open(ruta_imagen)
            self.mostrar_imagen_en_label(imagen, contenedor)

    def mostrar_imagen_en_label(self, imagen, contenedor):
        imagen.thumbnail((150, 100))
        imagen_tk = ImageTk.PhotoImage(imagen)

        contenedor.config(image=imagen_tk)
        contenedor.image = imagen_tk  # Mantener una referencia para evitar que sea eliminado

        if contenedor == self.contenedor_MedRes:
            self.imagen_tk_MedRes = imagen_tk
        elif contenedor == self.contenedor_ExaAdi:
            self.imagen_tk_ExaAdi = imagen_tk

    def mostrar_cuadro_dialogo(self, event):
        # Abrir el cuadro de diálogo de selección de archivo
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])

        # Verificar si se seleccionó una imagen
        if ruta_imagen:
            # Agregar la referencia de la imagen a la lista
            self.lista_imagenes.insert(tk.END, ruta_imagen)

            # Seleccionar la última imagen agregada
            self.lista_imagenes.selection_clear(0, tk.END)
            self.lista_imagenes.selection_set(tk.END)

            # Mostrar la última imagen en el contenedor
            self.seleccionar_imagen()

    def seleccionar_imagen(self, event=None):
        # Obtener el índice de la imagen seleccionada en el Listbox
        seleccion = self.lista_imagenes.curselection()

        if seleccion:
            indice = int(seleccion[0])
            ruta_imagen = self.lista_imagenes.get(indice)

            # Abrir la imagen con Pillow
            imagen = Image.open(ruta_imagen)

            self.mostrar_imagen_en_label(imagen, self.contenedor_ExaAdi)

    def camposDiagnosticoMedico(self):
        self.lblDM = tk.Label(self.scrollable_frame, text='Diagnóstico Médico: ', font=('ARIAL', 24, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblDM.grid(column=2, row=0, columnspan=3, padx=5, pady=5)

        self.lblPaci = tk.Label(self.scrollable_frame, text='Paciente: ', font=('ARIAL', 14, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblPaci.grid(column=0, row=1, padx=0, pady=5)

        self.lblEdad = tk.Label(self.scrollable_frame, text='Edad: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblEdad.grid(column=0, row=2, padx=0, pady=5)

        self.svEdad = tk.StringVar()
        self.entryEdad = tk.Entry(self.scrollable_frame, textvariable=self.svEdad, width=20, font=('ARIAL', 10,'bold'))
        self.entryEdad.grid(column=1, row=2, padx=0, pady=5)
        
        self.lblSex = tk.Label(self.scrollable_frame, text='Sexo: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblSex.grid(column=0, row=3, padx=0, pady=5)

        self.svSex = tk.StringVar()
        self.entrySex = tk.Entry(self.scrollable_frame, textvariable=self.svSex, width=20, font=('ARIAL', 10,'bold'))
        self.entrySex.grid(column=1, row=3, padx=0, pady=5)
        
        self.lblDir = tk.Label(self.scrollable_frame, text='Dirección: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDir.grid(column=0, row=4, padx=5, pady=5)

        self.svDir = tk.StringVar()
        self.entryDir = tk.Entry(self.scrollable_frame, textvariable=self.svDir, width=20, font=('ARIAL', 10,'bold'))
        self.entryDir.grid(column=1, row=4, padx=0, pady=5)

        self.lblDis = tk.Label(self.scrollable_frame, text='Distrito: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDis.grid(column=0, row=5, padx=5, pady=5)

        self.svDis = tk.StringVar()
        self.entryDis = tk.Entry(self.scrollable_frame, textvariable=self.svDis, width=20, font=('ARIAL', 10,'bold'))
        self.entryDis.grid(column=1, row=5, padx=0, pady=5)

        self.lblResp = tk.Label(self.scrollable_frame, text='Responsable: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblResp.grid(column=0, row=6, padx=5, pady=5)

        self.svResp = tk.StringVar()
        self.entryResp = tk.Entry(self.scrollable_frame, textvariable=self.svResp, width=20, font=('ARIAL', 10,'bold'))
        self.entryResp.grid(column=1, row=6, padx=0, pady=5)

        self.lblMI = tk.Label(self.scrollable_frame, text='Modo de Ingreso: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblMI.grid(column=0, row=7, padx=5, pady=5)

        self.svMI = tk.StringVar()
        self.entryMI = tk.Entry(self.scrollable_frame, textvariable=self.svMI, width=20, font=('ARIAL', 10,'bold'))
        self.entryMI.grid(column=1, row=7, padx=0, pady=5)

        self.lblDNI = tk.Label(self.scrollable_frame, text='DNI: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDNI.grid(column=2, row=2, padx=5, pady=5)

        self.svDNI = tk.StringVar()
        self.entryDNI = tk.Entry(self.scrollable_frame, textvariable=self.svDNI, width=20, font=('ARIAL', 10,'bold'))
        self.entryDNI.grid(column=3, row=2, padx=0, pady=5)

        self.lblTrans = tk.Label(self.scrollable_frame, text='Transito: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTrans.grid(column=2, row=3, padx=5, pady=5)

        self.svTrans = tk.StringVar()
        self.entryTrans = tk.Entry(self.scrollable_frame, textvariable=self.svTrans, width=20, font=('ARIAL', 10,'bold'))
        self.entryTrans.grid(column=3, row=3, padx=0, pady=5)

        self.lblTseg = tk.Label(self.scrollable_frame, text='Tipo Seg: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTseg.grid(column=2, row=4, padx=5, pady=5)

        self.svTseg = tk.StringVar()
        self.entryTseg = tk.Entry(self.scrollable_frame, textvariable=self.svTseg, width=20, font=('ARIAL', 10,'bold'))
        self.entryTseg.grid(column=3, row=4, padx=0, pady=5)

        self.lblTel = tk.Label(self.scrollable_frame, text='Telefono: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTel.grid(column=2, row=5, padx=5, pady=5)

        self.svTel = tk.StringVar()
        self.entryTel = tk.Entry(self.scrollable_frame, textvariable=self.svTel, width=20, font=('ARIAL', 10,'bold'))
        self.entryTel.grid(column=3, row=5, padx=0, pady=5)

        self.lblFicha = tk.Label(self.scrollable_frame, text='Ficha: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblFicha.grid(column=4, row=2, padx=5, pady=5)

        self.svFicha = tk.StringVar()
        self.entryFicha = tk.Entry(self.scrollable_frame, textvariable=self.svFicha, width=20, font=('ARIAL', 10,'bold'))
        self.entryFicha.grid(column=5, row=2, padx=0, pady=5)

        self.lblfechaP = tk.Label(self.scrollable_frame, text='Fecha: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblfechaP.grid(column=4, row=3, padx=5, pady=5)

        self.svfechaP = tk.StringVar()
        self.entryfechaP = DateEntry(self.scrollable_frame, textvariable=self.svfechaP, width=20, font=('ARIAL', 10,'bold'))
        self.entryfechaP.grid(column=5, row=3, padx=0, pady=5)

        self.lblHoraP = tk.Label(self.scrollable_frame, text='Hora: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblHoraP.grid(column=4, row=4, padx=5, pady=5)

        self.svHoraP = tk.StringVar()
        self.entryHoraP = tk.Entry(self.scrollable_frame, textvariable=self.svHoraP, width=20, font=('ARIAL', 10,'bold'))
        self.entryHoraP.grid(column=5, row=4, padx=0, pady=5)
        self.actualizar_hora()

        self.lblHistoria = tk.Label(self.scrollable_frame, text='Historia: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
        self.lblHistoria.grid(column=4, row=5, padx=5, pady=5)

        self.svHistoria = tk.StringVar()
        self.entryHistoria = tk.Entry(self.scrollable_frame, textvariable=self.svHistoria, width=20, font=('ARIAL', 10,'bold'))
        self.entryHistoria.grid(column=5, row=5, padx=0, pady=5)

        # Insertar una línea de separación entre la fila 2 y la fila 3
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=8, columnspan=15, sticky="ew", pady=5)

        self.lblEsp = tk.Label(self.scrollable_frame, text='Especialidad: ', font=('ARIAL', 12, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblEsp.grid(column=0, row=9, padx=5, pady=5)

        self.svMedicina = tk.BooleanVar()
        self.entryMedicina = tk.Checkbutton(self.scrollable_frame, text="Medicina", variable=self.svMedicina, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryMedicina.grid(column=0, row=10, padx=0, pady=5)

        self.svPediatria = tk.BooleanVar()
        self.entryPediatria = tk.Checkbutton(self.scrollable_frame, text="Pediatria", variable=self.svPediatria, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryPediatria.grid(column=0, row=11, padx=0, pady=5)

        self.svCirugia = tk.BooleanVar()
        self.entryCirugia = tk.Checkbutton(self.scrollable_frame, text="Cirugia", variable=self.svCirugia, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryCirugia.grid(column=0, row=12, padx=0, pady=5)

        self.svGineco_OBS = tk.BooleanVar()
        self.entryGineco_OBS = tk.Checkbutton(self.scrollable_frame, text="Gineco OBS", variable=self.svGineco_OBS, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryGineco_OBS.grid(column=0, row=13, padx=0, pady=5)

        self.lblPD = tk.Label(self.scrollable_frame, text='Prioridad de Daño: ', font=('ARIAL', 12, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblPD.grid(column=1, row=9, padx=5, pady=5)

        self.svPriorid1 = tk.BooleanVar()
        self.entryPriorid1 = tk.Checkbutton(self.scrollable_frame, text="Prioridad I", variable=self.svPriorid1, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryPriorid1.grid(column=1, row=10, padx=0, pady=5)

        self.svPriorid2 = tk.BooleanVar()
        self.entryPriorid2 = tk.Checkbutton(self.scrollable_frame, text="Prioridad II", variable=self.svPriorid2, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryPriorid2.grid(column=1, row=11, padx=0, pady=5)

        self.svPriorid3 = tk.BooleanVar()
        self.entryPriorid3 = tk.Checkbutton(self.scrollable_frame, text="Prioridad III", variable=self.svPriorid3, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryPriorid3.grid(column=1, row=12, padx=0, pady=5)

        self.svPriorid4 = tk.BooleanVar()
        self.entryPriorid4 = tk.Checkbutton(self.scrollable_frame, text="Prioridad IV", variable=self.svPriorid4, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryPriorid4.grid(column=1, row=13, padx=0, pady=5)

        self.lblTA = tk.Label(self.scrollable_frame, text='Tipo de Accidente: ', font=('ARIAL', 12, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblTA.grid(column=2, row=9, padx=5, pady=5)

        self.lblAtrans = tk.Label(self.scrollable_frame, text='Accidente de Transito: ', font=('ARIAL', 11, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblAtrans.grid(column=2, row=10, padx=5, pady=5)

        self.svAtrop = tk.BooleanVar()
        self.entryAtrop = tk.Checkbutton(self.scrollable_frame, text="Atropello", variable=self.svAtrop, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryAtrop.grid(column=2, row=11, padx=0, pady=5)

        self.svChoque = tk.BooleanVar()
        self.entryChoque = tk.Checkbutton(self.scrollable_frame, text="Choque", variable=self.svChoque, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryChoque.grid(column=2, row=12, padx=0, pady=5)

        self.svDespiste = tk.BooleanVar()
        self.entryDespiste = tk.Checkbutton(self.scrollable_frame, text="Despiste", variable=self.svDespiste, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryDespiste.grid(column=2, row=13, padx=0, pady=5)

        self.svIncendio = tk.BooleanVar()
        self.entryIncendio = tk.Checkbutton(self.scrollable_frame, text="Incendio", variable=self.svIncendio, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryIncendio.grid(column=2, row=14, padx=0, pady=5)

        self.svAyF = tk.BooleanVar()
        self.entryAyF = tk.Checkbutton(self.scrollable_frame, text="Atropello y Fuga", variable=self.svAyF, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryAyF.grid(column=2, row=11, padx=0, pady=5)

        self.svCyF = tk.BooleanVar()
        self.entryCyF = tk.Checkbutton(self.scrollable_frame, text="Choque y Fuga", variable=self.svCyF, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryCyF.grid(column=2, row=12, padx=0, pady=5)

        self.svCaidaP = tk.BooleanVar()
        self.entryCaidaP = tk.Checkbutton(self.scrollable_frame, text="Caida de Pasajeros", variable=self.svCaidaP, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryCaidaP.grid(column=2, row=13, padx=0, pady=5)

        self.svVolcadura = tk.BooleanVar()
        self.entryVolcadura = tk.Checkbutton(self.scrollable_frame, text="Volcadura", variable=self.svVolcadura, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryVolcadura.grid(column=2, row=14, padx=0, pady=5)

        self.lblOtrosAT = tk.Label(self.scrollable_frame, text='Otros: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblOtrosAT.grid(column=2, row=15, padx=(0,0), pady=5)

        self.svOtrosAT = tk.StringVar()
        self.entryOtrosAT = tk.Entry(self.scrollable_frame, textvariable=self.svOtrosAT, width=5, font=('ARIAL', 10,'bold'))
        self.entryOtrosAT.grid(column=2, row=15, padx=(90,0), pady=5)

        self.lblFechaAT = tk.Label(self.scrollable_frame, text='Fecha: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblFechaAT.grid(column=0, row=14, padx=5, pady=5)

        self.svFechaAT = tk.StringVar()
        self.entryFechaAT = DateEntry(self.scrollable_frame, textvariable=self.svFechaAT, width=20, font=('ARIAL', 10,'bold'))
        self.entryFechaAT.grid(column=1, row=14, padx=0, pady=5)

        self.lblHoraAT = tk.Label(self.scrollable_frame, text='Hora: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblHoraAT.grid(column=0, row=15, padx=5, pady=5)

        self.svHoraAT = tk.StringVar()
        self.entryHoraAT = tk.Entry(self.scrollable_frame, textvariable=self.svHoraAT, width=20, font=('ARIAL', 10,'bold'))
        self.entryHoraAT.grid(column=1, row=15, padx=0, pady=5)
        self.actualizar_hora2()

        
        self.lblANAMNESIS = tk.Label(self.scrollable_frame, text='ANAMNESIS: ', font=('ARIAL', 12, 'bold'),fg='#ffffff', bg='#8C9BBA')
        self.lblANAMNESIS.grid(column=0, row=16, padx=5, pady=5)

        self.lblTipoE = tk.Label(self.scrollable_frame, text='Tiempo de Enfermedad: ', font=('ARIAL', 11, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTipoE.grid(column=0, row=17, padx=5, pady=5)

        self.svTipoE = tk.StringVar()
        self.entryTipoE = tk.Entry(self.scrollable_frame, textvariable=self.svTipoE, width=20, font=('ARIAL', 10,'bold'))
        self.entryTipoE.grid(column=1, row=17, padx=5, pady=5)

        self.lblMC = tk.Label(self.scrollable_frame, text='Motivo de Consulta: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblMC.grid(column=0, row=18, padx=5, pady=5)

        self.svMC = tk.StringVar()
        self.entryMC = tk.Entry(self.scrollable_frame, textvariable=self.svMC, width=127, font=('ARIAL', 10,'bold'))
        self.entryMC.grid(column=1, row=18, padx=0, pady=5, columnspan=6)

        self.lblAntecedentes = tk.Label(self.scrollable_frame, text='Antecedentes: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblAntecedentes.grid(column=0, row=19, padx=5, pady=5)

        self.svAntecedentes = tk.StringVar()
        self.entryAntecedentes = tk.Entry(self.scrollable_frame, textvariable=self.svAntecedentes, width=127, font=('ARIAL', 10,'bold'))
        self.entryAntecedentes.grid(column=1, row=19, padx=0, pady=5, columnspan=6)

        self.lblEClic = tk.Label(self.scrollable_frame, text='Examen Clínico: ', font=('ARIAL', 11, 'bold'),fg='black', bg='#8C9BBA')
        self.lblEClic.grid(column=0, row=20, padx=5, pady=5)

        self.lblPA = tk.Label(self.scrollable_frame, text='P.A ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblPA.grid(column=1, row=20, padx=(0,90), pady=5)

        self.svPA = tk.StringVar()
        self.entryPA = tk.Entry(self.scrollable_frame, textvariable=self.svPA, width=10, font=('ARIAL', 10,'bold'))
        self.entryPA.grid(column=1, row=20, padx=(10,0), pady=5)

        self.lblFC = tk.Label(self.scrollable_frame, text='FC ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblFC.grid(column=2, row=20, padx=(0,90), pady=5)

        self.svFC = tk.StringVar()
        self.entryFC = tk.Entry(self.scrollable_frame, textvariable=self.svFC, width=10, font=('ARIAL', 10,'bold'))
        self.entryFC.grid(column=2, row=20, padx=(10,0), pady=5)

        self.lblFR = tk.Label(self.scrollable_frame, text='FR ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblFR.grid(column=3, row=20, padx=(0,90), pady=5)

        self.svFR = tk.StringVar()
        self.entryFR = tk.Entry(self.scrollable_frame, textvariable=self.svFR, width=10, font=('ARIAL', 10,'bold'))
        self.entryFR.grid(column=3, row=20, padx=(10,0), pady=5)

        self.lblTº = tk.Label(self.scrollable_frame, text='Tº ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTº.grid(column=4, row=20, padx=(0,90), pady=5)

        self.svTº = tk.StringVar()
        self.entryTº = tk.Entry(self.scrollable_frame, textvariable=self.svTº, width=10, font=('ARIAL', 10,'bold'))
        self.entryTº.grid(column=4, row=20, padx=(10,0), pady=5)

        self.lblSO = tk.Label(self.scrollable_frame, text='SO ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblSO.grid(column=5, row=20, padx=(0,90), pady=5)

        self.svSO = tk.StringVar()
        self.entrySO = tk.Entry(self.scrollable_frame, textvariable=self.svSO, width=10, font=('ARIAL', 10,'bold'))
        self.entrySO.grid(column=5, row=20, padx=(10,0), pady=5)

        self.lblPeso = tk.Label(self.scrollable_frame, text='Peso ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblPeso.grid(column=6, row=20, padx=(0,110), pady=5)

        self.svPeso = tk.StringVar()
        self.entryPeso = tk.Entry(self.scrollable_frame, textvariable=self.svPeso, width=5, font=('ARIAL', 10,'bold'))
        self.entryPeso.grid(column=6, row=20, padx=(10,0), pady=5)

        self.lblExamenP = tk.Label(self.scrollable_frame, text='Examen Preferencial: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblExamenP.grid(column=0, row=21, padx=5, pady=5)

        self.svExamenP = tk.StringVar()
        self.entryExamenP = tk.Entry(self.scrollable_frame, textvariable=self.svExamenP, width=127, font=('ARIAL', 10,'bold'))
        self.entryExamenP.grid(column=1, row=21, padx=0, pady=5, columnspan=6)

        self.lblDdi = tk.Label(self.scrollable_frame, text='Diagnóstico de Ingreso: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDdi.grid(column=0, row=22, padx=0, pady=5)

        self.svDdi = tk.StringVar()
        self.entryDdi = tk.Entry(self.scrollable_frame, textvariable=self.svDdi, width=127, font=('ARIAL', 10,'bold'))
        self.entryDdi.grid(column=0, row=23, padx=5, pady=5, columnspan=5)

        self.lblCodCie = tk.Label(self.scrollable_frame, text='COD. CIE 10: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblCodCie.grid(column=5, row=22, padx=0, pady=5, columnspan=6)

        self.svCodCie = tk.StringVar()
        self.entryCodCie = tk.Entry(self.scrollable_frame, textvariable=self.svCodCie, width=30, font=('ARIAL', 10,'bold'))
        self.entryCodCie.grid(column=5, row=23, padx=5, pady=5, columnspan=6)


        # Insertar una línea de separación entre la fila 24 y la fila 26
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=24, columnspan=15, sticky="ew", pady=5)
        
        self.lblPlanT = tk.Label(self.scrollable_frame, text='Plan de Trabajo: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblPlanT.grid(column=0, row=25, padx=0, pady=5)
        
        self.lblHidrat = tk.Label(self.scrollable_frame, text='Hidratación: ', font=('ARIAL', 11, 'bold'),fg='black', bg='#8C9BBA')
        self.lblHidrat.grid(column=4, row=25, padx=0, pady=5)
        
        self.svHidratS = tk.BooleanVar()
        self.entryHidratS = tk.Checkbutton(self.scrollable_frame, text="Si", variable=self.svHidratS, width=5, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryHidratS.grid(column=5, row=25, padx=(0,20), pady=5)

        self.svHidratN = tk.BooleanVar()
        self.entryHidratN = tk.Checkbutton(self.scrollable_frame, text="No", variable=self.svHidratN, width=5, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryHidratN.grid(column=5, row=25, padx=(100,0), pady=5)

        self.lblExamA = tk.Label(self.scrollable_frame, text='Exámenes Auxiliares: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblExamA.grid(column=0, row=26, padx=5, pady=5)

        self.svLaboratorio = tk.BooleanVar()
        self.entryLaboratorio = tk.Checkbutton(self.scrollable_frame, text="Laboratorio", variable=self.svLaboratorio, width=25, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryLaboratorio.grid(column=0, row=27, padx=5, pady=5)

        self.svRadiología = tk.BooleanVar()
        self.entryRadiología = tk.Checkbutton(self.scrollable_frame, text="Radiología", variable=self.svRadiología, width=25, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryRadiología.grid(column=0, row=28, padx=5, pady=5)

        self.svEcografía = tk.BooleanVar()
        self.entryEcografía = tk.Checkbutton(self.scrollable_frame, text="Ecografía", variable=self.svEcografía, width=25, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryEcografía.grid(column=0, row=29, padx=5, pady=5)

        self.lblOtros = tk.Label(self.scrollable_frame, text='Otros: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblOtros.grid(column=0, row=30, padx=(0,0), pady=5)

        self.svOtros = tk.StringVar()
        self.entryOtrosora = tk.Entry(self.scrollable_frame, textvariable=self.svOtros, width=10, font=('ARIAL', 10,'bold'))
        self.entryOtrosora.grid(column=0, row=30, padx=(120,0), pady=5)

        self.lblTratam = tk.Label(self.scrollable_frame, text='Tratamiento: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTratam.grid(column=3, row=26, padx=5, pady=5)

        self.svTratam = tk.StringVar()
        self.entryTratam = tk.Text(self.scrollable_frame, wrap=tk.WORD, width=40, height=10, font=('ARIAL', 10, 'bold'))
        self.entryTratam.grid(column=3, row=26, padx=5, pady=5, columnspan=5, rowspan=5)

         # Insertar una línea de separación entre la fila 24 y la fila 26
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=31, columnspan=15, sticky="ew", pady=5)

        self.lblProcedimientos = tk.Label(self.scrollable_frame, text='Procedimientos: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblProcedimientos.grid(column=0, row=32, padx=5, pady=5)

        self.svProcedimientos = tk.StringVar()
        self.entryProcedimientos = tk.Text(self.scrollable_frame, wrap=tk.WORD, width=160, height=5, font=('ARIAL', 10, 'bold'))
        self.entryProcedimientos.grid(column=0, row=33, padx=5, pady=5, columnspan=7, rowspan=2)

        self.lblDF = tk.Label(self.scrollable_frame, text='Diagnóstico de Final: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDF.grid(column=0, row=37, padx=0, pady=5)

        self.svDF = tk.StringVar()
        self.entryDF = tk.Entry(self.scrollable_frame, textvariable=self.svDF, width=123, font=('ARIAL', 10,'bold'))
        self.entryDF.grid(column=0, row=38, padx=5, pady=5, columnspan=5)

        self.lblCodCief = tk.Label(self.scrollable_frame, text='COD. CIE 10: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblCodCief.grid(column=5, row=37, padx=0, pady=5, columnspan=6)

        self.svCodCief = tk.StringVar()
        self.entryCodCief = tk.Entry(self.scrollable_frame, textvariable=self.svCodCief, width=30, font=('ARIAL', 10,'bold'))
        self.entryCodCief.grid(column=5, row=38, padx=5, pady=5, columnspan=6)

        self.lblIndicaciones = tk.Label(self.scrollable_frame, text='Indicaciones: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblIndicaciones.grid(column=0, row=39, padx=5, pady=5)

        self.svIndicaciones = tk.StringVar()
        self.entryIndicaciones = tk.Text(self.scrollable_frame, wrap=tk.WORD, width=160, height=5, font=('ARIAL', 10, 'bold'))
        self.entryIndicaciones.grid(column=0, row=40, padx=5, pady=5, columnspan=7, rowspan=2)

        self.lblObservaciones = tk.Label(self.scrollable_frame, text='Observaciones: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblObservaciones.grid(column=0, row=43, padx=5, pady=5)

        self.svObservaciones = tk.StringVar()
        self.entryObservaciones = tk.Text(self.scrollable_frame, wrap=tk.WORD, width=160, height=5, font=('ARIAL', 10, 'bold'))
        self.entryObservaciones.grid(column=0, row=44, padx=5, pady=5, columnspan=7, rowspan=2)

         #Insertar una línea de separación entre la fila 44 y la fila 46
        ttk.Separator(self.scrollable_frame, orient='horizontal').grid(row=46, columnspan=15, sticky="ew", pady=5)

        self.lblDestino = tk.Label(self.scrollable_frame, text='Destino: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
        self.lblDestino.grid(column=0, row=47, padx=0, pady=5)

        self.svAlta = tk.BooleanVar()
        self.entryAlta = tk.Checkbutton(self.scrollable_frame, text="Alta", variable=self.svAlta, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryAlta.grid(column=1, row=48, padx=0, pady=5)
        
        self.svObservación = tk.BooleanVar()
        self.entryObservación = tk.Checkbutton(self.scrollable_frame, text="Observación", variable=self.svObservación, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryObservación.grid(column=1, row=49, padx=0, pady=5)

        self.svUPC = tk.BooleanVar()
        self.entryUPC = tk.Checkbutton(self.scrollable_frame, text="Unidad Paciente Crítico", variable=self.svUPC, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryUPC.grid(column=1, row=50, padx=0, pady=5)

        self.svHospitalización = tk.BooleanVar()
        self.entryHospitalización = tk.Checkbutton(self.scrollable_frame, text="Hospitalización", variable=self.svHospitalización, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryHospitalización.grid(column=1, row=51, padx=0, pady=5)

        self.svCObs = tk.BooleanVar()
        self.entryCObs = tk.Checkbutton(self.scrollable_frame, text="Centro Obstetratico", variable=self.svCObs, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryCObs.grid(column=3, row=48, padx=5, pady=5)

        self.svCquir = tk.BooleanVar()
        self.entryCquir = tk.Checkbutton(self.scrollable_frame, text="Centro Quirúrgico", variable=self.svCquir, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryCquir.grid(column=3, row=49, padx=5, pady=5)

        self.svR_Trans = tk.BooleanVar()
        self.entryR_Trans = tk.Checkbutton(self.scrollable_frame, text="Referencia / Transferencia", variable=self.svR_Trans, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryR_Trans.grid(column=3, row=50, padx=0, pady=5)

        self.lblLugar = tk.Label(self.scrollable_frame, text='Lugar: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblLugar.grid(column=3, row=51, padx=(0,0), pady=5)

        self.svLugar = tk.StringVar()
        self.entryLugar = tk.Entry(self.scrollable_frame, textvariable=self.svLugar, width=10, font=('ARIAL', 10,'bold'))
        self.entryLugar.grid(column=3, row=51, padx=(120,0), pady=5)

        self.lblHoraD = tk.Label(self.scrollable_frame, text='Hora: ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblHoraD.grid(column=3, row=52, padx=(0,0), pady=5)

        self.svHoraD = tk.StringVar()
        self.entryHoraD = tk.Entry(self.scrollable_frame, textvariable=self.svHoraD, width=10, font=('ARIAL', 10,'bold'))
        self.entryHoraD.grid(column=3, row=52, padx=(120,0), pady=5) 
        self.actualizar_hora3()

        self.svRetVol = tk.BooleanVar()
        self.entryRetVol = tk.Checkbutton(self.scrollable_frame, text="Retiro Voluntario", variable=self.svRetVol, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryRetVol.grid(column=5, row=48, padx=0, pady=5)

        self.svFuga = tk.BooleanVar()
        self.entryFuga = tk.Checkbutton(self.scrollable_frame, text="Fuga", variable=self.svFuga, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryFuga.grid(column=5, row=49, padx=0, pady=5)

        self.svMortuorio = tk.BooleanVar()
        self.entryMortuorio = tk.Checkbutton(self.scrollable_frame, text="Mortuorio", variable=self.svMortuorio, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryMortuorio.grid(column=5, row=50, padx=0, pady=5)

        self.svNAtend = tk.BooleanVar()
        self.entryNAtend = tk.Checkbutton(self.scrollable_frame, text="No Atendido", variable=self.svNAtend, width=20, font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.entryNAtend.grid(column=5, row=51, padx=0, pady=5)

        self.lblMedRes = tk.Label(self.scrollable_frame, text='Medico Responsable: ', font=('ARIAL', 10, 'bold'), fg='black', bg='#8C9BBA')
        self.lblMedRes.grid(column=2, row=53, padx=0, pady=5)

        self.contenedor_MedRes = tk.Label(self.scrollable_frame, bg='#ffffff')
        self.contenedor_MedRes.grid(column=2, row=54, padx=5, pady=5)
        self.imagen_tk_MedRes = None
        self.contenedor_MedRes.bind("<Button-1>", lambda event, contenedor=self.contenedor_MedRes: self.mostrar_imagen(event, contenedor))

        self.lblExaAdi = tk.Label(self.scrollable_frame, text='Examenes Adicionales: ', font=('ARIAL', 10, 'bold'), fg='black', bg='#8C9BBA')
        self.lblExaAdi.grid(column=2, row=57, padx=0, pady=5)

        self.lista_imagenes = tk.Listbox(self.scrollable_frame, selectmode=tk.SINGLE, height=5)
        self.lista_imagenes.grid(column=2, row=58, padx=5, pady=5)
        self.lista_imagenes.bind("<<ListboxSelect>>", self.seleccionar_imagen)

        self.contenedor_ExaAdi = tk.Label(self.scrollable_frame, bg='#ffffff')
        self.contenedor_ExaAdi.grid(column=3, row=58, padx=5, pady=5)
        self.imagen_tk_ExaAdi = None
        self.lblExaAdi.bind("<Button-1>", self.mostrar_cuadro_dialogo)

        # Crear una ventana y mostrarla

root = tk.Tk()
ventana = VentanaDiagnosticoMedico(root)
ventana.pack()
root.mainloop()
