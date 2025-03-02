import threading
import time
import random
import sys
from buffer import Buffer

class Productor(threading.Thread):
    def __init__(self, buffer, id):
        super().__init__()
        self.buffer = buffer
        self.id = id

    def run(self):
        while True:
            self.buffer.producir(self.id)

            # Espera un tiempo aleatorio entre 0 y 5 segundos
            tiempo_espera = random.uniform(0, 5)
            time.sleep(tiempo_espera)

if __name__ == "__main__":
    # Verificar si se proporciona un argumento
    if len(sys.argv) != 2:
        print("Uso: python productor.py <num_productores>")
        sys.exit(1)

    # Obtener el número de productores desde el argumento
    try:
        num_productores = int(sys.argv[1])
    except ValueError:
        print("El número de productores debe ser un entero.")
        sys.exit(1)

    buffer = Buffer()
    productores = [Productor(buffer, i) for i in range(num_productores)]

    # Iniciar los productores
    for p in productores:
        p.start()