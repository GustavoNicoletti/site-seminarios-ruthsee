from nicegui import ui
from contextlib import contextmanager
import json
import os

def load_data(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default_data
    return default_data

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

@contextmanager
def frame(nav_title: str):
    config = load_data('config.json', {
        'nome': 'Professor(a)', 
        'modo_escuro': False, 
        'foto': ''
    })
    
    ui.colors(primary='#6366f1', secondary='#14b8a6', accent='#a855f7', positive='#22c55e')
    
    ui.add_css('''
        .menu-link { transition: all 0.3s ease !important; }
        .menu-link:hover { transform: translateX(5px); background-color: rgba(99, 102, 241, 0.1) !important; color: #6366f1 !important; }
        .body--dark .menu-link:hover { color: #818cf8 !important; }
        
        .nicegui-card { transition: all 0.3s ease !important; border: 1px solid rgba(0,0,0,0.03); background-color: white !important; }
        .body--dark .nicegui-card { border: 1px solid rgba(255,255,255,0.05); background-color: #1e293b !important; color: #f1f5f9 !important; }
        .nicegui-card:hover { transform: translateY(-3px); box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1) !important; }
        
        .q-header { background-color: white !important; color: #1f2937 !important; transition: background-color 0.3s ease; }
        .body--dark .q-header { background-color: #0f172a !important; color: white !important; border-bottom: 1px solid rgba(255,255,255,0.05); }
        
        .q-drawer { background-color: #f8fafc !important; transition: background-color 0.3s ease; }
        .body--dark .q-drawer { background-color: #0f172a !important; border-right: 1px solid rgba(255,255,255,0.05); }
        
        .body--dark .text-gray-800, .body--dark .text-gray-600, .body--dark .text-gray-700 { color: #f1f5f9 !important; }
        .body--dark body { background-color: #0f172a !important; color: #f1f5f9 !important; }
    ''')
    
    dark = ui.dark_mode()
    if config.get('modo_escuro'):
        dark.enable()
    else:
        dark.disable()
        
    def toggle_theme():
        if dark.value:
            dark.disable()
            config['modo_escuro'] = False
        else:
            dark.enable()
            config['modo_escuro'] = True
        save_data('config.json', config)
    
    with ui.header(elevated=True).classes('justify-between items-center px-6 py-3'):
        with ui.row().classes('items-center gap-4'):
            ui.button(on_click=lambda: left_drawer.toggle(), icon='menu').props('flat round')
            with ui.row().classes('items-center gap-2'):
                ui.icon('child_care').classes('text-3xl text-primary')
                ui.label('AdaptaEscola').classes('text-2xl font-bold text-primary hidden sm:block')
        
        with ui.row().classes('items-center gap-4'):
            ui.button(icon='dark_mode', on_click=toggle_theme).props('flat round').tooltip('Alternar Tema')
            ui.label(config.get('nome', '').split(' ')[0]).classes('font-medium hidden md:block')
            
            foto_url = config.get('foto', '').strip()
            if foto_url:
                ui.image(foto_url).classes('w-10 h-10 rounded-full object-cover border-2 border-primary/20')
            else:
                primeira_letra = config.get('nome', 'P')[0].upper() if config.get('nome') else 'P'
                ui.avatar(primeira_letra).classes('bg-primary text-white font-bold w-10 h-10')

    with ui.left_drawer(elevated=True) as left_drawer:
        with ui.column().classes('w-full p-4 gap-2'):
            ui.label('MENU PRINCIPAL').classes('text-xs font-bold text-gray-400 mb-2 tracking-widest')
            
            def menu_btn(name, icon, route):
                btn = ui.button(name, icon=icon, on_click=lambda r=route: ui.navigate.to(r))
                btn.classes('w-full justify-start rounded-xl menu-link font-medium')
                btn.props('flat no-caps')
            
            menu_btn('Dashboard', 'space_dashboard', '/')
            menu_btn('Alunos', 'face', '/alunos')
            menu_btn('Estratégias', 'auto_awesome', '/estrategias')
            menu_btn('Administração', 'admin_panel_settings', '/admin')
            menu_btn('Configurações', 'tune', '/config')

    with ui.column().classes('w-full max-w-6xl mx-auto p-6 lg:p-10'):
        with ui.row().classes('w-full items-center justify-between mb-8'):
            ui.label(nav_title).classes('text-4xl font-extrabold tracking-tight')
        yield