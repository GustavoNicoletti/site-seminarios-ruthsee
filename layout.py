from nicegui import ui, app
from contextlib import contextmanager
import json
import os

def load_data(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return default_data

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@contextmanager
def frame(nav_title: str):
    # 1. PROTEÇÃO DE ROTA: Se não tem nome na sessão, não está logado!
    user = app.storage.user
    if not user.get('nome'):
        ui.navigate.to('/login')
        yield
        return

    # Pega os dados do usuário logado
    nome_usuario = user.get('nome', 'Usuário')
    cargo_usuario = user.get('cargo', 'Professor')
    foto_usuario = user.get('foto', '').strip()

    # Carrega configurações do sistema (modo escuro)
    config = load_data('config.json', {'modo_escuro': False})
    
    dark_css = '''
        <style id="dark-mode-fix">
            body, .q-layout, .q-page-container, .q-header, .q-drawer { background-color: #0f172a !important; color: #f1f5f9 !important; }
            .nicegui-card, .q-card { background-color: #1e293b !important; color: #f1f5f9 !important; }
            .text-gray-800, .text-gray-600, .text-gray-700 { color: #f1f5f9 !important; }
        </style>
    '''
    if config.get('modo_escuro'):
        ui.add_head_html(dark_css)
    
    ui.colors(primary='#6366f1', secondary='#14b8a6', accent='#a855f7', positive='#22c55e')
    
    ui.add_css('''
        .menu-link { transition: all 0.3s ease; }
        .menu-link:hover { transform: translateX(5px); background-color: rgba(99, 102, 241, 0.1); color: #6366f1 !important; }
        .nicegui-card { transition: all 0.3s ease; }
        .nicegui-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1); }
    ''')
    
    dark = ui.dark_mode(config.get('modo_escuro'))
        
    def toggle_theme():
        if dark.value:
            dark.disable()
            config['modo_escuro'] = False
            ui.run_javascript('document.getElementById("dark-mode-fix")?.remove();')
        else:
            dark.enable()
            config['modo_escuro'] = True
            ui.run_javascript(f'if (!document.getElementById("dark-mode-fix")) {{ document.head.insertAdjacentHTML("beforeend", `{dark_css}`); }}')
        save_data('config.json', config)
        
    def fazer_logout():
        app.storage.user.clear()
        ui.navigate.to('/login')
    
    with ui.header(elevated=True).classes('fixed top-0 left-0 right-0 justify-between items-center bg-[#4f46e5] dark:bg-slate-900 px-6 py-3'):
        with ui.row().classes('items-center gap-4'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat round').classes('text-white/80')
            ui.label('AdaptaEscola').classes('text-2xl font-bold text-white')
        
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='dark_mode', on_click=toggle_theme).props('flat round').classes('text-white/80')
            
            with ui.row().classes('items-center gap-2 cursor-pointer'):
                with ui.column().classes('gap-0 items-end hidden md:flex'):
                    ui.label(nome_usuario.split(' ')[0]).classes('font-bold text-white leading-none')
                    ui.label(cargo_usuario).classes('text-[10px] text-white/70 uppercase')
                
                if foto_usuario:
                    ui.image(foto_usuario).classes('w-10 h-10 rounded-full object-cover border-2 border-white/20')
                else:
                    ui.avatar(nome_usuario[0].upper()).classes('bg-white text-[#4f46e5] font-bold w-10 h-10')
                
                with ui.menu():
                    ui.menu_item('Sair do Sistema', on_click=fazer_logout).classes('text-red-600 font-bold')

    with ui.left_drawer(elevated=True).classes('bg-slate-50 dark:bg-slate-900 flex flex-col justify-between') as left_drawer:
        with ui.column().classes('w-full p-4 gap-2'):
            ui.label('MENU PRINCIPAL').classes('text-xs font-bold text-gray-400')
            
            def menu_btn(name, icon, route):
                ui.button(name, icon=icon, on_click=lambda r=route: ui.navigate.to(r)).classes('w-full justify-start rounded-xl menu-link').props('flat no-caps')

            menu_btn('Dashboard', 'space_dashboard', '/')
            menu_btn('Alunos', 'face', '/alunos')
            menu_btn('Estratégias', 'auto_awesome', '/estrategias')
            
            if cargo_usuario in ['Administrador', 'Coordenador']:
                ui.separator().classes('my-2')
                ui.label('GESTÃO').classes('text-xs font-bold text-gray-400')
                menu_btn('Usuários', 'people', '/usuarios')
                menu_btn('Administração', 'admin_panel_settings', '/admin')
            
        with ui.column().classes('w-full p-4'):
            menu_btn('Configurações', 'tune', '/config')

    with ui.column().classes('w-full max-w-6xl mx-auto p-6 mt-16'):
        ui.label(nav_title).classes('text-4xl font-extrabold text-gray-800 dark:text-white mb-8')
        yield