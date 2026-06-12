from nicegui import ui
from pages import dashboard, alunos, estrategias, admin, config

# Registro das rotas (Páginas)
@ui.page('/')
def page_dashboard():
    dashboard.render()

@ui.page('/alunos')
def page_alunos():
    alunos.render()

@ui.page('/estrategias')
def page_estrategias():
    estrategias.render()

@ui.page('/admin')
def page_admin():
    admin.render()

@ui.page('/config')
def page_config():
    config.render()

# Inicialização do Servidor
ui.run(title='AdaptaEscola', favicon='🧩', language='pt-BR')