# CLASE PERSONA
# tenemos la siguiente clase persona que es agrgacion de la clase cabina con los siguientes atributos : nombre :String, edad:int , pesodepersona:float y los siguientes metodos publicos: +persona (nombre, edad,peso)
class Persona:
    def __init__(self, nombre: str, edad: int, peso: float):
        self.nombre = nombre
        self.edad = edad
        self.peso = peso
    
    def __str__(self):
        return f"Persona(nombre={self.nombre}, edad={self.edad}, peso={self.peso})"


# CLASE CABINA
# tenemos la clase cabina que es composicion de la clase linea con los siguientes atributos : nro de cabina : int , personasAbordo: persona que es aguegacion [] y los siguientes metodos publicos : +cabina (nrocabina), + agregarpersona (persona p)
class Cabina:
    def __init__(self, nroCabina: int):
        self.nroCabina = nroCabina
        self.personasAbordo = []
    
    def agregar_persona(self, persona: Persona):
        self.personasAbordo.append(persona)
    
    def __str__(self):
        personas = ', '.join(str(p) for p in self.personasAbordo)
        return f"Cabina(nroCabina={self.nroCabina}, personasAbordo=[{personas}])"


# CLASE LINEA
# tenemos la siguiente clase Linea que es composicion de la clase miteleferico con atributos color :String, FilaPersonas: Clase persona que es aguegacion [] y por ultimo cantidfad de cabinas que es un int...
class Linea:
    def __init__(self, color: str):
        self.color = color
        self.filaPersonas = []  
        self.cabinas = []
    
    def agregar_persona(self, persona: Persona):
        self.filaPersonas.append(persona)
    
    def agregar_cabina(self, nroCabina: int):
        cabina = Cabina(nroCabina)
        self.cabinas.append(cabina)
    
    def __str__(self):
        personas = ', '.join(str(p) for p in self.filaPersonas)
        cabinas = ', '.join(str(c) for c in self.cabinas)
        return f"Linea(color={self.color}, filaPersonas=[{personas}], cabinas=[{cabinas}])"


# CLASE MI TELEFÉRICO
#tenemos cuatro clases MiTeleferico atributos: composiscion clase Linea [] cantidad dingresos:que es un float...
class MiTeleferico:
    def __init__(self):
        self.lineas = []  
        self.cantidadDeIngresos = 0.0  
    
    def agregar_linea(self, linea: Linea):
        self.lineas.append(linea)

    def buscar_linea(self, color: str):
        for linea in self.lineas:
            if linea.color == color:
                return linea
        return None
    
    def agregar_persona_fila(self, persona: Persona, linea_color: str):
        linea = self.buscar_linea(linea_color)
        if linea:
            linea.agregar_persona(persona)
    
    def agregar_cabina(self, linea_color: str, nroCabina: int):
        linea = self.buscar_linea(linea_color)
        if linea:
            linea.agregar_cabina(nroCabina)

    # a)
    def agregar_primera_persona_a_cabina(self, linea_color: str, nroCabina: int):
        linea = self.buscar_linea(linea_color)
        if not linea:
            return
        
        if len(linea.filaPersonas) == 0:
            return
        
        cabina_obj = None
        for c in linea.cabinas:
            if c.nroCabina == nroCabina:
                cabina_obj = c
                break
        
        if not cabina_obj:
            return
        
        if len(cabina_obj.personasAbordo) >= 10:
            return
        
        peso_actual = sum(p.peso for p in cabina_obj.personasAbordo)
        if peso_actual + linea.filaPersonas[0].peso > 850:
            return
        
        persona = linea.filaPersonas.pop(0)
        cabina_obj.agregar_persona(persona)

    # b)
    def verificar_cabinas(self):
        for linea in self.lineas:
            for cabina in linea.cabinas:
                if len(cabina.personasAbordo) > 10:
                    print(f"Cabina {cabina.nroCabina} excede el límite de personas")
                
                peso = sum(p.peso for p in cabina.personasAbordo)
                if peso > 850:
                    print(f"Cabina {cabina.nroCabina} excede el peso máximo")

    # c)
    def calcular_ingresos(self):
        total = 0
        for linea in self.lineas:
            for cabina in linea.cabinas:
                for p in cabina.personasAbordo:
                    if p.edad <= 25 or p.edad >= 70:
                        total += 1.5
                    else:
                        total += 3

        self.cantidadDeIngresos = total
        return total

    # d)
    def linea_con_mas_ingresos(self):
        max_ingreso = -1
        linea_max = None

        for linea in self.lineas:
            ingreso_linea = 0
            for cabina in linea.cabinas:
                for p in cabina.personasAbordo:
                    if not (p.edad <= 25 or p.edad >= 70):
                        ingreso_linea += 3

            if ingreso_linea > max_ingreso:
                max_ingreso = ingreso_linea
                linea_max = linea
        
        return linea_max

    def __str__(self):
        lineas = ', '.join(str(l) for l in self.lineas)
        return f"MiTeleferico(lineas=[{lineas}], cantidadDeIngresos={self.cantidadDeIngresos})"


# MAIN
if __name__ == "__main__":
    persona1 = Persona("Jhonny Felipez", 30, 75.5)
    persona2 = Persona("Ana", 25, 60.0)

    mi_teleferico = MiTeleferico()

    linea_roja = Linea("Roja")
    linea_amarilla = Linea("Amarilla")

    mi_teleferico.agregar_linea(linea_roja)
    mi_teleferico.agregar_linea(linea_amarilla)

    mi_teleferico.agregar_persona_fila(persona1, "Roja")
    mi_teleferico.agregar_persona_fila(persona2, "Amarilla")

    mi_teleferico.agregar_cabina("Roja", 101)
    mi_teleferico.agregar_cabina("Amarilla", 102)

    mi_teleferico.agregar_primera_persona_a_cabina("Roja", 101)
    mi_teleferico.agregar_primera_persona_a_cabina("Amarilla", 102)

    total = mi_teleferico.calcular_ingresos()
    print("Ingresos Totales:", total)

    linea_max = mi_teleferico.linea_con_mas_ingresos()
    print("Línea con más ingresos (solo regular):", linea_max.color if linea_max else "Ninguna")

    print("\nEstado Final:")
    print(mi_teleferico)
