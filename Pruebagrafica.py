import tkinter as tk
from tkinter import ttk, messagebox
import random

class Persona:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol

class Computadora:
    def __init__(self, procesador, ram, disco_duro, tarjeta_grafica=False):
        self.id = f"PC-{random.randint(100, 999)}"
        self.procesador = procesador
        self.ram = f"{ram}GB"
        self.disco_duro = f"{disco_duro}GB"
        self.tarjeta_grafica = tarjeta_grafica
        self.estado = "operativa"
    def ejecutar_diagnostico(self):
        return f"Diagnóstico de {self.id}: OK. Estado: {self.estado}"
    def poner_en_mantenimiento(self):
        self.estado = "Mantenimiento"
    def volver_a_operacion(self):
        self.estado = "Operatíva"

class Mesa:
    def __init__(self, capacidad_alumnos):
        self.id = f"Mesa-{random.randint(1, 100)}"
        self.capacidad_alumnos = min(6, max(4, capacidad_alumnos))
        self.sillas = self.capacidad_alumnos
        self.estado = "Disponible"

class Laboratorio:
    def __init__(self, nombre, personal_asignado):
        self.nombre = nombre
        self.internet = True
        self.computadoras = []
        self.mesas = []
        self.personal_asignado = personal_asignado
    def capacidad_total(self):
        capacidad_pc = len([pc for pc in self.computadoras if pc.estado == "Operativa"])
        capacidad_mesas = sum(mesa.capacidad_alumnos for mesa in self.mesas if mesa.estado == "Disponible")
        return capacidad_pc + capacidad_mesas
    def activar_modo_examen(self):
        self.internet = False
    def activar_modo_clase(self):
        self.internet = True
    def add_computadora(self, pc):
        self.computadoras.append(pc)
    def add_mesa(self, mesa):
        self.mesas.append(mesa)

personal_lab = [Persona("Lic, Felipez", "Docente"), Persona("Aux. Tarqui Joel", "Auxiliar")]

lasin1 = Laboratorio("Lasin 1", personal_lab)
lasin1.add_computadora(Computadora("Core i7", 16, 512, True))
lasin1.add_computadora(Computadora("Core i5", 8, 256, False))
lasin1.computadoras[1].estado = "Mantenimiento"
lasin1.add_mesa(Mesa(4))
lasin1.add_mesa(Mesa(6))

lasin2 = Laboratorio("Lasin 2", [Persona("Lic. Tapia", "Docente")])
for _ in range(3):
    lasin2.add_computadora(Computadora("Ryzen 5", 16, 512, True))
lasin2.add_mesa(Mesa(4))
lasin2.add_mesa(Mesa(4))
lasin2.mesas[1].estado = "Mantenimiento"

class Aplicacion:
    def __init__(self, master, laboratorios):
        self.master = master
        self.laboratorios = laboratorios
        master.title("Sistema de Gestión de Laboratorios - LaSin")
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(pady=10, padx=10, expand=True, fill="both")
        self.frames = {}
        self.lab_labels = {}
        for lab in self.laboratorios:
            frame = ttk.Frame(self.notebook, padding="10")
            self.notebook.add(frame, text=lab.nombre)
            self.frames[lab.nombre] = frame
            self.crear_interfaz_laboratorio(frame, lab)

    def crear_interfaz_laboratorio(self, frame, lab):
        attr_frame = ttk.LabelFrame(frame, text="Atributos Generales", padding="10")
        attr_frame.pack(fill="x", pady=5)

        labels = {}
        labels["nombre"] = ttk.Label(attr_frame, text=f"Nombre: {lab.nombre}")
        labels["nombre"].grid(row=0, column=0, sticky="w", padx=5, pady=2)

        labels["internet"] = ttk.Label(attr_frame, text="Internet: " + ("Activo" if lab.internet else "Inactivo"))
        labels["internet"].grid(row=1, column=0, sticky="w", padx=5, pady=2)

        labels["capacidad"] = ttk.Label(attr_frame, text=f"Capacidad Total: {lab.capacidad_total()} alumnos")
        labels["capacidad"].grid(row=2, column=0, sticky="w", padx=5, pady=2)

        personal_nombres = ", ".join([p.nombre for p in lab.personal_asignado])
        ttk.Label(attr_frame, text=f"Personal Asignado: {personal_nombres}").grid(row=3, column=0, sticky="w", padx=5, pady=2)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(btn_frame, text="Activar Modo Examen (OFF)", command=lambda: self.cambiar_modo_internet(lab, False)).pack(side="left", padx=5, pady=5, expand=True, fill="x")
        ttk.Button(btn_frame, text="Activar Modo Clase (ON)", command=lambda: self.cambiar_modo_internet(lab, True)).pack(side="left", padx=5, pady=5, expand=True, fill="x")

        ttk.Button(frame, text="Gestión de Componentes (CRUD)", command=lambda: self.abrir_ventana_crud(lab)).pack(fill="x", pady=10)

        pc_frame = ttk.LabelFrame(frame, text="Computadoras (Composición)", padding="10")
        pc_frame.pack(fill="both", expand=True, pady=5)
        labels["pc_list"] = ttk.Label(pc_frame, text="")
        labels["pc_list"].pack(fill="both", expand=True)

        mesa_frame = ttk.LabelFrame(frame, text="Mesas (Composición)", padding="10")
        mesa_frame.pack(fill="both", expand=True, pady=5)
        labels["mesa_list"] = ttk.Label(mesa_frame, text="")
        labels["mesa_list"].pack(fill="both", expand=True)

        self.lab_labels[lab.nombre] = labels
        self.actualizar_vista(lab)

    def cambiar_modo_internet(self, lab, estado):
        if estado:
            lab.activar_modo_clase()
            messagebox.showinfo("Modo Internet", f"Internet Activado en {lab.nombre} (Modo Clase).")
        else:
            lab.activar_modo_examen()
            messagebox.showwarning("Modo Internet", f"Internet Desactivado en {lab.nombre} (Modo Examen).")
        self.actualizar_vista(lab)

    def actualizar_vista(self, lab):
        labels = self.lab_labels[lab.nombre]
        internet_text = "Activo" if lab.internet else "Inactivo"
        labels["internet"].config(text=f"Internet: {internet_text}")
        labels["capacidad"].config(text=f"Capacidad Total: {lab.capacidad_total()} alumnos")

        pc_list_text = "ID | Procesador | RAM | GPU | Estado\n" + "="*40 + "\n"
        for pc in lab.computadoras:
            gpu = "Sí" if pc.tarjeta_grafica else "No"
            pc_list_text += f"{pc.id} | {pc.procesador} | {pc.ram} | {gpu} | {pc.estado}\n"
        labels["pc_list"].config(text=pc_list_text, justify=tk.LEFT)

        mesa_list_text = "ID | Capacidad | Sillas | Estado\n" + "="*30 + "\n"
        for mesa in lab.mesas:
            mesa_list_text += f"{mesa.id} | {mesa.capacidad_alumnos} alumnos | {mesa.sillas} | {mesa.estado}\n"
        labels["mesa_list"].config(text=mesa_list_text, justify=tk.LEFT)

    def abrir_ventana_crud(self, lab):
        crud_win = tk.Toplevel(self.master)
        crud_win.title(f"CRUD de Componentes - {lab.nombre}")
        crud_win.geometry("600x600")
        notebook_crud = ttk.Notebook(crud_win)
        notebook_crud.pack(pady=10, padx=10, expand=True, fill="both")

        frame_add = ttk.Frame(notebook_crud, padding="10")
        notebook_crud.add(frame_add, text="Añadir Componente")
        self.crear_pestana_añadir(frame_add, lab, crud_win)

        frame_manage = ttk.Frame(notebook_crud, padding="10")
        notebook_crud.add(frame_manage, text="Eliminar / Mantenimiento")
        self.crear_pestana_gestionar(frame_manage, lab, crud_win)

    def crear_pestana_añadir(self, frame, lab, crud_win):
        pc_frame = ttk.LabelFrame(frame, text="Añadir Computadora", padding="10")
        pc_frame.pack(fill="x", pady=10)

        entries_pc = {}
        for i, (label, default) in enumerate([("Procesador:", "i7"), ("RAM (GB):", "16"), ("Disco Duro (GB):", "512")]):
            ttk.Label(pc_frame, text=label).grid(row=i, column=0, sticky="w", padx=5, pady=2)
            entries_pc[label] = ttk.Entry(pc_frame)
            entries_pc[label].insert(0, default)
            entries_pc[label].grid(row=i, column=1, sticky="ew", padx=5, pady=2)

        var_gpu = tk.BooleanVar(value=True)
        ttk.Checkbutton(pc_frame, text="Tarjeta Gráfica", variable=var_gpu).grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        def agregar_pc():
            try:
                nueva_pc = Computadora(
                    entries_pc["Procesador:"].get(),
                    int(entries_pc["RAM (GB):"].get()),
                    int(entries_pc["Disco Duro (GB):"].get()),
                    var_gpu.get()
                )
                lab.add_computadora(nueva_pc)
                messagebox.showinfo("Éxito", f"Computadora {nueva_pc.id} añadida a {lab.nombre}.")
                self.actualizar_vista(lab)
                crud_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "RAM y Disco Duro deben ser números enteros.")

        ttk.Button(pc_frame, text="Añadir PC", command=agregar_pc).grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

        mesa_frame = ttk.LabelFrame(frame, text="Añadir Mesa", padding="10")
        mesa_frame.pack(fill="x", pady=10)

        ttk.Label(mesa_frame, text="Capacidad:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        capacidad_mesa_entry = ttk.Entry(mesa_frame)
        capacidad_mesa_entry.insert(0, "4")
        capacidad_mesa_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        def agregar_mesa():
            try:
                capacidad = int(capacidad_mesa_entry.get())
                nueva_mesa = Mesa(capacidad)
                lab.add_mesa(nueva_mesa)
                messagebox.showinfo("Éxito", f"Mesa {nueva_mesa.id} (Cap: {capacidad}) añadida a {lab.nombre}.")
                self.actualizar_vista(lab)
                crud_win.destroy()
            except ValueError:
                messagebox.showerror("Error", "Capacidad debe ser un número entero.")

        ttk.Button(mesa_frame, text="Añadir Mesa", command=agregar_mesa).grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=10)

    def crear_pestana_gestionar(self, frame, lab, crud_win):
        pc_options = [f"{pc.id} ({pc.estado})" for pc in lab.computadoras]
        pc_selected = tk.StringVar()
        ttk.Label(frame, text="Seleccionar Computadora:").pack(pady=5)
        pc_combo = ttk.Combobox(frame, textvariable=pc_selected, values=pc_options, state="readonly")
        pc_combo.pack(fill="x", padx=10)

        def gestionar_pc(accion):
            if not pc_selected.get():
                messagebox.showwarning("Advertencia", "Selecciona una computadora.")
                return
            pc_id = pc_selected.get().split(" ")[0]
            pc_obj = next((pc for pc in lab.computadoras if pc.id == pc_id), None)
            if not pc_obj: return
            if accion == "mantenimiento":
                pc_obj.poner_en_mantenimiento()
                messagebox.showinfo("Estado", f"PC {pc_id} puesta en Mantenimiento.")
            elif accion == "operativa":
                pc_obj.volver_a_operacion()
                messagebox.showinfo("Estado", f"PC {pc_id} marcada como Operativa.")
            elif accion == "eliminar":
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de ELIMINAR permanentemente la PC {pc_id}?"):
                    lab.computadoras.remove(pc_obj)
                    messagebox.showinfo("Éxito", f"PC {pc_id} eliminada.")
            self.actualizar_vista(lab)
            crud_win.destroy()

        btn_frame_pc = ttk.Frame(frame)
        btn_frame_pc.pack(fill="x", pady=5)
        ttk.Button(btn_frame_pc, text="Mantenimiento", command=lambda: gestionar_pc("mantenimiento")).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame_pc, text="Operativa", command=lambda: gestionar_pc("operativa")).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame_pc, text="Eliminar", command=lambda: gestionar_pc("eliminar")).pack(side="left", expand=True, padx=5)

        ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=20)

        mesa_options = [f"{m.id} ({m.estado})" for m in lab.mesas]
        mesa_selected = tk.StringVar()
        ttk.Label(frame, text="Seleccionar Mesa:").pack(pady=5)
        mesa_combo = ttk.Combobox(frame, textvariable=mesa_selected, values=mesa_options, state="readonly")
        mesa_combo.pack(fill="x", padx=10)

        def gestionar_mesa(accion):
            if not mesa_selected.get():
                messagebox.showwarning("Advertencia", "Selecciona una mesa.")
                return
            mesa_id = mesa_selected.get().split(" ")[0]
            mesa_obj = next((m for m in lab.mesas if m.id == mesa_id), None)
            if not mesa_obj: return
            if accion == "mantenimiento":
                mesa_obj.estado = "Mantenimiento"
                messagebox.showinfo("Estado", f"Mesa {mesa_id} puesta en Mantenimiento.")
            elif accion == "disponible":
                mesa_obj.estado = "Disponible"
                messagebox.showinfo("Estado", f"Mesa {mesa_id} marcada como Disponible.")
            elif accion == "eliminar":
                if messagebox.askyesno("Confirmar", f"¿Estás seguro de ELIMINAR permanentemente la Mesa {mesa_id}?"):
                    lab.mesas.remove(mesa_obj)
                    messagebox.showinfo("Éxito", f"Mesa {mesa_id} eliminada.")
            self.actualizar_vista(lab)
            crud_win.destroy()

        btn_frame_mesa = ttk.Frame(frame)
        btn_frame_mesa.pack(fill="x", pady=5)
        ttk.Button(btn_frame_mesa, text="Mantenimiento", command=lambda: gestionar_mesa("mantenimiento")).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame_mesa, text="Disponible", command=lambda: gestionar_mesa("disponible")).pack(side="left", expand=True, padx=5)
        ttk.Button(btn_frame_mesa, text="Eliminar", command=lambda: gestionar_mesa("eliminar")).pack(side="left", expand=True, padx=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root, [lasin1, lasin2])
    root.mainloop()