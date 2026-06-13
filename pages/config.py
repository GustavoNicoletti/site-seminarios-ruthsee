from nicegui import ui
from layout import frame
from database import load_data, save_data

def render():
    with frame('Configurações'):
        # Adicionamos 'cargo' e 'bio' nos dados padrão
        config = load_data('config.json', {'nome': 'Professor(a)', 'foto': '', 'cargo': 'Professor', 'bio': ''})
        
        with ui.column().classes('w-full max-w-2xl mx-auto'):
            # --- CARD DE PERFIL ---
            with ui.card().classes('w-full p-8 rounded-3xl shadow-sm border border-gray-100 dark:border-gray-800'):
                ui.label('Perfil do Usuário').classes('text-xl font-bold dark:text-gray-100 mb-6')
                
                with ui.row().classes('items-center gap-6 mb-8'):
                    foto_url = config.get('foto', '').strip()
                    if foto_url:
                        ui.image(foto_url).classes('w-24 h-24 rounded-full object-cover border-4 border-primary/20')
                    else:
                        primeira_letra = config.get('nome', 'P')[0].upper() if config.get('nome') else 'P'
                        ui.label(primeira_letra).classes('w-24 h-24 rounded-full bg-primary text-white flex items-center justify-center text-4xl font-bold shadow-sm')
                
                # Nome e Cargo lado a lado em telas maiores
                with ui.row().classes('w-full gap-4 mb-4'):
                    nome_input = ui.input('Nome de Exibição').classes('flex-1').bind_value(config, 'nome')
                    cargo_input = ui.input('Cargo / Função').classes('flex-1').bind_value(config, 'cargo')
                
                foto_input = ui.input('URL da Foto (opcional)').classes('w-full mb-4').bind_value(config, 'foto')
                
                # Novo campo de Notas/Bio
                bio_input = ui.textarea('Notas / Biografia').classes('w-full mb-6').bind_value(config, 'bio')
                
                def salvar_perfil():
                    save_data('config.json', config)
                    ui.notify('Perfil salvo com sucesso! Recarregue a página para ver as alterações.', type='positive')
                
                with ui.row().classes('w-full justify-end'):
                    ui.button('Salvar Perfil', on_click=salvar_perfil).props('unelevated color=primary rounded-xl px-8 py-2 font-bold')