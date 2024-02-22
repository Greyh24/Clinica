import csv
import os
import tkinter as tk
from tkinter import messagebox
from historiamedica import HistoriaMedicaApp
from tkinter import simpledialog
from PIL import Image, ImageTk  
from paciente.ventana_doctor import VentanaDiagnosticoMedico

class Login:
    def __init__(self, root,callback=None):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.configure(bg='#8C9BBA')  # Color de fondo para la ventana principal
        self.callback = callback

        # Cargar la imagen y redimensionarla
        image = Image.open("C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/logo.jfif")
        image = image.resize((150, 150))
        self.logo = ImageTk.PhotoImage(image)

        # Mostrar la imagen en un Label
        tk.Label(root, image=self.logo, bg='#8C9BBA').grid(row=0, column=1, padx=5, pady=25, sticky="nsew")

        # Variables para almacenar el usuario, contraseña y perfil de usuario
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()
        self.Perfil_de_Usuario = tk.StringVar()
        self.Perfil_de_Usuario.set("Administracion")  # Valor por defecto

        # Entradas de texto para usuario y contraseña
        tk.Label(root, text="Usuario:", bg='#8C9BBA', font=(((('ARIAL',8, 'bold'))))).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.usuario, width=30).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Contraseña:", bg='#8C9BBA', font=((('ARIAL', 8, 'bold')))).grid(row=2, column=0, padx=5, pady=5)
        self.contrasena_entry = tk.Entry(root, textvariable=self.contrasena, width=30, show="*")
        self.contrasena_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Cargar la imagen del icono de ojo y redimensionarla
        image_eye = Image.open("C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/eye_icon.png")
        image_eye = image_eye.resize((20, 15))
        self.eye_icon = ImageTk.PhotoImage(image_eye)

        # Crear un botón con la imagen del icono de ojo para mostrar u ocultar la contraseña
        self.show_password_button = tk.Button(root, image=self.eye_icon, command=self.toggle_password_visibility)
        self.show_password_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # OptionMenu para seleccionar el perfil de usuario
        tk.Label(root, text="Perfil de usuario:", bg='#8C9BBA', font=(((('ARIAL',8, 'bold'))))).grid(row=3, column=0, padx=5, pady=5)
        opciones_perfil = ["Administracion", "Medico"]
        tk.OptionMenu(root, self.Perfil_de_Usuario, *opciones_perfil).grid(row=3, column=1, padx=5, pady=5)

        # Botón de inicio de sesión y registrar usuario
        tk.Button(root, text="Iniciar Sesión", width=15, fg='#FFFEFE', bg='#1658A2', cursor='hand2', activebackground='#3D69F0', font=(((('ARIAL',8, 'bold')))), command=self.iniciar_sesion).grid(row=4, column=1, padx=5, pady=20, sticky="ew")
        
        tk.Button(root, text="Registrar Usuario", width=15, fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE', font=(((('ARIAL',8, 'bold')))), command=self.Ventana_registrar_usuario).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Centrar la ventana en la pantalla
        window_width = 380  # Ancho de la ventana
        window_height = 450  # Altura de la ventana
        screen_width = root.winfo_screenwidth()  # Ancho de la pantalla
        screen_height = root.winfo_screenheight()  # Altura de la pantalla
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def abrir_ventana_login(self):
        # Crear y mostrar la ventana de inicio de sesión
        # Llamar al callback después de cerrar la ventana de inicio de sesión
        self.callback()

    def verificar_datos(self):
        with open('Usuarios.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if row['usuario'] == self.usuario.get() and row['contrasena'] == self.contrasena.get() and row['perfil'] == self.Perfil_de_Usuario.get():
                    return row['perfil']
        return None

    def iniciar_sesion(self):
        perfil = self.verificar_datos()

        if perfil == 'Administracion':
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso como Administrador.")
            self.root.destroy()  # Cerrar la ventana de inicio de sesión
            # Redirigir al usuario a HistoriaMedicaApp
            root = tk.Tk()
            app = HistoriaMedicaApp(root)
            root.mainloop()

        elif perfil == 'Medico':
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso como Médico.")
            # Cerrar la ventana de inicio de sesión
            self.root.destroy()
            # Abrir la ventana de diagnóstico médico
            root_doctor = tk.Tk()
            ventana_doctor = VentanaDiagnosticoMedico(root_doctor)
            root_doctor.mainloop()
        else:
            messagebox.showerror("Error", "Datos incorrectos o perfil no autorizado.")

    def toggle_password_visibility(self):
        # Muestra u oculta la contraseña según el estado actual
        if self.contrasena_entry.cget("show") == "":
            self.contrasena_entry.config(show="*")
        else:
            self.contrasena_entry.config(show="")

    def toggle_password_visibility_registro(self):
        # Muestra u oculta la contraseña en la ventana de registro según el estado actual
        if self.contrasena_registro_entry.cget("show") == "":
            self.contrasena_registro_entry.config(show="*")
        else:
            self.contrasena_registro_entry.config(show="")

    def Ventana_registrar_usuario(self):
        # Crear la nueva ventana
        ventana_registrar = tk.Toplevel()
        ventana_registrar.title("Registrar Usuario")
        ventana_registrar.geometry("345x250")
        ventana_registrar.configure(bg='#8C9BBA')  # Color de fondo para la ventana emergente

        # Variables para almacenar el usuario, contraseña y perfil de usuario
        self.usuario_registro = tk.StringVar()
        self.contrasena_registro = tk.StringVar()
        self.perfil_registro = tk.StringVar()

        # Función para registrar un nuevo usuario
        def crear_usuario():
            usuario = self.usuario_registro.get()
            contrasena = self.contrasena_registro.get()
            perfil = self.perfil_registro.get()

            with open('Usuarios.csv', 'a', newline='') as file:
                csv_writer = csv.writer(file)
                # Verificar si el archivo está vacío para escribir el encabezado
                if os.path.getsize('Usuarios.csv') == 0:
                    csv_writer.writerow(['usuario', 'contrasena', 'perfil'])
                csv_writer.writerow([usuario, contrasena, perfil])
                messagebox.showinfo("Registro de Usuario", "Usuario registrado exitosamente.")
                ventana_registrar.destroy()  # Cerrar la ventana después de registrar el usuario

        # Etiquetas y campos de entrada para usuario, contraseña y perfil de usuario
        tk.Label(ventana_registrar, text="Nuevo Usuario:", bg='#8C9BBA', font=((('ARIAL', 14, 'bold')))).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        tk.Label(ventana_registrar, text="Usuario:", bg='#8C9BBA', font=((('ARIAL', 8, 'bold')))).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(ventana_registrar, textvariable=self.usuario_registro, width=30).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(ventana_registrar, text="Contraseña:", bg='#8C9BBA', font=((('ARIAL', 8, 'bold')))).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.contrasena_registro_entry = tk.Entry(ventana_registrar, textvariable=self.contrasena_registro, width=30, show="*")
        self.contrasena_registro_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Cargar la imagen del icono de ojo y redimensionarla
        image_eye = Image.open("C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/eye_icon.png")
        image_eye = image_eye.resize((20, 15))
        self.eye_icon_registro = ImageTk.PhotoImage(image_eye)

        # Crear un botón con la imagen del icono de ojo para mostrar u ocultar la contraseña
        show_password_button_registro = tk.Button(ventana_registrar, image=self.eye_icon_registro, command=self.toggle_password_visibility_registro)
        show_password_button_registro.grid(row=2, column=2, padx=5, pady=5, sticky="w")

        # OptionMenu para seleccionar el perfil de usuario o crear uno nuevo
        tk.Label(ventana_registrar, text="Perfil de usuario:", bg='#8C9BBA', font=((('ARIAL', 8, 'bold')))).grid(row=3, column=0, padx=5, pady=5, sticky="w")
        opciones_perfil = ["Administracion", "Medico"]
        perfil_registrado = tk.OptionMenu(ventana_registrar, self.perfil_registro, *opciones_perfil)
        perfil_registrado.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Botones para crear usuario y cancelar
        tk.Button(ventana_registrar, text="Crear Usuario", width=15, fg='#FFFEFE', bg='#1658A2', cursor='hand2', activebackground='#3D69F0', font=((('ARIAL', 8, 'bold'))), command=crear_usuario).grid(row=4, column=1, padx=5, pady=20, sticky="ew")
        tk.Button(ventana_registrar, text="Cancelar", width=15, fg='#FFFEFE', bg='#0F1010', cursor='hand2', activebackground='#FFFEFE', font=((('ARIAL', 8, 'bold'))), command=ventana_registrar.destroy).grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Centrar la ventana en la pantalla
        ventana_registrar.update_idletasks()
        ventana_width = ventana_registrar.winfo_width()
        ventana_height = ventana_registrar.winfo_height()
        screen_width = ventana_registrar.winfo_screenwidth()
        screen_height = ventana_registrar.winfo_screenheight()
        x = (screen_width - ventana_width) // 2
        y = (screen_height - ventana_height) // 2
        ventana_registrar.geometry(f"{ventana_width}x{ventana_height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root, None)  # Pasa None como callback
    root.mainloop()
