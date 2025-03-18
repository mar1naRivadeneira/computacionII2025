import sys
import getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "n:", ["nombre="])
except getopt.GetoptError:
    print("Uso: python script.py -n <nombre> o --nombre <nombre>")
    sys.exit(1)

nombre = None
for opt, arg in opts:
    if opt in ("-n", "--nombre"):
        nombre = arg

if nombre:
    print(f"Hola, {nombre}!")
else:
    print("Uso: python script.py -n <nombre> o --nombre <nombre>")
