from nicegui import ui, app
from layout import frame
from database import load_data, save_data
import datetime

def render():
    with frame('Administração do Sistema'):
        comunicados = load_data('comunicados.json', [])
        despesas = load_data('despesas.json', [])
        
        # --- LÓGICA DE COMUNICADOS ---
        def salvar_comunicado():
            if not titulo_input.value or not mensagem_input.value:
                ui.notify('Preencha o título e a mensagem.', type='warning')
                return
                
            novo_aviso = {
                'titulo': titulo_input.value,
                'mensagem': mensagem_input.value,
                'data': datetime.datetime.now().strftime("%d/%m/%Y"),
                'autor': app.storage.user.get('nome', 'Administração').split(' ')[0]
            }
            
            comunicados.append(novo_aviso)
            save_data('comunicados.json', comunicados)
            ui.notify('Comunicado publicado com sucesso!', type='positive')
            
            titulo_input.value = ''
            mensagem_input.value = ''
            atualizar_lista_comunicados()

        def confirmar_exclusao_comunicado(aviso):
            with ui.dialog() as confirm_dialog, ui.card().classes('p-6 rounded-2xl'):
                ui.label('Confirmar Exclusão').classes('text-xl font-bold text-red-600 mb-4')
                ui.label(f'Tem certeza que deseja apagar o comunicado "{aviso["titulo"]}"?')
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Apagar', on_click=lambda: apagar_comunicado(aviso, confirm_dialog)).props('unelevated color=red rounded')
            confirm_dialog.open()

        def apagar_comunicado(aviso, confirm_dialog):
            comunicados.remove(aviso)
            save_data('comunicados.json', comunicados)
            ui.notify('Comunicado removido.', type='warning')
            confirm_dialog.close()
            atualizar_lista_comunicados()

        # --- LÓGICA DE DESPESAS ---
        def salvar_despesa():
            if not desc_despesa_input.value or not valor_despesa_input.value:
                ui.notify('Preencha a descrição e o valor.', type='warning')
                return
            
            try:
                valor_float = float(str(valor_despesa_input.value).replace(',', '.'))
            except ValueError:
                ui.notify('Digite um valor numérico válido.', type='warning')
                return
                
            nova_despesa = {
                'descricao': desc_despesa_input.value,
                'valor': valor_float,
                'data': datetime.datetime.now().strftime("%d/%m/%Y"),
                'autor': app.storage.user.get('nome', 'Administração').split(' ')[0]
            }
            
            despesas.append(nova_despesa)
            save_data('despesas.json', despesas)
            ui.notify('Despesa registrada com sucesso!', type='positive')
            
            desc_despesa_input.value = ''
            valor_despesa_input.value = ''
            atualizar_lista_despesas()

        def confirmar_exclusao_despesa(despesa):
            with ui.dialog() as confirm_dialog, ui.card().classes('p-6 rounded-2xl'):
                ui.label('Confirmar Exclusão').classes('text-xl font-bold text-red-600 mb-4')
                ui.label(f'Tem certeza que deseja apagar a despesa "{despesa["descricao"]}"?')
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Apagar', on_click=lambda: apagar_despesa(despesa, confirm_dialog)).props('unelevated color=red rounded')
            confirm_dialog.open()

        def apagar_despesa(despesa, confirm_dialog):
            despesas.remove(despesa)
            save_data('despesas.json', despesas)
            ui.notify('Despesa removida.', type='warning')
            confirm_dialog.close()
            atualizar_lista_despesas()

        # --- INTERFACE COM TABS ---
        with ui.tabs().classes('w-full mb-6') as tabs:
            tab_comunicados = ui.tab('Comunicados', icon='campaign')
            tab_despesas = ui.tab('Despesas', icon='account_balance_wallet')

        with ui.tab_panels(tabs, value=tab_comunicados).classes('w-full bg-transparent p-0'):
            
            # PAINEL DE COMUNICADOS
            with ui.tab_panel(tab_comunicados):
                with ui.card().classes('w-full p-6 rounded-2xl shadow-sm mb-8 border border-gray-100 dark:border-gray-800'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('campaign', size='sm').classes('text-primary')
                        ui.label('Publicar Novo Comunicado').classes('text-xl font-bold text-gray-800 dark:text-gray-100')
                    
                    titulo_input = ui.input('Título do Comunicado *').classes('w-full mb-4')
                    mensagem_input = ui.textarea('Mensagem *').classes('w-full mb-4')
                    
                    with ui.row().classes('w-full justify-end'):
                        ui.button('Publicar no Dashboard', icon='send', on_click=salvar_comunicado).props('unelevated color=primary rounded-xl px-6')

                ui.label('Comunicados Ativos').classes('text-xl font-bold mb-4 text-gray-800 dark:text-gray-100')
                container_comunicados = ui.column().classes('w-full gap-4')

                def atualizar_lista_comunicados():
                    container_comunicados.clear()
                    with container_comunicados:
                        if not comunicados:
                            ui.label('Nenhum comunicado publicado.').classes('text-gray-500 italic')
                        
                        for c in reversed(comunicados):
                            with ui.card().classes('w-full p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800'):
                                with ui.row().classes('w-full justify-between items-start'):
                                    with ui.column().classes('gap-1 flex-1'):
                                        ui.label(c.get('titulo', '')).classes('font-bold text-lg text-gray-800 dark:text-gray-100')
                                        ui.label(f"Publicado em {c.get('data', '')} por {c.get('autor', '')}").classes('text-xs text-gray-500')
                                    
                                    ui.button(icon='delete', on_click=lambda c=c: confirmar_exclusao_comunicado(c)).props('flat color=red round size=sm').tooltip('Remover Comunicado')
                                
                                ui.label(c.get('mensagem', '')).classes('text-gray-700 dark:text-gray-300 mt-3 text-sm')

                atualizar_lista_comunicados()

            # PAINEL DE DESPESAS
            with ui.tab_panel(tab_despesas):
                with ui.card().classes('w-full p-6 rounded-2xl shadow-sm mb-8 border border-gray-100 dark:border-gray-800'):
                    with ui.row().classes('items-center gap-2 mb-4'):
                        ui.icon('account_balance_wallet', size='sm').classes('text-emerald-500')
                        ui.label('Registrar Nova Despesa').classes('text-xl font-bold text-gray-800 dark:text-gray-100')
                    
                    with ui.row().classes('w-full gap-4 mb-4'):
                        desc_despesa_input = ui.input('Descrição da Despesa *').classes('flex-1')
                        valor_despesa_input = ui.input('Valor (R$) *').props('type=number step=0.01').classes('w-1/3')
                    
                    with ui.row().classes('w-full justify-end'):
                        ui.button('Registrar Despesa', icon='add_circle', on_click=salvar_despesa).props('unelevated color=positive rounded-xl px-6')

                ui.label('Histórico de Despesas').classes('text-xl font-bold mb-4 text-gray-800 dark:text-gray-100')
                container_despesas = ui.column().classes('w-full gap-4')

                def atualizar_lista_despesas():
                    container_despesas.clear()
                    with container_despesas:
                        if not despesas:
                            ui.label('Nenhuma despesa registrada.').classes('text-gray-500 italic')
                        
                        for d in reversed(despesas):
                            with ui.card().classes('w-full p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-800 flex-row justify-between items-center'):
                                with ui.column().classes('gap-0'):
                                    ui.label(d.get('descricao', '')).classes('font-bold text-lg text-gray-800 dark:text-gray-100')
                                    ui.label(f"Registrado em {d.get('data', '')} por {d.get('autor', '')}").classes('text-xs text-gray-500')
                                
                                with ui.row().classes('items-center gap-4'):
                                    valor_formatado = f"R$ {float(d.get('valor', 0)):.2f}".replace('.', ',')
                                    ui.label(valor_formatado).classes('text-xl font-black text-emerald-600 dark:text-emerald-400')
                                    ui.button(icon='delete', on_click=lambda d=d: confirmar_exclusao_despesa(d)).props('flat color=red round size=sm').tooltip('Remover Despesa')

                atualizar_lista_despesas()