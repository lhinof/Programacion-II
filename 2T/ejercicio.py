import json

class mundo:
    def __init__(self, seed, nombre, player):
        self.seed = seed  
        self.nombre = nombre
        self.player = player 
        self.mob = []  

    def agregar_item(self, nuevo_item):
        success = self.player.agregar_item(nuevo_item)
        if success:
            print(f"Item agregado: {nuevo_item}. Total items: {len(self.player.item)}")
        else:
            print("No se pudo agregar item: (inventario lleno) maximo (36).")
        return success

    def eliminarmobh(self):
        original = list(self.mob)
        self.mob = [m for m in self.mob if not (getattr(m, "tipo", None) == "hostil" and getattr(m, "vida", None) == 100)]
        removed = [m for m in original if m not in self.mob]
        if removed:
            names = ", ".join(getattr(m, "nombre", "<sin nombre>") for m in removed)
            print(f"Mobs eliminados (hostiles con vida 100): {names}")
        else:
            print("No se eliminaron mobs (no hay hostiles con vida 100).")

    def guardar_mundo(self, filepath="backup.json"):
        data = {
            "seed": self.seed,
            "nombre": self.nombre,
            "player": {
                "nickname": self.player.nickname,
                "vida": self.player.vida,
                "item": [{"nombre": it.nombre, "tipo": it.tipo} for it in self.player.item],
            },
            "mob": [
                {"nombre": m.nombre, "tipo": m.tipo, "vida": m.vida, "generacion": m.generacion}
                for m in self.mob
            ],
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        pretty = json.dumps(data, ensure_ascii=False, indent=2)
        print(f"--- Guardando mundo en {filepath} ---")
        print(pretty)
        print(f"Mundo guardado en {filepath} (JSON mostrado arriba).")

    @classmethod
    def cargar_mundo(cls, filepath="backup.json"):
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"--- Cargando mundo desde {filepath} ---")
        print(json.dumps(data, ensure_ascii=False, indent=2))

        pdata = data.get("player", {})
        player = jugador(pdata.get("nickname"), pdata.get("vida", 0))
        for it in pdata.get("item", []):
            player.item.append(item(it.get("nombre"), it.get("tipo")))

        m = cls(data.get("seed"), data.get("nombre"), player)
        for md in data.get("mob", []):
            m.mob.append(mob(md.get("nombre"), md.get("tipo"), md.get("vida", 0), md.get("generacion")))
        print(f"Mundo '{m.nombre}' cargado. Jugador: {player.nickname} (vida {player.vida}). Mobs: {len(m.mob)}")
        return m

class jugador:
    def __init__(self, nickname, vida):
        self.nickname = nickname
        self.vida = vida 
        self.item = []  

    def agregar_item(self, nuevo_item):
        if len(self.item) >= 36:
            return False
        self.item.append(nuevo_item)
        return True

    def comer(self):
        for idx, it in enumerate(self.item):
            if it.tipo in ("comida", "food"):
                self.vida += 20
                nombre = it.nombre
                del self.item[idx]
                print(f"{self.nickname} comió '{nombre}'. Vida ahora: {self.vida}. Items restantes: {len(self.item)}")
                return True
        print(f"{self.nickname} no tiene comida en el inventario.")
        return False

class item:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

    def __repr__(self):
        return f"item(nombre={self.nombre!r}, tipo={self.tipo!r})"

class mob:
    def __init__(self, nombre, tipo, vida, generacion):
        self.nombre = nombre
        self.tipo = tipo
        self.vida = vida
        self.generacion = generacion
       

    def ataque_mob(self, jugador_obj):
        if hasattr(jugador_obj, "vida"):
            jugador_obj.vida = max(0, jugador_obj.vida - 10)
            jname = getattr(jugador_obj, "nickname", "<jugador>")
            print(f"{self.nombre} atacó a {jname}. Vida de {jname}: {jugador_obj.vida}")

def mostrar_estado(m):
    if not m:
        print("No hay mundo cargado.")
        return
    print("=== Estado del mundo ===")
    print(f"Seed: {m.seed}, Nombre: {m.nombre}")
    p = m.player
    print(f"Jugador: {p.nickname} (vida: {p.vida})")
    print(f"Items ({len(p.item)}): {[repr(it) for it in p.item]}")
    print(f"Mobs ({len(m.mob)}):")
    for i, mm in enumerate(m.mob):
        print(f"  [{i}] {mm.nombre} - tipo: {mm.tipo}, vida: {mm.vida}, gen: {mm.generacion}")
    print("========================")

def leer_int(prompt_text, default=None):
    try:
        val = input(prompt_text)
        if val.strip() == "" and default is not None:
            return default
        return int(val)
    except ValueError:
        print("Entrada inválida, se usará valor por defecto si aplica.")
        return default

def menu_principal():
    print("""
Menú:
1) Crear mundo nuevo
2) Cargar mundo (backup.json)
3) Guardar mundo (backup.json)
4) Agregar item al jugador
5) Comer (usar comida del inventario)
6) Spawnear mob
7) Hacer que un mob ataque al jugador
8) Eliminar hostiles con vida 100
9) Mostrar estado del mundo
0) Salir
""")

def main():
    mundo_act = None
    while True:
        menu_principal()
        opc = input("Elija una opción: ").strip()
        if opc == "1":
            seed = leer_int("Seed (número): ", default=0)
            nombre = input("Nombre del mundo: ").strip() or "mundo"
            nick = input("Nickname del jugador: ").strip() or "player"
            vida = leer_int("Vida inicial del jugador: ", default=100)
            player = jugador(nick, vida)
            mundo_act = mundo(seed, nombre, player)
            print(f"Mundo '{nombre}' creado con jugador '{nick}'.")
        elif opc == "2":
            try:
                mundo_act = mundo.cargar_mundo("backup.json")
            except Exception as e:
                print(f"Error cargando mundo: {e}")
        elif opc == "3":
            if mundo_act:
                mundo_act.guardar_mundo("backup.json")
            else:
                print("No hay mundo para guardar.")
        elif opc == "4":
            if not mundo_act:
                print("Cree o cargue un mundo primero.")
                continue
            in_nombre = input("Nombre del item: ").strip() or "item"
            in_tipo = input("Tipo del item (ej: comida, arma, misc): ").strip() or "misc"
            it = item(in_nombre, in_tipo)
            mundo_act.agregar_item(it)
        elif opc == "5":
            if not mundo_act:
                print("Cree o cargue un mundo primero.")
                continue
            mundo_act.player.comer()
        elif opc == "6":
            if not mundo_act:
                print("Cree o cargue un mundo primero.")
                continue
            mn = input("Nombre del mob: ").strip() or "mob"
            mt = input("Tipo del mob (hostil/neutral): ").strip() or "hostil"
            mv = leer_int("Vida del mob: ", default=100)
            mg = leer_int("Generacion del mob: ", default=1)
            mm = mob(mn, mt, mv, mg)
            mundo_act.mob.append(mm)
            print(f"Mob '{mn}' agregado.")
        elif opc == "7":
            if not mundo_act or not mundo_act.mob:
                print("No hay mobs para atacar.")
                continue
            mostrar_estado(mundo_act)
            idx = leer_int("Índice del mob que atacará (número): ", default=0)
            if idx is None or idx < 0 or idx >= len(mundo_act.mob):
                print("Índice inválido.")
                continue
            mundo_act.mob[idx].ataque_mob(mundo_act.player)
        elif opc == "8":
            if not mundo_act:
                print("Cree o cargue un mundo primero.")
                continue
            mundo_act.eliminarmobh()
        elif opc == "9":
            mostrar_estado(mundo_act)
        elif opc == "0":
            print("Saliendo.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()