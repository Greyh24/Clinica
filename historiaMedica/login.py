import csv
import tkinter as tk
from tkinter import messagebox
from historiamedica import HistoriaMedicaApp
from tkinter import simpledialog
from PIL import Image, ImageTk  
from paciente.ventana_doctor import VentanaDiagnosticoMedico

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.configure(bg='#8C9BBA')  # Color de fondo para la ventana principal

        # Cargar la imagen y redimensionarla
        image = Image.open("C:/Users/Yo/Desktop/Clinica/historiaMedica/imagenes/logo.jfif")
        image = image.resize((100, 100))
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

        tk.Label(root, text="Contraseña:", bg='#8C9BBA', font=(((('ARIAL',8, 'bold'))))).grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.contrasena, width=30, show="*").grid(row=2, column=1, padx=5, pady=5)

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

    def registrar_usuario(self):
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()
        perfil = self.Perfil_de_Usuario.get()

        with open('Usuarios.csv', 'a', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([usuario, contrasena, perfil])
            messagebox.showinfo("Registro de Usuario", "Usuario registrado exitosamente.")

    def Ventana_registrar_usuario(self):
        # Crear la nueva ventana
        ventana_registrar = tk.Toplevel()
        ventana_registrar.title("Registrar Usuario")
        ventana_registrar.geometry("325x250")
        ventana_registrar.configure(bg='#8C9BBA')  # Color de fondo para la ventana emergente

        # Variables para almacenar el usuario, contraseña y perfil de usuario
        usuario_registro = tk.StringVar()
        contrasena_registro = tk.StringVar()
        perfil_registro = tk.StringVar()

        # Función para registrar un nuevo usuario
        def crear_usuario():
            usuario = usuario_registro.get()
            contrasena = contrasena_registro.get()
            perfil = perfil_registro.get()

            with open('Usuarios.csv', 'a', newline='') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow([usuario, contrasena, perfil])
                messagebox.showinfo("Registro de Usuario", "Usuario registrado exitosamente.")
                ventana_registrar.destroy()  # Cerrar la ventana después de registrar el usuario

        # Resto del código de la ventana de registro de usuario ...


if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.mainloop()
