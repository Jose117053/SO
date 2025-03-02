import threading
import random
import os
import time
from pastel import Pastel

# Archivos compartidos
PASTELES_FILE = "pasteles.txt"
CONTADOR_FILE = "contador.txt"
SEMAFOROS_FILE = "semaforos.txt"

# Lista de tipos de pasteles
PASTELES = [
    "3 Leches", "Cheesecake", "Chocolate", "Nuez", "Moka",
    "Fresa", "Vainilla", "Zanahoria", "Limón", "Coco",
    "Red Velvet", "Tiramisú", "Opera", "Tarta de Manzana", "Tarta de Pera",
    "Tarta de Frutas", "Tarta de Queso", "Tarta de Calabaza", "Tarta de Plátano", "Tarta de Durazno"]
BUFFER_SIZE = 30  # Tamaño máximo del buffer (maximo de lineas en pasteles.txt)

# Colores ANSI para los pasteleros
COLORES = [
    "\033[31m",  # Rojo
    "\033[32m",  # Verde
    "\033[33m",  # Amarillo
    "\033[34m",  # Azul
    "\033[35m",  # Magenta
    "\033[36m",  # Cyan
    "\033[91m",  # Rojo claro
    "\033[92m",  # Verde claro
    "\033[93m",  # Amarillo claro
    "\033[94m",  # Azul claro
    "\033[95m",  # Magenta claro
    "\033[96m",  # Cyan claro
]

class Buffer:
    def __init__(self):
        self.mutex = threading.Lock()  # Control de acceso al archivo de pasteles y semáforos
        self.initialize_files()

    def initialize_files(self):
        """Crea archivos si no existen y los inicializa con valores predeterminados."""
        with self.mutex:
            if not os.path.exists(PASTELES_FILE):
                open(PASTELES_FILE, "w").close()
            if not os.path.exists(CONTADOR_FILE):
                with open(CONTADOR_FILE, "w") as f:
                    f.write("0\n")
            if not os.path.exists(SEMAFOROS_FILE) or os.path.getsize(SEMAFOROS_FILE) == 0:
                with open(SEMAFOROS_FILE, "w") as f:
                    f.write(f"{BUFFER_SIZE} 0\n")  # Inicializar semáforos: empty=BUFFER_SIZE, full=0

    def leer_contador(self):
        """Lee el número de pasteles en el buffer."""
        with open(CONTADOR_FILE, "r") as f:
            return int(f.readline().strip())

    def actualizar_contador(self, valor):
        """Actualiza el contador de pasteles."""
        with open(CONTADOR_FILE, "w") as f:
            f.write(f"{valor}\n")

    def leer_semaforos(self):
        """Lee los valores de empty y full desde el archivo."""
        try:
            with open(SEMAFOROS_FILE, "r") as f:
                line = f.readline().strip()
                if line:
                    empty, full = map(int, line.split())
                    return empty, full
                else:
                    # Si el archivo está vacío, reinicializar
                    self.initialize_files()
                    return BUFFER_SIZE, 0
        except (ValueError, FileNotFoundError):
            # Si hay un error, reinicializar, esto en teoria no debe pasar.
            self.initialize_files()
            return BUFFER_SIZE, 0

    def actualizar_semaforos(self, empty, full):
        """Actualiza los valores de empty y full en el archivo semaforos.txt."""
        with open(SEMAFOROS_FILE, "w") as f:
            f.write(f"{empty} {full}\n")

    def producir(self, id):
        """Produce un pastel y lo almacena en el archivo pasteles.txt."""
        while True:
            with self.mutex:
                empty, full = self.leer_semaforos()
                if empty > 0:
                    break
            time.sleep(0.1)  # Pequeña espera para verificar si el buffer sigue lleno (mutex)

        with self.mutex: 
            tipo_pastel = random.choice(PASTELES)
            color = COLORES[id % len(COLORES)] 
            pastel = Pastel(tipo_pastel, color)

            # Escribir en archivo de pasteles
            with open(PASTELES_FILE, "a") as f:
                f.write(f"{pastel.nombre},{pastel.color}\n")

            # Actualizar contador
            pasteles = self.leer_contador() + 1
            self.actualizar_contador(pasteles)

            # Actualizar semáforos
            self.actualizar_semaforos(empty - 1, full + 1)

            print(f"{color}El pastelero {id} ha producido un pastel de {pastel.nombre} (Total: {pasteles})\033[0m")

    def consumir(self, id):
        """Consume un pastel eliminándolo del archivo."""
        while True:
            with self.mutex: 
                empty, full = self.leer_semaforos()
                if full > 0:
                    break
            time.sleep(0.1) 

        with self.mutex:
            pastel_consumido = None
            pasteles = []

            # Leer y eliminar el primer pastel
            with open(PASTELES_FILE, "r") as f:
                pasteles = f.readlines()

            if pasteles:
                nombre, color = pasteles.pop(0).strip().split(",")
                pastel_consumido = Pastel(nombre, color)

                # Escribir nuevamente el archivo sin el pastel consumido
                with open(PASTELES_FILE, "w") as f:
                    f.writelines(pasteles)

                pasteles_actualizados = max(self.leer_contador() - 1, 0)
                self.actualizar_contador(pasteles_actualizados)
                self.actualizar_semaforos(empty + 1, full - 1)

                print(f"{pastel_consumido.color}El consumidor {id} ha consumido un pastel de {pastel_consumido} (Quedan: {pasteles_actualizados})\033[0m")