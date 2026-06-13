from nicegui import ui
from pages import login, dashboard, alunos, estrategias, usuarios, admin, config

@ui.page('/login')
def login_page():
    login.render()

@ui.page('/')
def dashboard_page():
    dashboard.render()

@ui.page('/alunos')
def alunos_page():
    alunos.render()

@ui.page('/estrategias')
def estrategias_page():
    estrategias.render()

@ui.page('/usuarios')
def usuarios_page():
    usuarios.render()

@ui.page('/admin')
def admin_page():
    admin.render()

@ui.page('/config')
def config_page():
    config.render()

if __name__ in {'__main__', '__mp_main__'}:
    ui.run(title='AdaptaEscola', port=8080, storage_secret='adapta_escola_secreto_123')