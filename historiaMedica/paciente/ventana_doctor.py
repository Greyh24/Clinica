import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox,filedialog,ttk,Scrollbar
from tkcalendar import DateEntry
from time import strftime
from PIL import Image, ImageTk,ImageGrab
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from matplotlib.backends.backend_pdf import PdfPages

class VentanaDiagnosticoMedico(tk.Frame):
    def __init__(self, root):
        super().__init__(root, width=1300, height=620)
        self.root = root

        self.root.title("Diagnóstico Médico")
        self.canvas = tk.Canvas(self, bg='#8C9BBA', width=1300, height=620)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Obtener la resolución de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calcular las coordenadas para centrar la ventana
        x_coordinate = (screen_width - 1320) // 2  # Ancho de la ventana
        y_coordinate = (screen_height - 620) // 2  # Altura de la ventana

        # Centrar la ventana en la pantalla
        self.root.geometry(f"1320x620+{x_coordinate}+{y_coordinate}")

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

        self.svPaci = tk.StringVar()
        self.entryPaci = tk.Entry(self.scrollable_frame, textvariable=self.svPaci, width=20, font=('ARIAL', 10,'bold'))
        self.entryPaci.grid(column=1, row=1, padx=0, pady=5)

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

        self.lblTrans = tk.Label(self.scrollable_frame, text='Tipo de Accidente: ', font=('ARIAL', 8, 'bold'),fg='black', bg='#8C9BBA')
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

        self.lblTemp = tk.Label(self.scrollable_frame, text='Tº ', font=('ARIAL', 10, 'bold'),fg='black', bg='#8C9BBA')
        self.lblTemp.grid(column=4, row=20, padx=(0,90), pady=5)

        self.svTemp = tk.StringVar()
        self.entryTemp = tk.Entry(self.scrollable_frame, textvariable=self.svTemp, width=10, font=('ARIAL', 10,'bold'))
        self.entryTemp.grid(column=4, row=20, padx=(10,0), pady=5)

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

        self.lblDF = tk.Label(self.scrollable_frame, text='Diagnóstico Final: ', font=('ARIAL', 12, 'bold'),fg='black', bg='#8C9BBA')
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

        self.lblMedRes = tk.Label(self.scrollable_frame, text='Firma y Nombre del medico responsable: ', font=('ARIAL', 10, 'bold','underline'), underline=6, fg='black', bg='#8C9BBA')
        self.lblMedRes.grid(column=3, row=54, padx=0, pady=5)

        self.contenedor_MedRes = tk.Label(self.scrollable_frame, bg='#ffffff')
        self.contenedor_MedRes.grid(column=3, row=53, padx=5, pady=5)
        self.imagen_tk_MedRes = None
        self.contenedor_MedRes.bind("<Button-1>", lambda event, contenedor=self.contenedor_MedRes: self.mostrar_imagen(event, contenedor))

        # Cargar la imagen "firma.png"
        ruta_firma = "C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/firma.png"
        imagen_firma = Image.open(ruta_firma)
        self.mostrar_imagen_en_label(imagen_firma, self.contenedor_MedRes)

        self.svMedRes = tk.StringVar()
        self.entryMedRes = tk.Entry(self.scrollable_frame, textvariable=self.svMedRes, width=30, font=('ARIAL', 10,'bold'))
        self.entryMedRes.grid(column=4, row=54, padx=5, pady=5, columnspan=7, rowspan=2)

        self.lblExaAdi = tk.Label(self.scrollable_frame, text='Examenes Adicionales: ', font=('ARIAL', 10, 'bold'), fg='black', bg='#8C9BBA')
        self.lblExaAdi.grid(column=2, row=57, padx=0, pady=5)

        self.lista_imagenes = tk.Listbox(self.scrollable_frame, selectmode=tk.SINGLE, height=5)
        self.lista_imagenes.grid(column=2, row=58, padx=5, pady=5)
        self.lista_imagenes.bind("<<ListboxSelect>>", self.seleccionar_imagen)

        self.contenedor_ExaAdi = tk.Label(self.scrollable_frame, bg='#ffffff')
        self.contenedor_ExaAdi.grid(column=3, row=58, padx=5, pady=5)
        self.imagen_tk_ExaAdi = None
        self.contenedor_ExaAdi.bind("<Button-1>", self.mostrar_cuadro_dialogo)

        # Cargar la imagen predeterminada "galeria.png"
        ruta_predeterminada = "C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/galeria.png"
        imagen_predeterminada = Image.open(ruta_predeterminada)
        self.mostrar_imagen_en_label(imagen_predeterminada, self.contenedor_ExaAdi)

        # botones 
        self.BtnGuardarDoc = tk.Button(self.scrollable_frame, text='Guardar Documento', width=18, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE',command=self.generar_pdf)
        self.BtnGuardarDoc.grid(column=1, row=59, padx=5, pady=15)

        self.BtnCrearD = tk.Button(self.scrollable_frame, text='Crear Díagnostico', width=20, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#1658A2', cursor='hand2', activebackground='#3D69F0',command=self.abrir_nueva_ventana)
        self.BtnCrearD.grid(column=3, row=59, padx=5, pady=5)

        self.BtnCerrar = tk.Button(self.scrollable_frame, text='Cerrar', width=20, font=('Arial', 10, 'bold'),fg='#FFFEFE', bg='#D32F2F', cursor='hand2', activebackground='#3D69F0',command=self.cerrar_ventana)
        self.BtnCerrar.grid(column=5, row=59, padx=5, pady=5)
    
    #funcion utilizada para crear pdf de la ficha del diagnostico
    def generar_pdf(self):
        # Obtener los datos de la GUI
        datos_gui = self.obtener_datos()

        # Crear una interfaz de selección de archivo
        root = tk.Tk()
        root.withdraw()  # Evita que aparezca la ventana principal de tkinter

        # Mostrar el cuadro de diálogo para seleccionar la ubicación y el nombre del archivo
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        # Verificar si el usuario canceló la operación
        if not file_path:
            return

        # Crear un nuevo PDF
        c = canvas.Canvas(file_path, pagesize=letter)

        # Inicializar variables para el seguimiento de la posición en la página
        y_actual = 750
        espacio_requerido = 20  # Espacio requerido entre líneas
        espacio_pagina = 750  # Espacio total en una página

        # Función para verificar si hay suficiente espacio en la página actual
        def hay_espacio_suficiente():
            return y_actual - espacio_requerido > 0

        # Función para crear una nueva página
        def crear_nueva_pagina():
            nonlocal c, y_actual
            c.showPage()  # Crear una nueva página
            y_actual = espacio_pagina  # Restablecer la posición vertical en la nueva página

        # Función para agregar texto a la página actual
        def agregar_texto(texto):
            nonlocal y_actual
            c.drawString(100, y_actual, texto)
            y_actual -= espacio_requerido  # Actualizar la posición vertical

        # Agregar texto al PDF usando los datos proporcionados
        agregar_texto("{}".format(datos_gui["Diagnostico_Medico"]))
        agregar_texto("Paciente: {}".format(datos_gui["Paciente"]))

        # Campos adicionales relacionados con el paciente
        y_paciente = y_actual - espacio_requerido
        campos_paciente = [
            ("Edad", datos_gui["Edad"]),
            ("Sexo", datos_gui["Sexo"]),
            ("Dirección", datos_gui["Direccion"]),
            ("Distrito", datos_gui["Distrito"]),
            ("Responsable", datos_gui["Responsable"]),
            ("Modo de Ingreso", datos_gui["Modo_Ingreso"]),
            ("DNI", datos_gui["DNI"]),
            ("Tipo de Accidente", datos_gui["Tipo_AccidenteP"]or ""),
            ("Tipo de Seguro", datos_gui["Tipo_Seg"]),
            ("Teléfono", datos_gui["Telefono"]),
            ("Ficha", datos_gui["Ficha"]),
            ("Fecha de Presentación", datos_gui["Fecha_P"]),
            ("Hora de Presentación", datos_gui["Hora_P"]),
            ("Historia", datos_gui["Historia"]),
        ]

        for campo, valor in campos_paciente:
            if y_paciente - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_paciente = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_paciente -= espacio_requerido

        # Lista de especialidades y variables booleanas
        especialidades = [
            ("Medicina", self.svMedicina),
            ("Pediatria", self.svPediatria),
            ("Cirugia", self.svCirugia),
            ("Gineco OBS", self.svGineco_OBS),
            # Agrega más especialidades si es necesario
        ]

        # Iterar sobre la lista de especialidades para agregar al PDF
        for especialidad, variable in especialidades:
            if variable.get():
                agregar_texto("Especialidad: {}".format(especialidad))

        # Campos adicionales relacionados con el accidente
        y_accidente = y_paciente - espacio_requerido
        campos_accidente = [
            ("Prioridad de Daño",self.obtener_valor_seleccionado(datos_gui["Prioridad_Daño"])),
            ("Tipo de Accidente", self.obtener_valor_seleccionado(datos_gui["Tipo_Accidente"])),
            ("Otros Accidentes", datos_gui["Otros_Accidente"]),
            ("Fecha del Accidente", datos_gui["Fecha_Accidente"]),
            ("Hora del Accidente", datos_gui["Hora_Accidente"]),
        ]

        for campo, valor in campos_accidente:
            if y_accidente - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_accidente = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_accidente -= espacio_requerido

        # Campos adicionales relacionados con ANAMNESIS
        y_anamnesis = y_accidente - espacio_requerido
        campos_anamnesis = [
            ("Tiempo de Enfermedad", datos_gui["Tiempo_Enfermedad"]),
            ("Motivo de Consulta", datos_gui["Motivo_Consulta"]),
            ("Antecedentes", datos_gui["Antecedentes"]),
        ]

        for campo, valor in campos_anamnesis:
            if y_anamnesis - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_anamnesis = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_anamnesis -= espacio_requerido

        # Campos adicionales relacionados con Examen Clínico
        y_examen_clinico = y_anamnesis - espacio_requerido
        campos_examen_clinico = [
            ("P.A", datos_gui["P.A"]),
            ("FC", datos_gui["FC"]),
            ("FR", datos_gui["FR"]),
            ("Tº", datos_gui["Tº"]),
            ("SO", datos_gui["SO"]),
            ("Peso", datos_gui["Peso"]),
        ]

        for campo, valor in campos_examen_clinico:
            if y_examen_clinico - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_examen_clinico = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_examen_clinico -= espacio_requerido

        # Campos adicionales relacionados con el examen preferencial
        y_examen_preferencial = y_examen_clinico - espacio_requerido
        if y_examen_preferencial - espacio_requerido < 0:
            crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio

        agregar_texto("Examen Preferencial: {}".format(datos_gui["Examen_Preferencial"]))

        # Campos adicionales relacionados con Diagnóstico de Ingreso
        y_diagnostico_ingreso = y_examen_preferencial - espacio_requerido
        if y_diagnostico_ingreso - espacio_requerido < 0:
            crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio

        agregar_texto("Diagnóstico de Ingreso: {}".format(datos_gui["Diagnostico_Ingreso"]))
        agregar_texto("COD CIE-10: {}".format(datos_gui["COD_CIE_10"]))

        # Campos adicionales relacionados con Plan de Trabajo
        y_plan_trabajo = y_diagnostico_ingreso - espacio_requerido
        campos_plan_trabajo = [
            ("Hidratación", datos_gui["Plan_Trabajo"]["Hidratacion"]),
            ("Tratamiento", datos_gui["Plan_Trabajo"]["Tratamiento"]),
        ]

        for campo, valor in campos_plan_trabajo:
            if y_plan_trabajo - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_plan_trabajo = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_plan_trabajo -= espacio_requerido

        # Campos adicionales relacionados con Examenes Auxiliares
        y_examenes_auxiliares = y_plan_trabajo - espacio_requerido
        campos_examenes_auxiliares = [
            ("Laboratorio", datos_gui["Examenes_Auxiliares"]["Laboratorio"]),
            ("Radiología", datos_gui["Examenes_Auxiliares"]["Radiologia"]),
            ("Ecografía", datos_gui["Examenes_Auxiliares"]["Ecografia"]),
            ("Otros", datos_gui["Examenes_Auxiliares"]["Otros"]),
        ]

        if y_examenes_auxiliares - espacio_requerido < 0:
            crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio

        agregar_texto("Examenes Auxiliares:")
        for campo, valor in campos_examenes_auxiliares:
            if y_examenes_auxiliares - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_examenes_auxiliares = espacio_pagina

            # Verificar si el valor es True antes de imprimir
            if valor:
                agregar_texto("{}".format(campo))
            
            y_examenes_auxiliares -= espacio_requerido

        # Campos adicionales relacionados con Procedimientos
        y_procedimientos = y_examenes_auxiliares - espacio_requerido
        if y_procedimientos - espacio_requerido < 0:
            crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio

        agregar_texto("Procedimientos: {}".format(datos_gui["Procedimientos"]))

        # Campos adicionales relacionados con Diagnóstico Final
        y_diagnostico_final = y_procedimientos - espacio_requerido
        campos_diagnostico_final = [
            ("Diagnóstico Final", datos_gui["Diagnostico_Final"]),
            ("COD CIE-10", datos_gui["COD_CIE_10f"]),  # Agregado el campo COD_CIE-10f
        ]

        for campo, valor in campos_diagnostico_final:
            if y_diagnostico_final - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_diagnostico_final = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_diagnostico_final -= espacio_requerido

        # Campos adicionales relacionados con Indicaciones
        y_indicaciones = y_diagnostico_final - espacio_requerido
        campos_indicaciones = [
            ("Indicaciones", datos_gui["Indicaciones"]),
        ]

        for campo, valor in campos_indicaciones:
            if y_indicaciones - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_indicaciones = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_indicaciones -= espacio_requerido

        # Campos adicionales relacionados con Observaciones
        y_observaciones = y_indicaciones - espacio_requerido
        campos_observaciones = [
            ("Observaciones", datos_gui["Observaciones"]),
        ]

        for campo, valor in campos_observaciones:
            if y_observaciones - espacio_requerido < 0:
                crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                y_observaciones = espacio_pagina

            agregar_texto("{}: {}".format(campo, valor))
            y_observaciones -= espacio_requerido

       # Campos adicionales relacionados con Destino
        y_destino = y_observaciones - espacio_requerido
        campos_destino = [
            ("Alta", datos_gui["Destino"].get("Alta", "")),
            ("Observación", datos_gui["Destino"].get("Observacion", "")),
            ("Unidad Paciente Crítico", datos_gui["Destino"].get("UPC", "")),
            ("Hospitalización", datos_gui["Destino"].get("Hospitalizacion", "")),
            ("Centro Obstétrico", datos_gui["Destino"].get("Centro_Obstetrico", "")),
            ("Centro Quirúrgico", datos_gui["Destino"].get("Centro_Quirurgico", "")),
            ("Referencia/Transferencia", datos_gui["Destino"].get("Referencia_Transferencia", "")),
            ("Lugar", datos_gui["Destino"].get("Lugar", "")),
            ("Hora", datos_gui["Destino"].get("Hora", "")),
            ("Retiro Voluntario", datos_gui["Destino"].get("Retiro_Voluntario", "")),
            ("Fuga", datos_gui["Destino"].get("Fuga", "")),
            ("Mortuorio", datos_gui["Destino"].get("Mortuorio", "")),
            ("No Atendido", datos_gui["Destino"].get("No_Atendido", "")),
        ]

        if y_destino - espacio_requerido < 0:
            crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio

        agregar_texto("Destino:")

        for campo, valor in campos_destino:
            if valor:  # Solo imprimir si el valor es True
                if y_destino - espacio_requerido < 0:
                    crear_nueva_pagina()  # Crear nueva página si no hay suficiente espacio
                    y_destino = espacio_pagina

                if campo == "Observación":
                    agregar_texto("{}".format(campo, valor))
                elif campo in ["Lugar", "Hora"]:
                    agregar_texto("{}: {}".format(campo, valor))
                else:
                    agregar_texto("{}".format(campo))
                
                y_destino -= espacio_requerido
      

        # Guardar el PDF
        c.save()

    def obtener_valor_seleccionado(self, diccionario):
        # Si el diccionario está vacío o no es un diccionario, devolver una cadena vacía
        if not diccionario or not isinstance(diccionario, dict):
            return ""
        
        # Obtener la primera clave del diccionario (debería haber solo una clave)
        clave = next(iter(diccionario.keys()), '')

        # Si la clave es True, devolver la clave; de lo contrario, devolver una cadena vacía
        return clave if diccionario[clave] else ""

    #funcion utilizada para obtiene datos de la ventana de la ficha del diagnostico
    def obtener_datos(self):
        datos = {}

        # Campos relacionados con el paciente
        datos['Diagnostico_Medico'] = self.lblDM.cget('text')
        datos['Paciente'] = self.svPaci.get()
        datos['Edad'] = self.svEdad.get()
        datos['Sexo'] = self.svSex.get()
        datos['Direccion'] = self.svDir.get()
        datos['Distrito'] = self.svDis.get()
        datos['Responsable'] = self.svResp.get()
        datos['Modo_Ingreso'] = self.svMI.get()
        datos['DNI'] = self.svDNI.get()
        datos['Tipo_AccidenteP'] = self.svTrans.get()
        datos['Tipo_Seg'] = self.svTseg.get()
        datos['Telefono'] = self.svTel.get()
        datos['Ficha'] = self.svFicha.get()
        datos['Fecha_P'] = self.svfechaP.get()
        datos['Hora_P'] = self.svHoraP.get()
        datos['Historia'] = self.svHistoria.get()
        # Campos relacionados con especialidades
        especialidades = {key: value.get() for key, value in {
            'Medicina': self.svMedicina,
            'Pediatria': self.svPediatria,
            'Cirugia': self.svCirugia,
            'Gineco_OBS': self.svGineco_OBS,
        }.items() if value.get()}

        # Asegúrate de que el diccionario no esté vacío antes de agregarlo a los datos
        if especialidades:
            datos['Especialidad'] = especialidades
        else:
            datos['Especialidad'] = None  # O cualquier valor predeterminado que desees


        # Campos adicionales relacionados con el accidente
        datos['Prioridad_Daño'] = {key: value.get() for key, value in {
            'Prioridad1': self.svPriorid1,
            'Prioridad2': self.svPriorid2,
            'Prioridad3': self.svPriorid3,
            'Prioridad4': self.svPriorid4,
        }.items() if value.get()}

        datos['Tipo_Accidente'] = {key: value.get() for key, value in {
            'Atropello': self.svAtrop,
            'Choque': self.svChoque,
            'Despiste': self.svDespiste,
            'Incendio': self.svIncendio,
            'Atropello_y_Fuga': self.svAyF,
            'Choque_y_Fuga': self.svCyF,
            'Caida_de_Pasajeros': self.svCaidaP,
            'Volcadura': self.svVolcadura,
        }.items() if value.get()}

        datos['Otros_Accidente'] = self.svOtrosAT.get()
        datos['Fecha_Accidente'] = self.svFechaAT.get()
        datos['Hora_Accidente'] = self.svHoraAT.get()

        # Campos relacionados con ANAMNESIS
        datos['Tiempo_Enfermedad'] = self.svTipoE.get()
        datos['Motivo_Consulta'] = self.svMC.get()
        datos['Antecedentes'] = self.svAntecedentes.get()

        # Campos relacionados con Examen Clínico
        datos['P.A'] = self.svPA.get()
        datos['FC'] = self.svFC.get()
        datos['FR'] = self.svFR.get()
        datos['Tº'] = self.svTemp.get()
        datos['SO'] = self.svSO.get()
        datos['Peso'] = self.svPeso.get()

        # Campos relacionados con el examen preferencial
        datos['Examen_Preferencial'] = self.svExamenP.get()

        # Campos relacionados con Diagnóstico de Ingreso
        datos['Diagnostico_Ingreso'] = self.svDdi.get()
        datos['COD_CIE_10'] = self.svCodCie.get()

        # Campos relacionados con Plan de Trabajo
        datos['Plan_Trabajo'] = {
            'Hidratacion': 'Si' if self.svHidratS.get() else 'No',
            'Tratamiento': self.entryTratam.get("1.0", "end-1c") if self.svHidratS.get() else '',
        }

        # Campos relacionados con exámenes auxiliares
        datos['Examenes_Auxiliares'] = {
        'Laboratorio': self.svLaboratorio.get(),
        'Radiologia': self.svRadiología.get(),  # Corregir el nombre aquí
        'Ecografia': self.svEcografía.get(),
        'Otros': self.svOtros.get(),
        }

        # Campos relacionados con Procedimientos
        datos['Procedimientos'] = self.entryProcedimientos.get("1.0", "end-1c")

        # Campos relacionados con Diagnóstico Final
        datos['Diagnostico_Final'] = self.svDF.get()
        datos['COD_CIE_10f'] = self.svCodCief.get()

        # Campos relacionados con Indicaciones
        datos['Indicaciones'] = self.entryIndicaciones.get("1.0", "end-1c")

        # Campos relacionados con Observaciones
        datos['Observaciones'] = self.entryObservaciones.get("1.0", "end-1c")

        # Campos relacionados con destino
        datos['Destino'] = {
            'Alta': self.svAlta.get(),
            'Observacion': self.svObservación.get(),
            'UPC': self.svUPC.get(),
            'Hospitalizacion': self.svHospitalización.get(),
            'Centro_Obstetrico': self.svCObs.get(),
            'Centro_Quirurgico': self.svCquir.get(),
            'Referencia_Transferencia': self.svR_Trans.get(),
            'Lugar': self.svLugar.get(),
            'Hora': self.svHoraD.get(),
            'Retiro_Voluntario': self.svRetVol.get(),
            'Fuga': self.svFuga.get(),
            'Mortuorio': self.svMortuorio.get(),
            'No_Atendido': self.svNAtend.get(),
        }

        return datos

    #funcion utilizada para guardar ficha del diagnostico
    def guardar_pdf(self, datos, file_path):
        # Crear un nuevo PDF
        c = canvas.Canvas(file_path, pagesize=letter)

        # Agregar texto al PDF usando los datos proporcionados
        c.drawString(100, 750, "Diagnóstico Médico: {}".format(datos["Diagnostico_Medico"]))
        c.drawString(100, 730, "Paciente: {}".format(datos["Paciente"]))

        # Campos adicionales relacionados con el paciente
        y_paciente = 710
        campos_paciente = [
            ("Edad", datos["Edad"]),
            ("Sexo", datos["Sexo"]),
            ("Dirección", datos["Direccion"]),
            ("Distrito", datos["Distrito"]),
            ("Responsable", datos["Responsable"]),
            ("Modo de Ingreso", datos["Modo_Ingreso"]),
            ("DNI", datos["DNI"]),
            ("Tipo de Accidente", datos["Tipo_AccidenteP"] or ""),  # Corregido el nombre de la clave
            ("Tipo de Seguro", datos["Tipo_Seg"]),
            ("Teléfono", datos["Telefono"]),
            ("Ficha", datos["Ficha"]),
            ("Fecha de Presentación", datos["Fecha_P"]),
            ("Hora de Presentación", datos["Hora_P"]),
            ("Historia", datos["Historia"]),
            ("Especialidad", datos.get("Especialidad", "")),  # Asegurarse de manejar el caso en que no haya especialidad
        ]

        for campo, valor in campos_paciente:
            c.drawString(100, y_paciente, "{}: {}".format(campo, valor))
            y_paciente -= 20

        # Campos adicionales relacionados con el accidente
        y_accidente = y_paciente - 20
        campos_accidente = [
            ("Prioridad de Daño", datos["Prioridad_Daño"]or ""),
            ("Tipo de Accidente", datos["Tipo_Accidente"]or ""),
            ("Otros Accidentes", datos["Otros_Accidente"]),
            ("Fecha del Accidente", datos["Fecha_Accidente"]),
            ("Hora del Accidente", datos["Hora_Accidente"]),
        ]

        for campo, valor in campos_accidente:
            c.drawString(100, y_accidente, "{}: {}".format(campo, valor))
            y_accidente -= 20

        # Campos adicionales relacionados con ANAMNESIS
        y_anamnesis = y_accidente - 20
        campos_anamnesis = [
            ("Tiempo de Enfermedad", datos["Tiempo_Enfermedad"]),
            ("Motivo de Consulta", datos["Motivo_Consulta"]),
            ("Antecedentes", datos["Antecedentes"]),
        ]

        for campo, valor in campos_anamnesis:
            c.drawString(100, y_anamnesis, "{}: {}".format(campo, valor))
            y_anamnesis -= 20

        # Campos adicionales relacionados con Examen Clínico
        y_examen_clinico = y_anamnesis - 20
        campos_examen_clinico = [
            ("P.A", datos["P.A"]),
            ("FC", datos["FC"]),
            ("FR", datos["FR"]),
            ("Tº", datos["Tº"]),
            ("SO", datos["SO"]),
            ("Peso", datos["Peso"]),
        ]

        for campo, valor in campos_examen_clinico:
            c.drawString(100, y_examen_clinico, "{}: {}".format(campo, valor))
            y_examen_clinico -= 20

        # Campos adicionales relacionados con el examen preferencial
        y_examen_preferencial = y_examen_clinico - 20
        c.drawString(100, y_examen_preferencial, "Examen Preferencial: {}".format(datos["Examen_Preferencial"]))

        # Campos adicionales relacionados con Diagnóstico de Ingreso
        y_diagnostico_ingreso = y_examen_preferencial - 20
        c.drawString(100, y_diagnostico_ingreso, "Diagnóstico de Ingreso: {}".format(datos["Diagnostico_Ingreso"]))
        c.drawString(100, y_diagnostico_ingreso - 20, "COD CIE-10: {}".format(datos["COD_CIE_10"]))

        # Campos adicionales relacionados con Plan de Trabajo
        y_plan_trabajo = y_diagnostico_ingreso - 40
        campos_plan_trabajo = [
            ("Hidratación", datos["Plan_Trabajo"]["Hidratacion"]),
            ("Tratamiento", datos["Plan_Trabajo"]["Tratamiento"]),
        ]

        for campo, valor in campos_plan_trabajo:
            c.drawString(100, y_plan_trabajo, "{}: {}".format(campo, valor))
            y_plan_trabajo -= 20

        # Campos adicionales relacionados con Examenes Auxiliares
        y_examenes_auxiliares = y_plan_trabajo - 20
        campos_examenes_auxiliares = [
            ("Laboratorio", datos["Examenes_Auxiliares"]["Laboratorio"]),
            ("Radiología", datos["Examenes_Auxiliares"]["Radiologia"]),
            ("Ecografía", datos["Examenes_Auxiliares"]["Ecografia"]),
            ("Otros", datos["Examenes_Auxiliares"]["Otros"]),
        ]

        c.drawString(100, y_examenes_auxiliares, "Examenes Auxiliares:")
        for campo, valor in campos_examenes_auxiliares:
            c.drawString(120, y_examenes_auxiliares - 20, "{}: {}".format(campo, valor))
            y_examenes_auxiliares -= 20

        # Campos adicionales relacionados con Procedimientos
        y_procedimientos = y_examenes_auxiliares - 20
        c.drawString(100, y_procedimientos, "Procedimientos: {}".format(datos["Procedimientos"]))

        # Campos adicionales relacionados con Diagnóstico Final
        y_diagnostico_final = y_procedimientos - 20
        campos_diagnostico_final = [
            ("Diagnóstico Final", datos["Diagnostico_Final"]),
            ("COD CIE-10f", datos["COD_CIE_10f"]),  # Agregado el campo COD_CIE-10f
        ]

        for campo, valor in campos_diagnostico_final:
            c.drawString(100, y_diagnostico_final, "{}: {}".format(campo, valor))
            y_diagnostico_final -= 20

        # Campos adicionales relacionados con Indicaciones
        y_indicaciones = y_diagnostico_final - 20
        campos_indicaciones = [
            ("Indicaciones", datos["Indicaciones"]),
        ]

        for campo, valor in campos_indicaciones:
            c.drawString(100, y_indicaciones, "{}: {}".format(campo, valor))
            y_indicaciones -= 20

        # Campos adicionales relacionados con Observaciones
        y_observaciones = y_indicaciones - 20
        campos_observaciones = [
            ("Observaciones", datos["Observaciones"]),
        ]

        for campo, valor in campos_observaciones:
            c.drawString(100, y_observaciones, "{}: {}".format(campo, valor))
            y_observaciones -= 20

        # Campos adicionales relacionados con Destino
        y_destino = y_observaciones - 20
        campos_destino = [
            ("Alta", datos["Destino"]["Alta"]),
            ("Observación", datos["Destino"]["Observacion"]),
            ("UPC", datos["Destino"]["UPC"]),
            ("Hospitalización", datos["Destino"]["Hospitalizacion"]),
            ("Centro Obstétrico", datos["Destino"]["Centro_Obstetrico"]),
            ("Centro Quirúrgico", datos["Destino"]["Centro_Quirurgico"]),
            ("Referencia/Transferencia", datos["Destino"]["Referencia_Transferencia"]),
            ("Lugar", datos["Destino"]["Lugar"]),
            ("Hora", datos["Destino"]["Hora"]),
            ("Retiro Voluntario", datos["Destino"]["Retiro_Voluntario"]),
            ("Fuga", datos["Destino"]["Fuga"]),
            ("Mortuorio", datos["Destino"]["Mortuorio"]),
            ("No Atendido", datos["Destino"]["No_Atendido"]),
        ]

        c.drawString(100, y_destino, "Destino:")
        for campo, valor in campos_destino:
            c.drawString(120, y_destino - 20, "{}: {}".format(campo, valor))
            y_destino -= 20
        
        # Guardar el PDF
        c.save()

    #funcion utilizada para crear ventana de la receta
    def abrir_nueva_ventana(self):
        nueva_ventana = tk.Toplevel(self.root)
        nueva_ventana.title("Diagnostico")
        nueva_ventana.geometry("520x600")

        # Centrar la ventana en la pantalla
        nueva_ventana.update_idletasks()
        width = nueva_ventana.winfo_width()
        height = nueva_ventana.winfo_height()
        x = (nueva_ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (nueva_ventana.winfo_screenheight() // 2) - (height // 2)
        nueva_ventana.geometry(f"{width}x{height}+{x}+{y}")
        
        main_frame = tk.Frame(nueva_ventana, padx=10, pady=10)
        main_frame.grid(row=0, column=0)

        # Obtener valores de las variables
        paciente =self.svPaci.get()
        fecha = self.svfechaP.get()
        Diagnóstico_final = self.svDF.get()

        # Etiquetas para los campos básicos
        tk.Label(main_frame, text=f'Paciente: {paciente}').grid(row=0, column=2, sticky="w", padx=10, pady=5)
        tk.Label(main_frame, text=f'Fecha: {fecha}').grid(row=1, column=2, sticky="w", padx=10, pady=5)
        tk.Label(main_frame, text=f'Diagnóstico Final:').grid(row=2, column=0, sticky="w", padx=5, pady=5)

        # Crear el widget Text para el diagnóstico final y la barra de desplazamiento
        self.text_diagnostico = tk.Text(main_frame, width=30, height=10, font=('ARIAL', 10,'bold'))
        self.text_diagnostico.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        scrollbar = Scrollbar(main_frame, command=self.text_diagnostico.yview)
        scrollbar.grid(row=2, column=4, sticky="ns")
        self.text_diagnostico.config(yscrollcommand=scrollbar.set)

        # Asignar el diagnóstico final al widget Text
        self.text_diagnostico.insert(tk.END, Diagnóstico_final)

        # Botones
        tk.Button(main_frame, text="Guardar", command=self.guardar_datosPdf, width=12, font=('Arial', 10, 'bold'), fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE').grid(row=3, column=1, pady=5)
        tk.Button(main_frame, text="Cerrar", command=self.root.destroy, width=12, font=('Arial', 10, 'bold'), fg='#FFFEFE', bg='#CF811E', cursor='hand2', activebackground='#E72D40').grid(row=3, column=2, pady=5)

    #funcion utilizada para guardar la receta
    def guardar_datosPdf(self):
        try:
            # Obtener el texto del diagnóstico final
            diagnostico_final = self.text_diagnostico.get('1.0', tk.END).strip()

            # Crear un gráfico con los datos
            fig, ax = plt.subplots(figsize=(8, 6))

            # Dividir el texto del diagnóstico en varias líneas para que se ajuste al ancho de la página
            lines = diagnostico_final.split('\n')
            max_chars_per_line = 30  # Número máximo de caracteres por línea
            formatted_diagnosis = '\n'.join([line[i:i+max_chars_per_line] for line in lines for i in range(0, len(line), max_chars_per_line)])

            ax.text(0.5, 0.5, "Datos de la Receta Médica:\n\n\n" +
                    f"Paciente: {self.svPaci.get()}\n\n" +
                    f"Fecha: {self.svfechaP.get()}\n\n" +
                    f"Diagnóstico:\n{formatted_diagnosis}", 
                    fontsize=14, ha='center', va='center')

            ax.axis('off')

            # Obtener una ruta para guardar el archivo PDF
            ruta_archivo = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("Archivos PDF", "*.pdf")])

            if not ruta_archivo:
                plt.close()  # Cerrar la ventana de vista previa
                return  # El usuario canceló el diálogo de guardado

            # Guardar el gráfico en el PDF
            with PdfPages(ruta_archivo) as pdf:
                pdf.savefig(fig)
                plt.close()  # Cerrar la ventana de vista previa

            messagebox.showinfo("Imprimir", f"Datos guardados exitosamente en '{ruta_archivo}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al imprimir los datos: {str(e)}")

    def cerrar_ventana(self):
    # Cierra la ventana principal
        self.root.destroy()

root = tk.Tk()
ventana = VentanaDiagnosticoMedico(root)
ventana.pack()
root.mainloop()
