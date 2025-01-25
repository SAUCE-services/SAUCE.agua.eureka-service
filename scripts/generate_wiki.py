import os
import json
import subprocess
from pathlib import Path
import requests

def generate_wiki_pages():
    # Guardar directorio original
    original_dir = os.getcwd()
    data_dir = os.path.join(original_dir, 'data')
    
    print("Iniciando generación de Wiki")
    
    # Crear directorio temporal para la wiki
    wiki_dir = Path(original_dir) / 'wiki_content'
    if wiki_dir.exists():
        subprocess.run(['rm', '-rf', str(wiki_dir)])
    wiki_dir.mkdir(exist_ok=True)
    
    # Configuración
    token = os.environ['GITHUB_TOKEN']
    repo = os.environ['GITHUB_REPOSITORY']
    api_url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Verificar y habilitar wiki
    print("Verificando estado de la wiki...")
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        repo_data = response.json()
        if not repo_data.get('has_wiki'):
            print("Habilitando wiki...")
            response = requests.patch(api_url, headers=headers, json={'has_wiki': True})
            if response.status_code != 200:
                print(f"Error habilitando wiki: {response.status_code}")
                return
    else:
        print(f"Error verificando repositorio: {response.status_code}")
        return

    # URL para git con autenticación
    wiki_url = f"https://x-access-token:{token}@github.com/{repo}.wiki.git"
    
    try:
        # Configurar git
        subprocess.run(['git', 'config', '--global', 'user.name', 'github-actions[bot]'])
        subprocess.run(['git', 'config', '--global', 'user.email', 'github-actions[bot]@users.noreply.github.com'])
        
        # Intentar clonar o inicializar la wiki
        print("Intentando clonar wiki...")
        result = subprocess.run(['git', 'clone', wiki_url, 'wiki_content'], 
                              capture_output=True,
                              text=True)
        
        if 'fatal' in result.stderr:
            print("Wiki no existe, inicializando...")
            os.chdir(wiki_dir)
            subprocess.run(['git', 'init'])
            subprocess.run(['git', 'remote', 'add', 'origin', wiki_url])
            subprocess.run(['git', 'checkout', '-b', 'main'])  # Crear y cambiar a rama main
        
        # Generar contenido usando paths absolutos
        generate_wiki_content(wiki_dir, data_dir)
        
        # Commit y push (asegurándonos de estar en el directorio correcto)
        os.chdir(str(wiki_dir))
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'Update wiki content'])
        
        if 'fatal' in result.stderr:
            # Para primera inicialización
            subprocess.run(['git', 'push', '--set-upstream', 'origin', 'main'])  # Usar main en lugar de master
        else:
            subprocess.run(['git', 'push'])
        
    except Exception as e:
        print(f"Error: {e}")
        raise  # Re-lanzar la excepción para que el workflow falle si hay error
    finally:
        os.chdir(original_dir)  # Siempre volver al directorio original
        if wiki_dir.exists():
            subprocess.run(['rm', '-rf', str(wiki_dir)])

def generate_wiki_content(wiki_dir, data_dir):
    # Verificar archivos JSON usando paths absolutos
    issues_file = os.path.join(data_dir, 'issues.json')
    milestones_file = os.path.join(data_dir, 'milestones.json')
    
    if not os.path.exists(issues_file) or not os.path.exists(milestones_file):
        raise FileNotFoundError("Archivos de datos no encontrados")

    # Cargar datos
    with open(issues_file, 'r') as f:
        issues = json.load(f)
    with open(milestones_file, 'r') as f:
        milestones = json.load(f)

    # Generar Home.md
    with open(wiki_dir / 'Home.md', 'w') as f:
        f.write("""# SAUCE Agua Eureka Service Wiki

Bienvenido a la Wiki del servicio Eureka de SAUCE Agua.

## Navegación Rápida

- [[Milestones]]
- [[Issues-Activos]]
- [[Issues-Cerrados]]
""")

    # Generar Milestones.md
    with open(wiki_dir / 'Milestones.md', 'w') as f:
        f.write("# Milestones\n\n")
        for ms in milestones:
            f.write(f"## {ms['title']}\n")
            f.write(f"**Estado:** {ms['state']}\n\n")
            f.write(f"**Descripción:** {ms['description']}\n\n")
            if ms['due_on']:
                f.write(f"**Fecha límite:** {ms['due_on']}\n\n")
            f.write("---\n\n")

    # Generar Issues-Activos.md
    active_issues = [i for i in issues if i['state'] == 'open']
    with open(wiki_dir / 'Issues-Activos.md', 'w') as f:
        f.write("# Issues Activos\n\n")
        for issue in active_issues:
            f.write(f"## #{issue['number']}: {issue['title']}\n")
            f.write(f"**Creado:** {issue['created_at']}\n\n")
            if issue['milestone']:
                f.write(f"**Milestone:** {issue['milestone']}\n\n")
            if issue['labels']:
                f.write(f"**Labels:** {', '.join(issue['labels'])}\n\n")
            f.write(f"{issue['body']}\n\n---\n\n")

    # Generar Issues-Cerrados.md
    closed_issues = [i for i in issues if i['state'] == 'closed']
    with open(wiki_dir / 'Issues-Cerrados.md', 'w') as f:
        f.write("# Issues Cerrados\n\n")
        for issue in closed_issues:
            f.write(f"## #{issue['number']}: {issue['title']}\n")
            f.write(f"**Creado:** {issue['created_at']}\n")
            f.write(f"**Cerrado:** {issue['closed_at']}\n\n")
            if issue['milestone']:
                f.write(f"**Milestone:** {issue['milestone']}\n\n")
            if issue['labels']:
                f.write(f"**Labels:** {', '.join(issue['labels'])}\n\n")
            f.write(f"{issue['body']}\n\n---\n\n")

if __name__ == '__main__':
    generate_wiki_pages() 