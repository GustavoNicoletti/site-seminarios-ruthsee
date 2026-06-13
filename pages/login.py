from nicegui import app, ui

from auth import get_admin_credentials
from database import load_data
from theme import add_app_theme


def render():
    app.storage.user.clear()

    config = load_data('config.json', {'modo_escuro': False})
    usuarios = load_data('usuarios.json', [])
    add_app_theme()

    if config.get('modo_escuro'):
        ui.dark_mode().enable()
    else:
        ui.dark_mode().disable()

    ui.add_css('''
        .login-shell {
            background:
                linear-gradient(135deg, color-mix(in srgb, var(--app-primary) 12%, transparent), transparent 38%),
                linear-gradient(315deg, color-mix(in srgb, var(--app-teal) 16%, transparent), transparent 44%),
                var(--app-bg);
        }

        .login-card {
            position: relative;
            width: min(455px, calc(100vw - 2rem));
        }

        .login-form-panel {
            background:
                radial-gradient(circle at top right, color-mix(in srgb, var(--app-teal) 13%, transparent), transparent 34%),
                radial-gradient(circle at bottom left, color-mix(in srgb, var(--app-primary) 10%, transparent), transparent 36%),
                var(--app-surface) !important;
        }

        .login-form-inner {
            width: 100%;
        }

        .login-logo-frame {
            width: 5.35rem;
            height: 5.35rem;
            border-radius: 8px;
            background: white;
            object-fit: contain;
            padding: 0.45rem;
            border: 1px solid var(--app-border);
            box-shadow: var(--app-soft-shadow);
        }

        .login-profile-preview {
            background: color-mix(in srgb, var(--app-surface) 88%, transparent) !important;
            border: 1px solid var(--app-border);
            border-radius: 8px;
            box-shadow: var(--app-soft-shadow);
            backdrop-filter: blur(12px);
        }

        .login-profile-photo {
            width: 3rem;
            height: 3rem;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid var(--app-border);
        }

        .login-mini-note {
            background: var(--app-surface-muted) !important;
            border: 1px solid var(--app-border);
            border-radius: 8px;
        }

        .login-access-pill {
            background: color-mix(in srgb, var(--app-primary) 12%, transparent);
            border: 1px solid color-mix(in srgb, var(--app-primary) 22%, transparent);
            border-radius: 999px;
            color: var(--app-primary-strong) !important;
        }

        @media (max-width: 640px) {
            .login-card {
                width: min(100%, calc(100vw - 1.25rem));
            }
        }
    ''')

    preview_state = {'container': None}

    def _login_usuario(usuario):
        return str(usuario or '').strip().lower()

    def _preferencias(usuario):
        preferencias = usuario.get('preferencias') or {}
        return preferencias if isinstance(preferencias, dict) else {}

    def _pagina_inicial(usuario):
        rotas_validas = {'/', '/agenda', '/alunos', '/turmas', '/pais', '/registros', '/relatorios', '/impressao', '/estrategias'}
        pagina = _preferencias(usuario).get('pagina_inicial', '/')
        return pagina if pagina in rotas_validas else '/'

    def usuario_por_login(login):
        login = _login_usuario(login)
        if not login:
            return None
        admin_usuario, _ = get_admin_credentials()
        if login == _login_usuario(admin_usuario):
            return {
                'nome': config.get('nome') or 'Administrador Padrão',
                'cargo': config.get('cargo') or 'Administrador',
                'foto': config.get('foto', ''),
                'usuario': admin_usuario,
                'preferencias': config.get('preferencias', {}),
            }
        return next((u for u in usuarios if _login_usuario(u.get('usuario') or u.get('email')) == login), None)

    def atualizar_preview():
        preview_container = preview_state['container']
        if preview_container is None:
            return
        preview_container.clear()
        usuario = usuario_por_login(usuario_input.value)
        preview_container.visible = bool(usuario)
        with preview_container:
            if usuario:
                foto = usuario.get('foto', '').strip()
                nome = usuario.get('nome', 'Usuário')
                if foto:
                    ui.image(foto).classes('login-profile-photo')
                else:
                    ui.avatar(nome[0].upper()).classes('brand-badge text-white font-black w-12 h-12')
                with ui.column().classes('gap-0 min-w-0'):
                    ui.label(nome.split(' ')[0]).classes('font-black leading-tight')
                    ui.label(usuario.get('cargo', 'Equipe escolar')).classes('app-muted text-xs font-bold uppercase')
        preview_container.update()

    with ui.row().classes('login-shell w-full min-h-screen items-center justify-center p-4'):
        with ui.row().classes('app-card login-card overflow-hidden'):
            with ui.column().classes('login-form-panel w-full p-7 md:p-8 items-center justify-center'):
                with ui.column().classes('login-form-inner items-center'):
                    ui.image('/assets/ruth-see-logo.png').classes('login-logo-frame mb-4')
                    ui.label('Acesso da equipe').classes('login-access-pill text-xs font-black px-3 py-1 mb-4')
                    ui.label('Bem-vindo(a)').classes('text-3xl font-black mb-1 text-center leading-tight')
                    ui.label('Entre para acompanhar a rotina escolar.').classes('app-muted mb-5 text-center text-sm')

                    with ui.row().classes('login-mini-note w-full items-center gap-3 p-3 mb-4'):
                        ui.icon('verified_user', size='sm').classes('tone-teal')
                        ui.label('Use seu usuário de acesso e senha cadastrados pela coordenação.').classes('app-muted text-xs font-bold leading-snug')

                    usuario_input = ui.input('Usuário').classes('w-full mb-3').props('outlined autocomplete=username')
                    with usuario_input.add_slot('prepend'):
                        ui.icon('person').classes('app-muted')

                    preview_state['container'] = ui.row().classes('login-profile-preview w-full items-center gap-3 px-3 py-2 mb-3')
                    preview_state['container'].visible = False

                    senha_input = ui.input('Senha', password=True, password_toggle_button=True).classes('w-full mb-5').props('outlined autocomplete=current-password')
                    with senha_input.add_slot('prepend'):
                        ui.icon('lock').classes('app-muted')
                    usuario_input.on_value_change(lambda _: atualizar_preview())
                    atualizar_preview()

                    def fazer_login():
                        login = usuario_input.value
                        senha = senha_input.value

                        if not login or not senha:
                            ui.notify('Por favor, preencha todos os campos. 😊', type='warning')
                            return

                        admin_usuario, admin_password = get_admin_credentials()
                        if _login_usuario(login) == _login_usuario(admin_usuario) and senha == admin_password:
                            usuario_admin = {
                                'nome': config.get('nome') or 'Administrador Padrão',
                                'usuario': admin_usuario,
                                'email': '',
                                'cargo': 'Administrador',
                                'foto': config.get('foto', ''),
                                'bio': config.get('bio', ''),
                                'tipo': 'admin_padrao',
                                'preferencias': {
                                    **(config.get('preferencias', {}) if isinstance(config.get('preferencias'), dict) else {}),
                                    'modo_escuro': bool(config.get('modo_escuro')),
                                },
                            }
                            app.storage.user.update(usuario_admin)
                            ui.notify('Login de administrador realizado! ✨', type='positive')
                            ui.navigate.to(_pagina_inicial(usuario_admin))
                            return

                        usuario_valido = next(
                            (
                                u for u in usuarios
                                if _login_usuario(u.get('usuario') or u.get('email')) == _login_usuario(login)
                                and u.get('senha') == senha
                            ),
                            None,
                        )

                        if usuario_valido:
                            if not usuario_valido.get('usuario'):
                                usuario_valido['usuario'] = usuario_valido.get('email', '')
                            app.storage.user.update(usuario_valido)
                            primeiro_nome = usuario_valido.get('nome', 'Usuário').split(' ')[0]
                            ui.notify(f'Bem-vindo(a), {primeiro_nome}! ⭐', type='positive')
                            ui.navigate.to(_pagina_inicial(usuario_valido))
                        else:
                            ui.notify('Usuário ou senha incorretos.', type='negative')

                    senha_input.on('keydown.enter', lambda _: fazer_login())
                    usuario_input.on('keydown.enter', lambda _: fazer_login())

                    ui.button('Entrar no sistema', icon='login', on_click=fazer_login).classes('w-full py-3 text-base font-bold mb-4').props('unelevated color=primary no-caps')
                    ui.label('Dados salvos localmente em arquivos JSON.').classes('app-muted text-xs text-center')
