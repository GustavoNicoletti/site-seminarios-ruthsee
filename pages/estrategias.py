from nicegui import ui
from layout import frame
from database import load_data, save_data

def render():
    with frame('Biblioteca de Estratégias'):
        estrategias = load_data('estrategias.json', [])
        
        categorias = [
            'Comunicação', 'Rotina', 'Manejo de crises', 
            'Sensibilidade sensorial', 'Inclusão escolar', 
            'Interação social', 'Atividades pedagógicas', 'Reforço positivo'
        ]
        
        editing_index = {'value': -1}

        def abrir_modal(estrategia=None, index=-1):
            editing_index['value'] = index
            if estrategia:
                titulo_input.value = estrategia.get('titulo', '')
                categoria_input.value = estrategia.get('categoria', categorias[0])
                conteudo_input.value = estrategia.get('conteudo', '')
                quando_usar_input.value = estrategia.get('quando_usar', '')
                quando_evitar_input.value = estrategia.get('quando_evitar', '')
                obs_input.value = estrategia.get('observacoes', '')
                dialog_title.set_text('Editar Estratégia')
            else:
                titulo_input.value = ''
                categoria_input.value = categorias[0]
                conteudo_input.value = ''
                quando_usar_input.value = ''
                quando_evitar_input.value = ''
                obs_input.value = ''
                dialog_title.set_text('Nova Estratégia')
            dialog.open()

        def salvar_estrategia():
            if not titulo_input.value:
                ui.notify('O título é obrigatório.', type='negative')
                return
                
            dados = {
                'titulo': titulo_input.value,
                'categoria': categoria_input.value,
                'conteudo': conteudo_input.value,
                'quando_usar': quando_usar_input.value,
                'quando_evitar': quando_evitar_input.value,
                'observacoes': obs_input.value
            }
            
            if editing_index['value'] >= 0:
                estrategias[editing_index['value']] = dados
                ui.notify('Estratégia atualizada com sucesso!', type='positive')
            else:
                estrategias.append(dados)
                ui.notify('Estratégia cadastrada com sucesso!', type='positive')
                
            save_data('estrategias.json', estrategias)
            dialog.close()
            atualizar_lista()

        def confirmar_exclusao(estrategia):
            with ui.dialog() as confirm_dialog, ui.card().classes('p-6 rounded-2xl'):
                ui.label('Confirmar Exclusão').classes('text-xl font-bold text-red-600 mb-4')
                ui.label(f'Tem certeza que deseja apagar a estratégia "{estrategia["titulo"]}"?')
                ui.label('Esta ação não pode ser desfeita.').classes('text-sm text-gray-500 mb-4')
                with ui.row().classes('w-full justify-end gap-2'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Apagar', on_click=lambda: apagar_estrategia(estrategia, confirm_dialog)).props('unelevated color=red rounded')
            confirm_dialog.open()

        def apagar_estrategia(estrategia, confirm_dialog):
            estrategias.remove(estrategia)
            save_data('estrategias.json', estrategias)
            ui.notify('Estratégia removida.', type='warning')
            confirm_dialog.close()
            atualizar_lista()

        with ui.dialog() as dialog, ui.card().classes('w-full max-w-3xl p-6 rounded-2xl'):
            dialog_title = ui.label('Nova Estratégia').classes('text-2xl font-bold mb-4')
            with ui.scroll_area().classes('w-full h-[60vh] pr-4'):
                with ui.row().classes('w-full gap-4 mb-2'):
                    titulo_input = ui.input('Título *').classes('flex-grow')
                    categoria_input = ui.select(categorias, label='Categoria').classes('w-1/3')
                conteudo_input = ui.textarea('Conteúdo completo da estratégia').classes('w-full mb-4')
                with ui.row().classes('w-full gap-4 mb-2'):
                    quando_usar_input = ui.textarea('Quando utilizar (Indicações)').classes('flex-1')
                    quando_evitar_input = ui.textarea('Quando evitar (Contraindicações)').classes('flex-1')
                obs_input = ui.textarea('Observações adicionais').classes('w-full mb-4')
            with ui.row().classes('w-full justify-end gap-2 mt-4 pt-4 border-t'):
                ui.button('Cancelar', on_click=dialog.close).props('flat')
                ui.button('Salvar', on_click=salvar_estrategia).props('unelevated color=primary rounded')

        with ui.row().classes('w-full justify-between items-center mb-6'):
            busca_input = ui.input('Buscar por título ou categoria...').classes('w-full md:w-1/2')
            with busca_input.add_slot('prepend'):
                ui.icon('search')
            ui.button('Nova Estratégia', icon='add', on_click=lambda: abrir_modal()).props('unelevated color=primary rounded-xl')

        container_lista = ui.grid(columns=1).classes('w-full gap-6 md:grid-cols-2 xl:grid-cols-3')

        def atualizar_lista():
            container_lista.clear()
            termo = busca_input.value.lower() if busca_input.value else ''
            with container_lista:
                for i, est in enumerate(estrategias):
                    if termo and termo not in est.get('titulo', '').lower() and termo not in est.get('categoria', '').lower():
                        continue
                    with ui.card().classes('w-full p-5 rounded-2xl shadow-sm hover:shadow-md transition-shadow duration-300 flex flex-col h-full'):
                        with ui.row().classes('w-full justify-between items-start mb-2'):
                            ui.badge(est.get('categoria', 'Geral'), color='accent').classes('px-2 py-1')
                            with ui.row().classes('gap-1'):
                                ui.button(icon='edit', on_click=lambda i=i, est=est: abrir_modal(est, i)).props('flat color=primary size=sm round padding=xs').tooltip('Editar')
                                ui.button(icon='delete', on_click=lambda est=est: confirmar_exclusao(est)).props('flat color=red size=sm round padding=xs').tooltip('Remover')
                        ui.label(est.get('titulo', 'Sem título')).classes('text-xl font-bold mb-2 line-clamp-2 text-gray-800 dark:text-gray-100')
                        conteudo = est.get('conteudo', '')
                        if len(conteudo) > 100:
                            conteudo = conteudo[:100] + '...'
                        ui.label(conteudo).classes('text-gray-600 dark:text-gray-300 text-sm flex-grow mb-4')
                        ui.separator().classes('mb-3')
                        with ui.expansion('Ver detalhes completos', icon='info').classes('w-full text-sm'):
                            ui.label('Quando utilizar:').classes('font-bold mt-2 text-green-600')
                            ui.label(est.get('quando_usar', '-')).classes('mb-2')
                            ui.label('Quando evitar:').classes('font-bold text-red-600')
                            ui.label(est.get('quando_evitar', '-')).classes('mb-2')
                            if est.get('observacoes'):
                                ui.label('Observações:').classes('font-bold text-blue-600')
                                ui.label(est.get('observacoes')).classes('mb-2')

        busca_input.on_value_change(lambda _: atualizar_lista())
        atualizar_lista()