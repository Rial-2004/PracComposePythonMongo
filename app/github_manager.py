import requests
import json
import base64

def parse_github_url(url):
    """
    Limpia la URL proporcionada para obtener el formato 'usuario/repositorio'.
    Soporta formatos SSH (git@github.com:user/repo.git) y HTTPS.
    """
    # Eliminar el .git al final si existe
    url = url.replace(".git", "") 
    
    # Si es formato SSH
    if "git@github.com:" in url:
        return url.split("git@github.com:")[1]
    
    # Si es formato HTTPS
    if "https://github.com/" in url:
        return url.split("https://github.com/")[1]
    
    return url

def export_to_github(token, repo_url, file_path, data):
    """
    Convierte los datos de la base de datos a JSON y los sube a GitHub.
    """
    repo = parse_github_url(repo_url)
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    
    # 1. Preparar los datos: Convertir a JSON y luego a Base64 (requerido por GitHub)
    json_data = json.dumps(data, indent=4)
    content_b64 = base64.b64encode(json_data.encode()).decode()

    headers = {"Authorization": f"token {token}"}
    
    # 2. Verificar si el archivo ya existe para obtener su SHA (necesario para actualizarlo)
    resp = requests.get(url, headers=headers)
    sha = resp.json().get('sha') if resp.status_code == 200 else None

    # 3. Crear el cuerpo del mensaje para la API
    payload = {
        "message": "Actualización automática de base de datos escolar",
        "content": content_b64
    }
    if sha: 
        payload["sha"] = sha

    # 4. Enviar la petición PUT a GitHub
    response = requests.put(url, headers=headers, json=payload)
    return response.status_code in [200, 201]

def import_from_github(token, repo_url, file_path):
    """
    Descarga el archivo JSON desde GitHub y lo devuelve como un objeto Python.
    """
    repo = parse_github_url(repo_url)
    url = f"https://api.github.com/repos/{repo}/contents/{file_path}"
    headers = {"Authorization": f"token {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Decodificar el contenido que viene en Base64
        content_b64 = response.json().get('content')
        json_data = base64.b64decode(content_b64).decode()
        return json.loads(json_data)
    
    return None