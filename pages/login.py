from nicegui import app, ui

from auth import get_admin_credentials
from database import load_data
from theme import add_app_theme


def render():
    app.storage.user.clear()

    config = load_data('config.json', {'modo_escuro': False})
    add_app_theme()

    if config.get('modo_escuro'):
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()

    ui.add_css('''
        .login-shell {
            background:
                linear-gradient(135deg, color-mix(in srgb, var(--app-primary) 14%, transparent), transparent 42%),
                linear-gradient(315deg, color-mix(in srgb, var(--app-coral) 16%, transparent), transparent 46%),
                var(--app-bg);
        }

        .login-side {
            background: var(--app-happy) !important;
            min-height: 460px;
        }

        .login-chip {
            background: color-mix(in srgb, var(--app-surface) 78%, transparent);
            border: 1px solid var(--app-border);
            border-radius: 8px;
        }
    ''')

    with ui.row().classes('login-shell w-full min-h-screen items-center justify-center p-4'):
        with ui.row().classes('app-card w-full max-w-5xl overflow-hidden'):
            with ui.column().classes('login-side hidden md:flex w-1/2 p-10 justify-between'):
                with ui.column().classes('gap-4'):
                    ui.label('☀️').classes('text-6xl')
                    ui.label('Um espaço calmo, colorido e organizado para a escola cuidar melhor.').classes('text-3xl font-black leading-tight')
                    ui.label('Feito para apoiar a rotina de crianças com TEA, professores e coordenação.').classes('app-muted text-base leading-relaxed')

                with ui.grid(columns=2).classes('w-full gap-3'):
                    for texto in ['🧩 Rotina clara', '💬 Comunicação', '🤝 Acolhimento', '⭐ Progresso']:
                        ui.label(texto).classes('login-chip p-3 text-sm font-bold')

            with ui.column().classes('w-full md:w-1/2 p-8 md:p-10 items-center justify-center'):
                ui.image('/assets/ruth-see-logo.png').classes('w-28 h-28 object-contain mb-4')
                ui.label('Ruth See Escola').classes('text-4xl font-black mb-1 text-center')
                ui.label('Entrar no painel da equipe escolar').classes('app-muted mb-8 text-center')

                email_input = ui.input('E-mail').classes('w-full mb-4').props('outlined')
                senha_input = ui.input('Senha', password=True, password_toggle_button=True).classes('w-full mb-8').props('outlined')

                def fazer_login():
                    email = email_input.value
                    senha = senha_input.value

                    if not email or not senha:
                        ui.notify('Por favor, preencha todos os campos. 😊', type='warning')
                        return

                    admin_email, admin_password = get_admin_credentials()
                    if email == admin_email and senha == admin_password:
                        app.storage.user.update({
                            'nome': 'Administrador Padrão',
                            'email': email,
                            'cargo': 'Administrador',
                            'foto': '',
                        })
                        ui.notify('Login de administrador realizado! ✨', type='positive')
                        ui.navigate.to('/')
                        return

                    usuarios = load_data('usuarios.json', [])
                    usuario_valido = next((u for u in usuarios if u.get('email') == email and u.get('senha') == senha), None)

                    if usuario_valido:
                        app.storage.user.update(usuario_valido)
                        primeiro_nome = usuario_valido.get('nome', 'Usuário').split(' ')[0]
                        ui.notify(f'Bem-vindo(a), {primeiro_nome}! ⭐', type='positive')
                        ui.navigate.to('/')
                    else:
                        ui.notify('E-mail ou senha incorretos.', type='negative')

                ui.button('Entrar ✨', on_click=fazer_login).classes('w-full py-3 text-lg font-bold mb-4').props('unelevated color=primary')
                ui.label('Dados salvos localmente em arquivos JSON.').classes('app-muted text-xs text-center')
