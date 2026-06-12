from nicegui import ui
from layout import frame
from database import load_data, save_data
import datetime

def render():
    with frame('Administração'):
        despesas = load_data('despesas.json', [])
        comunicados = load_data('comunicados.json', [])

        with ui.row().classes('w-full gap-8 flex-wrap md:flex-nowrap'):
            
            # --- COLUNA 1: COMUNICADOS ---
            with ui.column().classes('w-full md:w-1/2'):
                ui.label('Gestão de Comunicados').classes('text-xl font-bold mb-2')
                
                with ui.card().classes('w-full p-6 rounded-2xl shadow-sm mb-4'):
                    titulo_input = ui.input('Título do Comunicado').classes('w-full mb-2')
                    msg_input = ui.textarea('Mensagem').classes('w-full mb-4')
                    
                    def salvar_comunicado():
                        if not titulo_input.value or not msg_input.value:
                            ui.notify('Preencha título e mensagem.', type='warning')
                            return
                        
                        comunicados.insert(0, {
                            'titulo': titulo_input.value,
                            'mensagem': msg_input.value,
                            'data': datetime.datetime.now().strftime("%d/%m/%Y")
                        })
                        save_data('comunicados.json', comunicados)
                        
                        titulo_input.value = ''
                        msg_input.value = ''
                        ui.notify('Comunicado publicado!', type='positive')
                        atualizar_comunicados()
                        
                    ui.button('Publicar Comunicado', icon='campaign', on_click=salvar_comunicado).props('unelevated color=primary rounded-xl w-full')

                lista_comunicados = ui.column().classes('w-full gap-3')
                
                def atualizar_comunicados():
                    lista_comunicados.clear()
                    with lista_comunicados:
                        if not comunicados:
                            ui.label('Nenhum comunicado registrado.').classes('text-gray-400 italic')
                        for c in comunicados:
                            with ui.card().classes('w-full p-4 rounded-xl bg-blue-50 dark:bg-slate-800'):
                                with ui.row().classes('w-full justify-between items-start'):
                                    with ui.column().classes('gap-0'):
                                        ui.label(c['titulo']).classes('font-bold text-blue-800 dark:text-blue-300')
                                        ui.label(c['data']).classes('text-xs text-gray-500')
                                    ui.button(icon='delete', on_click=lambda c=c: apagar_comunicado(c)).props('flat color=red size=sm round padding=xs')
                                ui.label(c['mensagem']).classes('text-sm text-gray-700 dark:text-gray-300 mt-2')
                                
                def apagar_comunicado(c):
                    comunicados.remove(c)
                    save_data('comunicados.json', comunicados)
                    ui.notify('Comunicado removido.', type='warning')
                    atualizar_comunicados()
                    
                atualizar_comunicados()

            # --- COLUNA 2: DESPESAS E BACKUP ---
            with ui.column().classes('w-full md:w-1/2'):
                ui.label('Gestão Financeira').classes('text-xl font-bold mb-2')
                
                with ui.card().classes('w-full p-6 rounded-2xl shadow-sm mb-4'):
                    desc_input = ui.input('Descrição da Despesa').classes('w-full mb-2')
                    valor_input = ui.number('Valor (R$)', format='%.2f').classes('w-full mb-4')
                    
                    def salvar_despesa():
                        if not desc_input.value or valor_input.value is None:
                            ui.notify('Preencha descrição e valor.', type='warning')
                            return
                        
                        despesas.insert(0, {
                            'descricao': desc_input.value,
                            'valor': float(valor_input.value),
                            'data': datetime.datetime.now().strftime("%d/%m/%Y")
                        })
                        save_data('despesas.json', despesas)
                        
                        desc_input.value = ''
                        valor_input.value = None
                        ui.notify('Despesa registrada!', type='positive')
                        atualizar_despesas()
                        
                    ui.button('Registrar Despesa', icon='add_shopping_cart', on_click=salvar_despesa).props('unelevated color=secondary rounded-xl w-full')

                lista_despesas = ui.column().classes('w-full gap-3 mb-6')
                
                def atualizar_despesas():
                    lista_despesas.clear()
                    with lista_despesas:
                        if not despesas:
                            ui.label('Nenhuma despesa registrada.').classes('text-gray-400 italic')
                        for d in despesas:
                            with ui.card().classes('w-full p-4 rounded-xl border-l-4 border-secondary'):
                                with ui.row().classes('w-full justify-between items-center'):
                                    with ui.column().classes('gap-0'):
                                        ui.label(d['descricao']).classes('font-bold text-gray-800 dark:text-gray-100')
                                        ui.label(d['data']).classes('text-xs text-gray-500')
                                    with ui.row().classes('items-center gap-3'):
                                        ui.label(f"R$ {d['valor']:.2f}").classes('font-bold text-secondary text-lg')
                                        ui.button(icon='delete', on_click=lambda d=d: apagar_despesa(d)).props('flat color=red size=sm round padding=xs')
                                        
                def apagar_despesa(d):
                    despesas.remove(d)
                    save_data('despesas.json', despesas)
                    ui.notify('Despesa removida.', type='warning')
                    atualizar_despesas()
                    
                atualizar_despesas()
                
                ui.label('Sistema').classes('text-xl font-bold mb-2 mt-2')
                with ui.card().classes('w-full p-6 rounded-2xl shadow-sm'):
                    ui.label('Backup de Dados').classes('font-bold mb-1')
                    ui.label('Baixe os arquivos para manter uma cópia de segurança.').classes('text-sm text-gray-500 mb-4')
                    with ui.row().classes('gap-2 w-full'):
                        ui.button('Alunos', icon='download', on_click=lambda: ui.download('data/alunos.json')).props('outline rounded-xl size=sm flex-1')
                        ui.button('Estratégias', icon='download', on_click=lambda: ui.download('data/estrategias.json')).props('outline rounded-xl size=sm flex-1')