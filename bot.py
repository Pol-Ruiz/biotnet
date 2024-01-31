import subprocess
import os
 
def run():


# URL del archivo raw en GitHub
url = "https://raw.githubusercontent.com/AlessandroZ/LaZagne/blob/master/Linux/laZagne.py"

# Descargar el archivo
subprocess.run(["curl", "-O", url], check=True)

# Nombre del archivo descargado
nombre_archivo = url.split("/")[-1]

# Ejecutar el archivo con el argumento "all"
subprocess.run(["python3", nombre_archivo, "all"], check=True)
