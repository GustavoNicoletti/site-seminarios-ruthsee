from nicegui import ui
from layout import frame
from database import load_data, save_data

def render():
    with frame('Configurações'):
        config_data = load_data('config.json', {
            'nome': 'Professor(a)',
            'email': 'prof@adaptaescola.com',
            'foto': '',
            'modo_escuro': False
        })

        def salvar_configuracoes():
            config_data['nome'] = nome_input.value
            config_data['email'] = email_input.value
            config_data['foto'] = foto_input.value
            config_data['modo_escuro'] = escuro_switch.value
            
            save_data('config.json', config_data)
            ui.notify('Configurações salvas com sucesso!', type='positive')
            ui.timer(1.0, lambda: ui.run_javascript('window.location.reload()'), once=True)

        with ui.column().classes('w-full items-center p-4'):
            with ui.card().classes('w-full max-w-2xl p-8 rounded-2xl shadow-lg'):
                ui.label('Configurações do Perfil').classes('text-2xl font-bold mb-6')
                
                with ui.row().classes('w-full gap-6 mb-6 items-center'):
                    foto_url = config_data.get('foto', '').strip()
                    if foto_url:
                        ui.image(foto_url).classes('w-24 h-24 rounded-full object-cover border-2 border-gray-200')
                    else:
                        initial = config_data.get('nome', 'P')[0].upper() if config_data.get('nome') else 'P'
                        ui.label(initial).classes('w-24 h-24 rounded-full bg-blue-500 text-white flex items-center justify-center text-4xl font-bold')
                    
                    with ui.column().classes('flex-grow gap-2'):
                        nome_input = ui.input('Nome Completo', value=config_data.get('nome')).classes('w-full')
                        foto_input = ui.input('URL da Foto (Opcional)', value=config_data.get('foto')).classes('w-full')
                
                email_input = ui.input('E-mail', value=config_data.get('email')).classes('w-full mb-6')
                
                ui.separator().classes('my-4')
                
                ui.label('Preferências').classes('text-lg font-semibold mb-4')
                escuro_switch = ui.switch('Ativar Modo Escuro', value=config_data.get('modo_escuro')).classes('mb-6')
                
                ui.button('Salvar Alterações', icon='save', on_click=salvar_configuracoes).props('unelevated color=primary size=lg').classes('w-full')