import threading
import time
import random
import sys
from buffer import Buffer

class Consumidor(threading.Thread):
    def __init__(self, buffer, id):
        super().__init__()
        self.buffer = buffer
        self.id = id

    def run(self):
        while True:
            self.buffer.consumir(self.id)

            # Espera un tiempo aleatorio entre 0 y 5 segundos
            tiempo_espera = random.uniform(0, 5)
            time.sleep(tiempo_espera)

if __name__ == "__main__":
    # Verificar si se proporciona un argumento
    if len(sys.argv) != 2:
        print("Uso: python consumidor.py <num_consumidores>")
        sys.exit(1)

    # Obtener el número de consumidores desde el argumento
    try:
        num_consumidores = int(sys.argv[1])
    except ValueError:
        print("El número de consumidores debe ser un entero.")
        sys.exit(1)

    buffer = Buffer()
    consumidores = [Consumidor(buffer, i) for i in range(num_consumidores)]

    # Iniciar los consumidores
    for c in consumidores:
        c.start()