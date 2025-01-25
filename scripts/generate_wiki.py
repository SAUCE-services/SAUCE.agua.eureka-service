from github import Github
import os
import json

def generate_wiki_pages():
    # Inicializar cliente de GitHub
    g = Github(os.environ['GITHUB_TOKEN'])
    repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])
    
    # Obtener Wiki
    wiki = repo.get_wiki()
    
    # Generar página principal
    home_content = """# SAUCE Agua Eureka Service Wiki

Bienvenido a la Wiki del servicio Eureka de SAUCE Agua.

## Navegación Rápida

- [[Milestones]]
- [[Issues Activos]]
- [[Issues Cerrados]]
- [[Historial de Cambios]]
"""
    try:
        wiki.create_page("Home", "Wiki Home", home_content)
    except:
        wiki.update_page("Home", "Wiki Update", home_content)

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
    
    try:
        wiki.create_page("Milestones", "Milestones Update", milestone_content)
    except:
        wiki.update_page("Milestones", "Milestones Update", milestone_content)

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
    
    try:
        wiki.create_page("Issues-Activos", "Active Issues Update", active_content)
    except:
        wiki.update_page("Issues-Activos", "Active Issues Update", active_content)

if __name__ == '__main__':
    generate_wiki_pages() 