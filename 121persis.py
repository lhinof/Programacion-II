import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.libros = []
        self.autores = []
        self.prestamos = []
        self.horario = None

    def agregar_libro(self, libro):
        self.libros.append(libro)

    def agregar_autor(self, autor):
        self.autores.append(autor)

    def agregar_prestamo(self, prestamo):
        self.prestamos.append(prestamo)

    def establecer_horario(self, horario):
        self.horario = horario

    def prestar_libro(self, estudiante, libro, fecha_devolucion):
        fecha_prestamo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prestamo = Prestamo(estudiante, libro, fecha_prestamo, fecha_devolucion)
        self.agregar_prestamo(prestamo)

    def mostrar_estado(self):
        estado = f"Biblioteca: {self.nombre}\n"
        estado += f"Libros disponibles: {len(self.libros)}\n"
        estado += f"Autores registrados: {len(self.autores)}\n"
        estado += f"Prestamos activos: {len(self.prestamos)}\n"
        if self.horario:
            estado += f"Horario: {self.horario.mostrar()}\n"
        return estado

    def cerrar(self):
        self.prestamos = []
        return "La biblioteca está cerrada y los préstamos han sido eliminados."

class Pagina:
    def __init__(self, numero, contenido):
        self.numero = numero
        self.contenido = contenido
    
    def mostrar(self):
        return f"Página {self.numero}: {self.contenido}"

class Horario:
    def __init__(self, dias_apertura, hora_apertura, hora_cierre):
        self.dias_apertura = dias_apertura
        self.hora_apertura = hora_apertura
        self.hora_cierre = hora_cierre

    def mostrar(self):
        return f"Horario: {self.dias_apertura} de {self.hora_apertura} a {self.hora_cierre}"

class Autor:
    def __init__(self, nombre, nacionalidad):
        self.nombre = nombre
        self.nacionalidad = nacionalidad

    def mostrar_info(self):
        return f"Autor: {self.nombre}, Nacionalidad: {self.nacionalidad}"

class Libro:
    def __init__(self, titulo, isbn):
        self.titulo = titulo
        self.isbn = isbn
        self.paginas = []

    def agregar_pagina(self, pagina):
        self.paginas.append(pagina)
    
    def leer(self):
        return "\n".join([pagina.mostrar() for pagina in self.paginas])

class Estudiante:
    def __init__(self, codigo, nombre):
        self.codigo = codigo
        self.nombre = nombre

    def mostrar_info(self):
        return f"Estudiante: {self.nombre}, Código: {self.codigo}"

class Prestamo:
    def __init__(self, estudiante, libro, fecha_prestamo, fecha_devolucion):
        self.estudiante = estudiante
        self.libro = libro
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion

    def mostrar_info(self):
        return (f"Prestamo:\n Estudiante: {self.estudiante.mostrar_info()}\n"
                f" Libro: {self.libro.titulo}\n Fecha de préstamo: {self.fecha_prestamo}\n"
                f" Fecha de devolución: {self.fecha_devolucion}")

class BibliotecaApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Biblioteca Universitaria")
        self.biblioteca = Biblioteca("Biblioteca UMSA")

        self.frame_libros = tk.LabelFrame(self.master, text="Libros", padx=10, pady=10)
        self.frame_libros.pack(padx=10, pady=10)

        self.lbl_titulo = tk.Label(self.frame_libros, text="Título del libro:")
        self.lbl_titulo.grid(row=0, column=0)
        self.ent_titulo = tk.Entry(self.frame_libros)
        self.ent_titulo.grid(row=0, column=1)

        self.lbl_isbn = tk.Label(self.frame_libros, text="ISBN:")
        self.lbl_isbn.grid(row=1, column=0)
        self.ent_isbn = tk.Entry(self.frame_libros)
        self.ent_isbn.grid(row=1, column=1)

        self.btn_agregar_libro = tk.Button(self.frame_libros, text="Agregar Libro", command=self.agregar_libro)
        self.btn_agregar_libro.grid(row=2, column=0, columnspan=2)

        self.listbox_libros = tk.Listbox(self.master, height=6, width=50)
        self.listbox_libros.pack(pady=10)

        
        self.btn_mostrar_estado = tk.Button(self.master, text="Mostrar Estado de la Biblioteca", command=self.mostrar_estado)
        self.btn_mostrar_estado.pack(pady=10)

    def agregar_libro(self):
        titulo = self.ent_titulo.get()
        isbn = self.ent_isbn.get()
        if titulo and isbn:
            libro = Libro(titulo, isbn)
            self.biblioteca.agregar_libro(libro)
            self.listbox_libros.insert(tk.END, f"{titulo} (ISBN: {isbn})")
            self.ent_titulo.delete(0, tk.END)
            self.ent_isbn.delete(0, tk.END)
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, complete todos los campos.")

    def mostrar_estado(self):
        estado = self.biblioteca.mostrar_estado()
        messagebox.showinfo("Estado de la Biblioteca", estado)

def run_app():
    root = tk.Tk()
    app = BibliotecaApp(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
