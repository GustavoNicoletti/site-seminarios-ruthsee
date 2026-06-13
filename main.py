from nicegui import app, ui
from pages import login, dashboard, alunos, pais, prontuario, registros, relatorios, estrategias, usuarios, admin, config
from auth import get_app_port, get_storage_secret

app.add_static_files('/assets', 'assets')

@ui.page('/login')
def login_page():
    login.render()

@ui.page('/')
def dashboard_page():
    dashboard.render()

@ui.page('/alunos')
def alunos_page():
    alunos.render()

@ui.page('/alunos/{aluno_index}/prontuario')
def prontuario_page(aluno_index: str):
    prontuario.render(aluno_index)

@ui.page('/pais')
def pais_page():
    pais.render()

@ui.page('/registros')
def registros_page():
    registros.render()

@ui.page('/relatorios')
def relatorios_page():
    relatorios.render()

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
    ui.run(title='Ruth See Escola', port=get_app_port(), storage_secret=get_storage_secret())
