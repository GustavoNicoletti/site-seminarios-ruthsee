from nicegui import ui

from database import load_data, save_data
from layout import frame


def render():
    with frame('Configurações'):
        config = load_data('config.json', {'nome': 'Professor(a)', 'foto': '', 'cargo': 'Professor', 'bio': ''})

        with ui.column().classes('w-full max-w-4xl mx-auto gap-5'):
            with ui.row().classes('app-card-colorful w-full items-center justify-between gap-5 p-6'):
                with ui.column().classes('gap-2'):
                    ui.label('⚙️ Meu cantinho').classes('app-muted text-sm font-black uppercase')
                    ui.label('Perfil da equipe').classes('text-3xl font-black')
                    ui.label('Personalize como seu nome aparece no sistema.').classes('app-muted text-sm')
                ui.label('😊').classes('text-5xl')

            with ui.card().classes('app-card w-full p-6'):
                with ui.row().classes('items-center gap-5 mb-6'):
                    foto_url = config.get('foto', '').strip()
                    if foto_url:
                        ui.image(foto_url).classes('w-24 h-24 rounded-full object-cover')
                    else:
                        primeira_letra = config.get('nome', 'P')[0].upper() if config.get('nome') else 'P'
                        ui.label(primeira_letra).classes('brand-badge w-24 h-24 flex items-center justify-center text-4xl font-black')

                    with ui.column().classes('gap-1'):
                        ui.label(config.get('nome', 'Professor(a)')).classes('text-2xl font-black')
                        ui.label(config.get('cargo', 'Professor')).classes('app-pill text-sm font-black px-3 py-1 w-fit')
                        ui.label('Essas informações ajudam a deixar o sistema mais pessoal. 🌻').classes('app-muted text-sm')

                with ui.grid(columns=2).classes('w-full gap-4'):
                    ui.input('Nome de exibição').props('outlined').classes('w-full').bind_value(config, 'nome')
                    ui.input('Cargo / função').props('outlined').classes('w-full').bind_value(config, 'cargo')

                ui.input('URL da foto (opcional)').props('outlined').classes('w-full mt-4').bind_value(config, 'foto')
                ui.textarea('Notas / biografia').props('outlined autogrow').classes('w-full mt-4').bind_value(config, 'bio')

                def salvar_perfil():
                    save_data('config.json', config)
                    ui.notify('Perfil salvo com sucesso! ⭐', type='positive')

                with ui.row().classes('w-full justify-end mt-6'):
                    ui.button('Salvar perfil ✨', icon='save', on_click=salvar_perfil).props('unelevated color=primary')
