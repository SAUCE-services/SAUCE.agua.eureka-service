import requests
import json
import os
import base64

def generate_wiki_pages():
    # Configuración
    token = os.environ['GITHUB_TOKEN']
    repo = os.environ['GITHUB_REPOSITORY']
    api_url = f"https://api.github.com/repos/{repo}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json',
        'User-Agent': 'SAUCE-Wiki-Generator'
    }

    print(f"Iniciando generación de Wiki para {repo}")

    # Verificar y habilitar Wiki
    repo_response = requests.get(api_url, headers=headers)
    if repo_response.status_code == 200:
        repo_data = repo_response.json()
        if not repo_data.get('has_wiki'):
            print("Habilitando Wiki...")
            enable_response = requests.patch(
                api_url,
                headers=headers,
                json={'has_wiki': True}
            )
            if enable_response.status_code != 200:
                print(f"Error habilitando wiki: {enable_response.status_code}")
                print(enable_response.text)
                return
    else:
        print(f"Error accediendo al repositorio: {repo_response.status_code}")
        return

    def update_wiki_page(page_name, content):
        print(f"\nActualizando página: {page_name}")
        wiki_url = f"https://api.github.com/repos/{repo}/wiki/{page_name}"
        
        print(f"URL de la Wiki: {wiki_url}")
        print(f"Headers utilizados: {headers}")
        
        # Verificar si la wiki está habilitada antes de cada operación
        repo_check = requests.get(api_url, headers=headers)
        if not repo_check.json().get('has_wiki'):
            print("Error: Wiki no está habilitada")
            return

        data = {
            'message': f'Update {page_name}',
            'content': content,
            'name': page_name,
            'sha': None
        }

        get_response = requests.get(wiki_url, headers=headers)
        print(f"GET response status: {get_response.status_code}")
        if get_response.status_code == 200:
            print("Página existente encontrada")
            data['sha'] = get_response.json().get('sha')
        elif get_response.status_code == 404:
            print("Página nueva será creada")
        else:
            print(f"GET response inesperado: {get_response.text}")

        print("Actualizando/creando página...")
        response = requests.put(
            wiki_url,
            headers=headers,
            json=data
        )
        print(f"PUT response status: {response.status_code}")
        print(f"PUT response headers: {response.headers}")
        print(f"PUT response body: {response.text}")

    # Verificar existencia de archivos
    if not os.path.exists('data/issues.json'):
        print("Error: No se encontró el archivo issues.json")
        return
    if not os.path.exists('data/milestones.json'):
        print("Error: No se encontró el archivo milestones.json")
        return

    # Verificar contenido de archivos
    try:
        with open('data/issues.json', 'r') as f:
            issues = json.load(f)
        with open('data/milestones.json', 'r') as f:
            milestones = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decodificando JSON: {e}")
        return

    # Generar página principal
    home_content = """# SAUCE Agua Eureka Service Wiki

Bienvenido a la Wiki del servicio Eureka de SAUCE Agua.

## Navegación Rápida

- [Milestones](Milestones)
- [Issues Activos](Issues-Activos)
- [Issues Cerrados](Issues-Cerrados)
- [Historial de Cambios](Historial-de-Cambios)
"""
    update_wiki_page('Home', home_content)

    # Generar página de Milestones
    milestone_content = "# Milestones\n\n"
    for ms in milestones:
        milestone_content += f"## {ms['title']}\n"
        milestone_content += f"**Estado:** {ms['state']}\n\n"
        milestone_content += f"**Descripción:** {ms['description']}\n\n"
        if ms['due_on']:
            milestone_content += f"**Fecha límite:** {ms['due_on']}\n\n"
        milestone_content += "---\n\n"
    
    update_wiki_page('Milestones', milestone_content)

    # Generar páginas de Issues
    active_issues = [i for i in issues if i['state'] == 'open']
    closed_issues = [i for i in issues if i['state'] == 'closed']
    
    # Página de Issues Activos
    active_content = "# Issues Activos\n\n"
    for issue in active_issues:
        active_content += f"## #{issue['number']}: {issue['title']}\n"
        active_content += f"**Creado:** {issue['created_at']}\n\n"
        if issue['milestone']:
            active_content += f"**Milestone:** {issue['milestone']}\n\n"
        if issue['labels']:
            active_content += f"**Labels:** {', '.join(issue['labels'])}\n\n"
        active_content += f"{issue['body']}\n\n---\n\n"
    
    update_wiki_page('Issues-Activos', active_content)

    # Página de Issues Cerrados
    closed_content = "# Issues Cerrados\n\n"
    for issue in closed_issues:
        closed_content += f"## #{issue['number']}: {issue['title']}\n"
        closed_content += f"**Creado:** {issue['created_at']}\n"
        closed_content += f"**Cerrado:** {issue['closed_at']}\n\n"
        if issue['milestone']:
            closed_content += f"**Milestone:** {issue['milestone']}\n\n"
        if issue['labels']:
            closed_content += f"**Labels:** {', '.join(issue['labels'])}\n\n"
        closed_content += f"{issue['body']}\n\n---\n\n"
    
    update_wiki_page('Issues-Cerrados', closed_content)

if __name__ == '__main__':
    generate_wiki_pages() 