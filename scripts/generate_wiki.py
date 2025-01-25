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
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    def update_wiki_page(page_name, content):
        # Codificar contenido en base64
        content_bytes = content.encode('utf-8')
        content_base64 = base64.b64encode(content_bytes).decode('utf-8')

        # Crear o actualizar página
        data = {
            'message': f'Update {page_name}',
            'content': content_base64,
            'branch': 'master'  # La rama wiki por defecto
        }

        # Intentar actualizar la página
        response = requests.put(
            f"{api_url}/wiki/{page_name}",
            headers=headers,
            json=data
        )
        
        if response.status_code not in [200, 201]:
            print(f"Error updating {page_name}: {response.status_code}")
            print(response.text)

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
    with open('data/milestones.json', 'r') as f:
        milestones = json.load(f)
    
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
    with open('data/issues.json', 'r') as f:
        issues = json.load(f)
    
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