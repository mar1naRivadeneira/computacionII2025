import argparse

parser = argparse.ArgumentParser(description= "script convertidor de archivos")

#agregado de archivos obligatorios : nombre del archivo de entrada y el nombre del archivo de salida
parser.add_argument("-i", "--input", required=True,  help="Ingrese el nombre del archivo de entrada")
parser.add_argument("-o", "--output", required=True, help="Nombre de el archivo de salida")
parser.add_argument("-f", "--formato", default="txt", help="Formato de salida (por defecto 'txt')")

#parsea los argumentos
args = parser.parse_args()

#Mostrar valores ingresados
print(f"Archivo de entrada: {args.input}")
#Mostrar valores de salida
print(f"Archivo de salida: {args.output}")
#El formato
print(f"formato de salida: {args.formato}")
