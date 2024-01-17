from .conexion import ConexionDB
from tkinter import messagebox

class adulto:
    def __init__(self, historiaClinica, fecha, nombre, apellido, dni, sexo, edad, fechaNacimiento, telefono):
        self.idadulto = None
        self.historiaClinica = historiaClinica
        self.fecha = fecha
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.sexo = sexo
        self.edad = edad
        self.fechaNacimiento = fechaNacimiento
        self.telefono = telefono

    def actualizar_idadulto(self, idadulto):
        self.idadulto = idadulto

    def __str__(self):
        return f'adulto[{self.historiaClinica},{self.fecha},{self.nombre},{self.apellido},{self.dni},{self.sexo},{self.edad},{self.fechaNacimiento},{self.telefono}]'

def guardarDatpAdulto(Adulto):
    conexion = ConexionDB()
    sql = f"""INSERT INTO adulto (historiaClinica,fecha,nombre,apellido,dni,sexo,edad,fechaNacimiento,telefono) VALUES 
        ('{Adulto.historiaClinica}','{Adulto.fecha}','{Adulto.nombre}','{Adulto.apellido}','{Adulto.dni}','{Adulto.sexo}','{Adulto.edad}','{Adulto.fechaNacimiento}','{Adulto.telefono}')"""
    
    try:
        conexion.cursor.execute(sql)
        idadulto = conexion.cursor.lastrowid  # Obtener el último ID insertado
        Adulto.actualizar_idadulto(idadulto)  # Actualizar el atributo idadulto en el objeto Adulto
        conexion.cerrarConexion()

        title = 'Registrar Paciente'
        mensaje = 'Paciente Registrado Exitosamente'
        messagebox.showinfo(title, mensaje)
    except:
        title ='Registrar Paciente'
        mensaje ='Error al registrar paciente'
        messagebox.showinfo(title, mensaje)
