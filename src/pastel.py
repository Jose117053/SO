class Pastel:
    def __init__(self, nombre, color):
        self.nombre = nombre
        self.color = color

    def __str__(self):
        return f"{self.color}{self.nombre}\033[0m"  # Aplica el color y lo resetea al final