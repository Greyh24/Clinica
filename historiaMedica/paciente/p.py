   def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, width=1300, height=620)
        self.frame.pack()
        self.root.title("Diagnóstico Médico")
        self.canvas = tk.Canvas(self.frame, bg='#8C9BBA', width=1300, height=620)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width - 1320) // 2 
        y_coordinate = (screen_height - 620) // 2  
        self.root.geometry(f"1320x620+{x_coordinate}+{y_coordinate}")
        self.scrollable_frame = tk.Frame(self.canvas, bg='#8C9BBA')
        self.scrollable_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        self.scrollbar_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar_y.set)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        datos_frame = tk.Frame(self.scrollable_frame, bg='#8C9BBA')
        datos_frame.grid(column=2, row=1, padx=5, pady=5, sticky='ew')
        self.camposDiagnosticoMedico()
        self.menu_bar = Menu(root)
        root.config(menu=self.menu_bar)
        self.menu_bar.add_command(label="Cerrar Sesión", command=self.cerrar_sesion)
    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    def mostrar_imagen(self, event, contenedor):
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if ruta_imagen:
            imagen = Image.open(ruta_imagen) 
            self.mostrar_imagen_en_label(imagen, contenedor)
    def mostrar_imagen_en_label(self, imagen, contenedor):
        imagen.thumbnail((150, 100))
        imagen_tk = ImageTk.PhotoImage(imagen)
        contenedor.config(image=imagen_tk)
        contenedor.image = imagen_tk 
        if contenedor == self.contenedor_MedRes:
            self.imagen_tk_MedRes = imagen_tk
        elif contenedor == self.contenedor_ExaAdi:
            self.imagen_tk_ExaAdi = imagen_tk
    def mostrar_cuadro_dialogo(self, event):
        ruta_imagen = filedialog.askopenfilename(title="Seleccionar Imagen", filetypes=[("Archivos de imagen", "*.png;*.jpg;*.jpeg")])
        if ruta_imagen:
            self.lista_imagenes.insert(tk.END, ruta_imagen)
            self.lista_imagenes.selection_clear(0, tk.END)
            self.lista_imagenes.selection_set(tk.END)
            self.seleccionar_imagen()
    def seleccionar_imagen(self, event=None):
        seleccion = self.lista_imagenes.curselection()
        if seleccion:
            indice = int(seleccion[0])
            ruta_imagen = self.lista_imagenes.get(indice)
            imagen = Image.open(ruta_imagen)
            self.mostrar_imagen_en_label(imagen, self.contenedor_ExaAdi)
    def cerrar_sesion(self):
        self.root.destroy()
        login_module = __import__('login')
        Login = getattr(login_module, 'Login')
        root_login = tk.Tk()
        login_page = Login(root_login)
        root_login.mainloop()
    def camposDiagnosticoMedico(self):
        self.lblMedRes = tk.Label(self.scrollable_frame, text='Firma y Nombre del medico responsable: ', font=('ARIAL', 10, 'bold','underline'), underline=6, fg='black', bg='#8C9BBA')
        self.lblMedRes.grid(column=3, row=54, padx=0, pady=5)
        self.contenedor_MedRes = tk.Label(self.scrollable_frame, bg='#ffffff')
        self.contenedor_MedRes.grid(column=3, row=53, padx=5, pady=5)
        self.imagen_tk_MedRes = None
        self.contenedor_MedRes.bind("<Button-1>", lambda event, contenedor=self.contenedor_MedRes: self.mostrar_imagen(event, contenedor))
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
        ruta_predeterminada = "C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/galeria.png"
        imagen_predeterminada = Image.open(ruta_predeterminada)
        self.mostrar_imagen_en_label(imagen_predeterminada, self.contenedor_ExaAdi)
    def generar_pdf(self):
        datos_gui = self.obtener_datos()
        root = tk.Tk()
        root.withdraw()  
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
        c = canvas.Canvas(file_path, pagesize=letter)
        y_actual = 750
        espacio_requerido = 20  
        espacio_pagina = 750 
        def hay_espacio_suficiente():
            return y_actual - espacio_requerido > 0
        def crear_nueva_pagina():
            nonlocal c, y_actual
            c.showPage()  
            y_actual = espacio_pagina
        def agregar_texto(texto):
            nonlocal y_actual
            c.drawString(100, y_actual, texto)
            y_actual -= espacio_requerido  
        agregar_texto("{}".format(datos_gui["Diagnostico_Medico"]))
        agregar_texto("Paciente: {}".format(datos_gui["Paciente"]))
        y_paciente = y_actual - espacio_requerido
        campos_paciente = [("Edad", datos_gui["Edad"]),("Sexo", datos_gui["Sexo"]),("Dirección", datos_gui["Direccion"]),("Distrito", datos_gui["Distrito"]),("Responsable", datos_gui["Responsable"]),("Modo de Ingreso", datos_gui["Modo_Ingreso"]),("DNI", datos_gui["DNI"]),("Tipo de Accidente", datos_gui["Tipo_AccidenteP"]or ""),("Tipo de Seguro", datos_gui["Tipo_Seg"]),("Teléfono", datos_gui["Telefono"]),("Ficha", datos_gui["Ficha"]),("Fecha de Presentación", datos_gui["Fecha_P"]),("Hora de Presentación", datos_gui["Hora_P"]),("Historia", datos_gui["Historia"]),]
        for campo, valor in campos_paciente:
            if y_paciente - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_paciente = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_paciente -= espacio_requerido
        especialidades = [("Medicina", self.svMedicina),("Pediatria", self.svPediatria),("Cirugia", self.svCirugia),("Gineco OBS", self.svGineco_OBS),]
        for especialidad, variable in especialidades:
            if variable.get():
                agregar_texto("Especialidad: {}".format(especialidad))
        y_accidente = y_paciente - espacio_requerido
        campos_accidente = [("Prioridad de Daño",self.obtener_valor_seleccionado(datos_gui["Prioridad_Daño"])),("Tipo de Accidente", self.obtener_valor_seleccionado(datos_gui["Tipo_Accidente"])),("Otros Accidentes", datos_gui["Otros_Accidente"]),("Fecha del Accidente", datos_gui["Fecha_Accidente"]),("Hora del Accidente", datos_gui["Hora_Accidente"]),]
        for campo, valor in campos_accidente:
            if y_accidente - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_accidente = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_accidente -= espacio_requerido
        y_anamnesis = y_accidente - espacio_requerido
        campos_anamnesis = [("Tiempo de Enfermedad", datos_gui["Tiempo_Enfermedad"]),("Motivo de Consulta", datos_gui["Motivo_Consulta"]),("Antecedentes", datos_gui["Antecedentes"]),]
        for campo, valor in campos_anamnesis:
            if y_anamnesis - espacio_requerido < 0:
                crear_nueva_pagina() 
                y_anamnesis = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_anamnesis -= espacio_requerido
        y_examen_clinico = y_anamnesis - espacio_requerido
        campos_examen_clinico = [("P.A", datos_gui["P.A"]),("FC", datos_gui["FC"]),("FR", datos_gui["FR"]),("Tº", datos_gui["Tº"]),("SO", datos_gui["SO"]),("Peso", datos_gui["Peso"]),]
        for campo, valor in campos_examen_clinico:
            if y_examen_clinico - espacio_requerido < 0:
                crear_nueva_pagina() 
                y_examen_clinico = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_examen_clinico -= espacio_requerido
        y_examen_preferencial = y_examen_clinico - espacio_requerido
        if y_examen_preferencial - espacio_requerido < 0:
            crear_nueva_pagina() 
        agregar_texto("Examen Preferencial: {}".format(datos_gui["Examen_Preferencial"]))
        y_diagnostico_ingreso = y_examen_preferencial - espacio_requerido
        if y_diagnostico_ingreso - espacio_requerido < 0:
            crear_nueva_pagina() 
        agregar_texto("Diagnóstico de Ingreso: {}".format(datos_gui["Diagnostico_Ingreso"]))
        agregar_texto("COD CIE-10: {}".format(datos_gui["COD_CIE_10"]))
        y_plan_trabajo = y_diagnostico_ingreso - espacio_requerido
        campos_plan_trabajo = [("Hidratación", datos_gui["Plan_Trabajo"]["Hidratacion"]),("Tratamiento", datos_gui["Plan_Trabajo"]["Tratamiento"]),]
        for campo, valor in campos_plan_trabajo:
            if y_plan_trabajo - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_plan_trabajo = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_plan_trabajo -= espacio_requerido
        y_examenes_auxiliares = y_plan_trabajo - espacio_requerido
        campos_examenes_auxiliares = [("Laboratorio", datos_gui["Examenes_Auxiliares"]["Laboratorio"]),("Radiología", datos_gui["Examenes_Auxiliares"]["Radiologia"]),("Ecografía", datos_gui["Examenes_Auxiliares"]["Ecografia"]),("Otros", datos_gui["Examenes_Auxiliares"]["Otros"]),]
        if y_examenes_auxiliares - espacio_requerido < 0:
            crear_nueva_pagina()  
        agregar_texto("Examenes Auxiliares:")
        for campo, valor in campos_examenes_auxiliares:
            if y_examenes_auxiliares - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_examenes_auxiliares = espacio_pagina
            if valor:
                agregar_texto("{}".format(campo))
            y_examenes_auxiliares -= espacio_requerido
        y_procedimientos = y_examenes_auxiliares - espacio_requerido
        if y_procedimientos - espacio_requerido < 0:
            crear_nueva_pagina() 
        agregar_texto("Procedimientos: {}".format(datos_gui["Procedimientos"]))
        y_diagnostico_final = y_procedimientos - espacio_requerido
        campos_diagnostico_final = [("Diagnóstico Final", datos_gui["Diagnostico_Final"]),("COD CIE-10", datos_gui["COD_CIE_10f"]), ]
        for campo, valor in campos_diagnostico_final:
            if y_diagnostico_final - espacio_requerido < 0:
                crear_nueva_pagina()  
                y_diagnostico_final = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_diagnostico_final -= espacio_requerido
        y_indicaciones = y_diagnostico_final - espacio_requerido
        campos_indicaciones = [("Indicaciones", datos_gui["Indicaciones"]),]
        for campo, valor in campos_indicaciones:
            if y_indicaciones - espacio_requerido < 0:
                crear_nueva_pagina() 
                y_indicaciones = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_indicaciones -= espacio_requerido
        y_observaciones = y_indicaciones - espacio_requerido
        campos_observaciones = [("Observaciones", datos_gui["Observaciones"]),]
        for campo, valor in campos_observaciones:
            if y_observaciones - espacio_requerido < 0:
                crear_nueva_pagina() 
                y_observaciones = espacio_pagina
            agregar_texto("{}: {}".format(campo, valor))
            y_observaciones -= espacio_requerido
        y_destino = y_observaciones - espacio_requerido
        campos_destino = [
            ("Alta", datos_gui["Destino"].get("Alta", "")),("Observación", datos_gui["Destino"].get("Observacion", "")),("Unidad Paciente Crítico", datos_gui["Destino"].get("UPC", "")),("Hospitalización", datos_gui["Destino"].get("Hospitalizacion", "")),("Centro Obstétrico", datos_gui["Destino"].get("Centro_Obstetrico", "")),("Centro Quirúrgico", datos_gui["Destino"].get("Centro_Quirurgico", "")),("Referencia/Transferencia", datos_gui["Destino"].get("Referencia_Transferencia", "")),("Lugar", datos_gui["Destino"].get("Lugar", "")),("Hora", datos_gui["Destino"].get("Hora", "")),("Retiro Voluntario", datos_gui["Destino"].get("Retiro_Voluntario", "")),("Fuga", datos_gui["Destino"].get("Fuga", "")),("Mortuorio", datos_gui["Destino"].get("Mortuorio", "")),("No Atendido", datos_gui["Destino"].get("No_Atendido", "")),]
        if y_destino - espacio_requerido < 0:
            crear_nueva_pagina()  
        agregar_texto("Destino:")
        for campo, valor in campos_destino:
            if valor:  
                if y_destino - espacio_requerido < 0:
                    crear_nueva_pagina() 
                    y_destino = espacio_pagina
                if campo == "Observación":
                    agregar_texto("{}".format(campo, valor))
                elif campo in ["Lugar", "Hora"]:
                    agregar_texto("{}: {}".format(campo, valor))
                else:
                    agregar_texto("{}".format(campo))
                y_destino -= espacio_requerido
        c.save()
    def obtener_valor_seleccionado(self, diccionario):
        if not diccionario or not isinstance(diccionario, dict):
            return ""
        clave = next(iter(diccionario.keys()), '')
        return clave if diccionario[clave] else ""
    def obtener_datos(self):
        datos = {}
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
        especialidades = {key: value.get() for key, value in {'Medicina': self.svMedicina,'Pediatria': self.svPediatria,'Cirugia': self.svCirugia,'Gineco_OBS': self.svGineco_OBS,}.items() if value.get()}
        if especialidades:
            datos['Especialidad'] = especialidades
        else:
            datos['Especialidad'] = None  
        datos['Prioridad_Daño'] = {key: value.get() for key, value in {'Prioridad1': self.svPriorid1,'Prioridad2': self.svPriorid2,'Prioridad3': self.svPriorid3,'Prioridad4': self.svPriorid4,}.items() if value.get()}
        datos['Tipo_Accidente'] = {key: value.get() for key, value in {'Atropello': self.svAtrop,'Choque': self.svChoque,'Despiste': self.svDespiste,'Incendio': self.svIncendio,'Atropello_y_Fuga': self.svAyF,'Choque_y_Fuga': self.svCyF,'Caida_de_Pasajeros': self.svCaidaP,'Volcadura': self.svVolcadura,}.items() if value.get()}
        datos['Otros_Accidente'] = self.svOtrosAT.get()
        datos['Fecha_Accidente'] = self.svFechaAT.get()
        datos['Hora_Accidente'] = self.svHoraAT.get()
        datos['Tiempo_Enfermedad'] = self.svTipoE.get()
        datos['Motivo_Consulta'] = self.svMC.get()
        datos['Antecedentes'] = self.svAntecedentes.get()
        datos['P.A'] = self.svPA.get()
        datos['FC'] = self.svFC.get()
        datos['FR'] = self.svFR.get()
        datos['Tº'] = self.svTemp.get()
        datos['SO'] = self.svSO.get()
        datos['Peso'] = self.svPeso.get()
        datos['Examen_Preferencial'] = self.svExamenP.get()
        datos['Diagnostico_Ingreso'] = self.svDdi.get()
        datos['COD_CIE_10'] = self.svCodCie.get()
        datos['Plan_Trabajo'] = {'Hidratacion': 'Si' if self.svHidratS.get() else 'No','Tratamiento': self.entryTratam.get("1.0", "end-1c") if self.svHidratS.get() else '',}
        datos['Examenes_Auxiliares'] = {'Laboratorio': self.svLaboratorio.get(),'Radiologia': self.svRadiología.get(),'Ecografia': self.svEcografía.get(),'Otros': self.svOtros.get(),}
        datos['Procedimientos'] = self.entryProcedimientos.get("1.0", "end-1c")
        datos['Diagnostico_Final'] = self.svDF.get()
        datos['COD_CIE_10f'] = self.svCodCief.get()
        datos['Indicaciones'] = self.entryIndicaciones.get("1.0", "end-1c")
        datos['Observaciones'] = self.entryObservaciones.get("1.0", "end-1c")
        datos['Destino'] = {'Alta': self.svAlta.get(),'Observacion': self.svObservación.get(),'UPC': self.svUPC.get(),'Hospitalizacion': self.svHospitalización.get(),'Centro_Obstetrico': self.svCObs.get(),'Centro_Quirurgico': self.svCquir.get(),'Referencia_Transferencia': self.svR_Trans.get(),'Lugar': self.svLugar.get(),'Hora': self.svHoraD.get(),'Retiro_Voluntario': self.svRetVol.get(),'Fuga': self.svFuga.get(),'Mortuorio': self.svMortuorio.get(),'No_Atendido': self.svNAtend.get(),}
        return datos
     def guardar_pdf(self, datos, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, "Diagnóstico Médico: {}".format(datos["Diagnostico_Medico"]))
        c.drawString(100, 730, "Paciente: {}".format(datos["Paciente"]))
        y_paciente = 710
        campos_paciente = [("Edad", datos["Edad"]),("Sexo", datos["Sexo"]),("Dirección", datos["Direccion"]),("Distrito", datos["Distrito"]),("Responsable", datos["Responsable"]),("Modo de Ingreso", datos["Modo_Ingreso"]),("DNI", datos["DNI"]),("Tipo de Accidente", datos["Tipo_AccidenteP"] or ""),("Tipo de Seguro", datos["Tipo_Seg"]),("Teléfono", datos["Telefono"]),("Ficha", datos["Ficha"]),("Fecha de Presentación", datos["Fecha_P"]),("Hora de Presentación", datos["Hora_P"]),("Historia", datos["Historia"]),("Especialidad", datos.get("Especialidad", "")),]
        for campo, valor in campos_paciente:
            c.drawString(100, y_paciente, "{}: {}".format(campo, valor))
            y_paciente -= 20
        y_accidente = y_paciente - 20
        campos_accidente = [("Prioridad de Daño", datos["Prioridad_Daño"]or ""),("Tipo de Accidente", datos["Tipo_Accidente"]or ""),("Otros Accidentes", datos["Otros_Accidente"]),("Fecha del Accidente", datos["Fecha_Accidente"]),("Hora del Accidente", datos["Hora_Accidente"]),]
        for campo, valor in campos_accidente:
            c.drawString(100, y_accidente, "{}: {}".format(campo, valor))
            y_accidente -= 20
        y_anamnesis = y_accidente - 20
        campos_anamnesis = [("Tiempo de Enfermedad", datos["Tiempo_Enfermedad"]),("Motivo de Consulta", datos["Motivo_Consulta"]),("Antecedentes", datos["Antecedentes"]),]
        for campo, valor in campos_anamnesis:
            c.drawString(100, y_anamnesis, "{}: {}".format(campo, valor))
            y_anamnesis -= 20
        y_examen_clinico = y_anamnesis - 20
        campos_examen_clinico = [("P.A", datos["P.A"]),("FC", datos["FC"]),("FR", datos["FR"]),("Tº", datos["Tº"]),("SO", datos["SO"]),("Peso", datos["Peso"]),]
        for campo, valor in campos_examen_clinico:
            c.drawString(100, y_examen_clinico, "{}: {}".format(campo, valor))
            y_examen_clinico -= 20
        y_examen_preferencial = y_examen_clinico - 20
        c.drawString(100, y_examen_preferencial, "Examen Preferencial: {}".format(datos["Examen_Preferencial"]))
        y_diagnostico_ingreso = y_examen_preferencial - 20
        c.drawString(100, y_diagnostico_ingreso, "Diagnóstico de Ingreso: {}".format(datos["Diagnostico_Ingreso"]))
        c.drawString(100, y_diagnostico_ingreso - 20, "COD CIE-10: {}".format(datos["COD_CIE_10"]))
        y_plan_trabajo = y_diagnostico_ingreso - 40
        campos_plan_trabajo = [("Hidratación", datos["Plan_Trabajo"]["Hidratacion"]),("Tratamiento", datos["Plan_Trabajo"]["Tratamiento"]),]
        for campo, valor in campos_plan_trabajo:
            c.drawString(100, y_plan_trabajo, "{}: {}".format(campo, valor))
            y_plan_trabajo -= 20
        y_examenes_auxiliares = y_plan_trabajo - 20
        campos_examenes_auxiliares = [("Laboratorio", datos["Examenes_Auxiliares"]["Laboratorio"]),("Radiología", datos["Examenes_Auxiliares"]["Radiologia"]),("Ecografía", datos["Examenes_Auxiliares"]["Ecografia"]),("Otros", datos["Examenes_Auxiliares"]["Otros"]),]
        c.drawString(100, y_examenes_auxiliares, "Examenes Auxiliares:")
        for campo, valor in campos_examenes_auxiliares:
            c.drawString(120, y_examenes_auxiliares - 20, "{}: {}".format(campo, valor))
            y_examenes_auxiliares -= 20
        y_procedimientos = y_examenes_auxiliares - 20
        c.drawString(100, y_procedimientos, "Procedimientos: {}".format(datos["Procedimientos"]))
        y_diagnostico_final = y_procedimientos - 20
        campos_diagnostico_final = [("Diagnóstico Final", datos["Diagnostico_Final"]),("COD CIE-10f", datos["COD_CIE_10f"]),]
        for campo, valor in campos_diagnostico_final:
            c.drawString(100, y_diagnostico_final, "{}: {}".format(campo, valor))
            y_diagnostico_final -= 20
        y_indicaciones = y_diagnostico_final - 20
        campos_indicaciones = [("Indicaciones", datos["Indicaciones"]),]
        for campo, valor in campos_indicaciones:
            c.drawString(100, y_indicaciones, "{}: {}".format(campo, valor))
            y_indicaciones -= 20
        y_observaciones = y_indicaciones - 20
        campos_observaciones = [("Observaciones", datos["Observaciones"]),]
        for campo, valor in campos_observaciones:
            c.drawString(100, y_observaciones, "{}: {}".format(campo, valor))
            y_observaciones -= 20
        y_destino = y_observaciones - 20
        campos_destino = [("Alta", datos["Destino"]["Alta"]),("Observación", datos["Destino"]["Observacion"]),("UPC", datos["Destino"]["UPC"]),("Hospitalización", datos["Destino"]["Hospitalizacion"]),("Centro Obstétrico", datos["Destino"]["Centro_Obstetrico"]),("Centro Quirúrgico", datos["Destino"]["Centro_Quirurgico"]),("Referencia/Transferencia", datos["Destino"]["Referencia_Transferencia"]),("Lugar", datos["Destino"]["Lugar"]),("Hora", datos["Destino"]["Hora"]),("Retiro Voluntario", datos["Destino"]["Retiro_Voluntario"]),("Fuga", datos["Destino"]["Fuga"]),("Mortuorio", datos["Destino"]["Mortuorio"]),("No Atendido", datos["Destino"]["No_Atendido"]),]
        c.drawString(100, y_destino, "Destino:")
        for campo, valor in campos_destino:
            c.drawString(120, y_destino - 20, "{}: {}".format(campo, valor))
            y_destino -= 20
        c.save()