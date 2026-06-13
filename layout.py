from contextlib import contextmanager

from nicegui import app, ui

from database import load_data, save_data
from theme import add_app_theme


@contextmanager
def frame(nav_title: str):
    config = load_data('config.json', {'modo_escuro': False})
    add_app_theme()
    dark = ui.dark_mode(config.get('modo_escuro'))

    user = app.storage.user
    if not user.get('nome'):
        ui.navigate.to('/login')
        with ui.column().classes('hidden'):
            yield
        return

    nome_usuario = user.get('nome', 'Usuário')
    cargo_usuario = user.get('cargo', 'Professor')
    foto_usuario = user.get('foto', '').strip()

    def toggle_theme():
        if dark.value:
            dark.disable()
            config['modo_escuro'] = False
        else:
            dark.enable()
            config['modo_escuro'] = True
        save_data('config.json', config)

    def fazer_logout():
        app.storage.user.clear()
        ui.navigate.to('/login')

    page_emojis = {
        'Dashboard': '🏫',
        'Alunos': '☀️',
        'Prontuário do Aluno': '📁',
        'Pais e Responsáveis': '☎️',
        'Registros de Acompanhamento': '📝',
        'Relatórios': '📊',
        'Biblioteca de Estratégias': '💡',
        'Gestão de Usuários': '👥',
        'Administração do Sistema': '📣',
        'Configurações': '⚙️',
    }
    page_emoji = page_emojis.get(nav_title, '✨')

    with ui.header(elevated=False).classes('app-header fixed top-0 left-0 right-0 justify-between items-center px-6 py-3'):
        with ui.row().classes('items-center gap-4'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat round').classes('app-muted')
            with ui.row().classes('items-center gap-3'):
                ui.image('/assets/ruth-see-logo.png').classes('w-11 h-11 rounded-lg object-contain bg-white p-1')
                with ui.column().classes('gap-0'):
                    ui.label('Ruth See Escola').classes('text-xl font-black leading-tight')
                    ui.label('Rotina escolar com carinho').classes('app-muted text-[11px] font-bold uppercase hidden sm:block')

        with ui.row().classes('items-center gap-4'):
            theme_icon = 'light_mode' if config.get('modo_escuro') else 'dark_mode'
            ui.button(icon=theme_icon, on_click=toggle_theme).props('flat round').classes('app-muted').tooltip('Alternar tema')

            with ui.row().classes('items-center gap-2 cursor-pointer'):
                with ui.column().classes('gap-0 items-end hidden md:flex'):
                    ui.label(nome_usuario.split(' ')[0]).classes('font-bold leading-none')
                    ui.label(cargo_usuario).classes('app-muted text-[10px] uppercase')

                if foto_usuario:
                    ui.image(foto_usuario).classes('w-10 h-10 rounded-full object-cover')
                else:
                    ui.avatar(nome_usuario[0].upper()).classes('bg-primary text-white font-bold w-10 h-10')

                with ui.menu():
                    ui.menu_item('Sair do Sistema', on_click=fazer_logout).classes('text-red-600 font-bold')

    with ui.left_drawer(elevated=False).classes('app-drawer flex flex-col justify-between') as left_drawer:
        with ui.column().classes('w-full p-4 gap-2'):
            ui.label('MENU PRINCIPAL ✨').classes('app-muted text-xs font-bold')

            def menu_btn(name, icon, route):
                ui.button(name, icon=icon, on_click=lambda r=route: ui.navigate.to(r)).classes('w-full justify-start menu-link').props('flat no-caps')

            menu_btn('🏫 Dashboard', 'space_dashboard', '/')
            menu_btn('☀️ Alunos', 'face', '/alunos')
            menu_btn('☎️ Pais', 'contact_phone', '/pais')
            menu_btn('📝 Registros', 'edit_note', '/registros')
            menu_btn('📊 Relatórios', 'analytics', '/relatorios')
            menu_btn('💡 Estratégias', 'auto_awesome', '/estrategias')

            if cargo_usuario in ['Administrador', 'Coordenador']:
                ui.separator().classes('my-2')
                ui.label('GESTÃO 🤝').classes('app-muted text-xs font-bold')
                menu_btn('👥 Usuários', 'people', '/usuarios')
                menu_btn('📣 Administração', 'admin_panel_settings', '/admin')

        with ui.column().classes('w-full p-4'):
            menu_btn('⚙️ Configurações', 'tune', '/config')

    with ui.column().classes('w-full max-w-7xl mx-auto px-5 md:px-8 py-6 mt-16 gap-6'):
        with ui.row().classes('items-center gap-3'):
            ui.label(page_emoji).classes('emoji-badge')
            ui.label(nav_title).classes('app-page-title')
        yield
