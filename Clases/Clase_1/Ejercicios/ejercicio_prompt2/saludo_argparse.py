import argparse

# Crear el parser
parser = argparse.ArgumentParser(description="Script de saludo")

# Agregar un argumento obligatorio
parser.add_argument("-n", "--nombre", required=True, help="Nombre de la persona a saludar")

# Parsear los argumentos
args = parser.parse_args()

# Usar el argumento
print(f"Hola, {args.nombre}!")
