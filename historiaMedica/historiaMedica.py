import tkinter as tk
from tkinter import Menu
from paciente.ventana_adultos import VentanaAdultos
from paciente.ventana_ninos import VentanaNinos

class HistoriaMedicaApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Historia Medica')
        self.root.resizable(0, 0)

        self.create_menu()

        # Inicializa una instancia del marco principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Inicializa instancias de las clases para las interfaces de paciente adulto y paciente niño
        self.paciente_frame = VentanaAdultos(self.main_frame)
        self.paciente_niño_frame = VentanaNinos(self.main_frame)

        # Muestra la interfaz de paciente adulto al inicio
        self.show_paciente_adulto()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # Menú Paciente
        paciente_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Paciente", menu=paciente_menu)

        # Opciones específicas para el paciente adulto
        paciente_menu.add_command(label="Adulto", command=self.show_paciente_adulto)

        # Opciones específicas para el paciente niño
        paciente_menu.add_command(label="Niño", command=self.show_paciente_niño)

    def show_paciente_adulto(self):
        # Oculta la interfaz de paciente niño
        self.paciente_niño_frame.pack_forget()
        # Muestra la interfaz de paciente adulto
        self.paciente_frame.pack(fill=tk.BOTH, expand=True)
        # Actualiza la tabla de pacientes adultos
        self.paciente_frame.actualizar_tabla()

    def show_paciente_niño(self):
        # Oculta la interfaz de paciente adulto
        self.paciente_frame.pack_forget()
        # Muestra la interfaz de paciente niño
        self.paciente_niño_frame.pack(fill=tk.BOTH, expand=True)
        # Actualiza la tabla de pacientes niños
        self.paciente_niño_frame.load_data_to_table()

    def center_window(self):
        # Función para centrar la ventana principal
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 1250
        window_height = 620

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

def main():
    root = tk.Tk()
    app = HistoriaMedicaApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()