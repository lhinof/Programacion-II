import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Cancion:
    def __init__(self, nombre, duracion, artista):
        self.nombre = nombre
        self.duracion = duracion
        self.artista = artista

class Artista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []
        self.seguidores = 0

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)

    def obtener_estadisticas(self):
        return f"{self.nombre} - Canciones: {len(self.canciones)}, Seguidores: {self.seguidores}"

class Usuario:
    def __init__(self, nombre, premium=False):
        self.nombre = nombre
        self.premium = premium
        self.estadisticas = {'canciones_reproducidas': 0, 'seguimiento_artistas': {}}

    def reproducir_cancion(self, cancion):
        self.estadisticas['canciones_reproducidas'] += 1
        artista = cancion.artista.nombre
        self.estadisticas['seguimiento_artistas'][artista] = \
            self.estadisticas['seguimiento_artistas'].get(artista, 0) + 1
        cancion.artista.seguidores += 1

    def obtener_estadisticas(self):
        return f"{self.nombre} - Reproducciones: {self.estadisticas['canciones_reproducidas']}"

class Spotify:
    def __init__(self):
        self.usuarios = []
        self.artistas = []

    def registrar_usuario(self, nombre, premium=False):
        u = Usuario(nombre, premium)
        self.usuarios.append(u)
        return u

    def registrar_artista(self, nombre):
        a = Artista(nombre)
        self.artistas.append(a)
        return a

def mostrar_estadisticas():
    text.delete("1.0", tk.END)
    text.insert(tk.END, "=== Usuarios ===\n")
    for u in spotify.usuarios:
        text.insert(tk.END, u.obtener_estadisticas() + "\n")

    text.insert(tk.END, "\n=== Artistas ===\n")
    for a in spotify.artistas:
        text.insert(tk.END, a.obtener_estadisticas() + "\n")

def graficar_reproducciones():
    nombres = []
    valores = []

    for artista in spotify.artistas:
        total = 0
    
        for u in spotify.usuarios:
            total += u.estadisticas['seguimiento_artistas'].get(artista.nombre, 0)
        nombres.append(artista.nombre)
        valores.append(total)

    fig, ax = plt.subplots()
    ax.bar(nombres, valores)
    ax.set_ylabel("Reproducciones")
    ax.set_title("Reproducciones por Artista")

    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.get_tk_widget().pack()

spotify = Spotify()

u1 = spotify.registrar_usuario("Carlos", True)
u2 = spotify.registrar_usuario("Ana")

a1 = spotify.registrar_artista("Shakira")
a2 = spotify.registrar_artista("Bad Bunny")

c1 = Cancion("Hips Don't Lie", 3.35, a1)
c2 = Cancion("La Canción", 4.05, a2)

a1.agregar_cancion(c1)
a2.agregar_cancion(c2)

u1.reproducir_cancion(c1)
u2.reproducir_cancion(c2)
u1.reproducir_cancion(c2)

ventana = tk.Tk()
ventana.title("Estadísticas Spotify")

tk.Button(ventana, text="Mostrar estadísticas", command=mostrar_estadisticas).pack()
tk.Button(ventana, text="Gráfico de reproducciones", command=graficar_reproducciones).pack()

text = tk.Text(ventana, height=15, width=60)
text.pack()

ventana.mainloop()
