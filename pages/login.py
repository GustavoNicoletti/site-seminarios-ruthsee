from nicegui import ui, app
from database import load_data

def render():
    app.storage.user.clear()
    
    config = load_data('config.json', {'modo_escuro': False})
    
    dark_css = '''
        <style id="dark-mode-fix">
            body, .q-layout, .q-page-container, .q-header, .q-drawer {
                background-color: #0f172a !important;
                color: #f1f5f9 !important;
            }
            .nicegui-card, .q-card {
                background-color: #1e293b !important;
                color: #f1f5f9 !important;
            }
            .text-gray-800, .text-gray-600, .text-gray-700 { color: #f1f5f9 !important; }
        </style>
    '''
    
    if config.get('modo_escuro'):
        ui.add_head_html(dark_css)
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()
    
    with ui.column().classes('w-full min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-900 p-4'):
        with ui.card().classes('w-full max-w-md p-8 rounded-2xl shadow-xl items-center border border-gray-100 dark:border-slate-800'):
            ui.icon('child_care', size='4rem').classes('text-primary mb-2')
            ui.label('AdaptaEscola').classes('text-3xl font-bold text-gray-800 dark:text-white mb-1')
            ui.label('Faça login para acessar o sistema').classes('text-gray-500 dark:text-gray-400 mb-8 text-center')

            email_input = ui.input('E-mail').classes('w-full mb-4').props('outlined')
            senha_input = ui.input('Senha', password=True, password_toggle_button=True).classes('w-full mb-8').props('outlined')

            def fazer_login():
                email = email_input.value
                senha = senha_input.value
                
                if not email or not senha:
                    ui.notify('Por favor, preencha todos os campos.', type='warning')
                    return

                if email == 'admin@adaptaescola.com' and senha == 'admin123':
                    app.storage.user.update({
                        'nome': 'Administrador Padrão',
                        'email': email,
                        'cargo': 'Administrador',
                        'foto': ''
                    })
                    ui.notify('Login de administrador realizado!', type='positive')
                    ui.navigate.to('/')
                    return

                usuarios = load_data('usuarios.json', [])
                usuario_valido = next((u for u in usuarios if u.get('email') == email and u.get('senha') == senha), None)

                if usuario_valido:
                    app.storage.user.update(usuario_valido)
                    primeiro_nome = usuario_valido.get("nome", "Usuário").split(" ")[0]
                    ui.notify(f'Bem-vindo(a), {primeiro_nome}!', type='positive')
                    ui.navigate.to('/')
                else:
                    ui.notify('E-mail ou senha incorretos.', type='negative')

            ui.button('Entrar', on_click=fazer_login).classes('w-full py-3 text-lg font-bold rounded-xl mb-6').props('unelevated color=primary')