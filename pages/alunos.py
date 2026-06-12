from nicegui import ui
from layout import frame
from database import load_data, save_data

def render():
    with frame('Gestão de Alunos'):
        alunos = load_data('alunos.json', [])
        
        editing_index = {'value': -1}

        def abrir_modal(aluno=None, index=-1):
            editing_index['value'] = index
            if aluno:
                nome_input.value = aluno.get('nome', '')
                idade_input.value = aluno.get('idade', '')
                turma_input.value = aluno.get('turma', '')
                obs_input.value = aluno.get('observacoes', '')
                fortes_input.value = aluno.get('pontos_fortes', '')
                dificuldades_input.value = aluno.get('dificuldades', '')
                cuidados_input.value = aluno.get('cuidados', '')
                evitar_input.value = aluno.get('evitar', '')
                estrategias_input.value = aluno.get('estrategias', '')
                medicamentos_input.value = aluno.get('medicamentos', '')
                adicionais_input.value = aluno.get('adicionais', '')
                anotacoes_input.value = aluno.get('anotacoes', '')
                dialog_title.set_text('Editar Aluno')
            else:
                nome_input.value = ''
                idade_input.value = None
                turma_input.value = ''
                obs_input.value = ''
                fortes_input.value = ''
                dificuldades_input.value = ''
                cuidados_input.value = ''
                evitar_input.value = ''
                estrategias_input.value = ''
                medicamentos_input.value = ''
                adicionais_input.value = ''
                anotacoes_input.value = ''
                dialog_title.set_text('Novo Aluno')
            dialog.open()

        def salvar_aluno():
            if not nome_input.value:
                ui.notify('O nome é obrigatório.', type='negative')
                return
                
            dados_aluno = {
                'nome': nome_input.value,
                'idade': idade_input.value,
                'turma': turma_input.value,
                'observacoes': obs_input.value,
                'pontos_fortes': fortes_input.value,
                'dificuldades': dificuldades_input.value,
                'cuidados': cuidados_input.value,
                'evitar': evitar_input.value,
                'estrategias': estrategias_input.value,
                'medicamentos': medicamentos_input.value,
                'adicionais': adicionais_input.value,
                'anotacoes': anotacoes_input.value
            }
            
            if editing_index['value'] >= 0:
                alunos[editing_index['value']] = dados_aluno
                ui.notify('Aluno atualizado com sucesso!', type='positive')
            else:
                alunos.append(dados_aluno)
                ui.notify('Aluno cadastrado com sucesso!', type='positive')
                
            save_data('alunos.json', alunos)
            dialog.close()
            atualizar_lista()

        def confirmar_exclusao(aluno):
            with ui.dialog() as confirm_dialog, ui.card().classes('p-6 rounded-2xl'):
                ui.label('Confirmar Exclusão').classes('text-xl font-bold text-red-600 mb-4')
                ui.label(f'Tem certeza que deseja apagar os dados de {aluno["nome"]}?')
                ui.label('Esta ação não pode ser desfeita.').classes('text-sm text-gray-500 mb-4')
                with ui.row().classes('w-full justify-end gap-2'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Apagar', on_click=lambda: apagar_aluno(aluno, confirm_dialog)).props('unelevated color=red rounded')
            confirm_dialog.open()

        def apagar_aluno(aluno, confirm_dialog):
            alunos.remove(aluno)
            save_data('alunos.json', alunos)
            ui.notify('Aluno removido.', type='warning')
            confirm_dialog.close()
            atualizar_lista()

        with ui.dialog() as dialog, ui.card().classes('w-full max-w-4xl p-6 rounded-2xl'):
            dialog_title = ui.label('Novo Aluno').classes('text-2xl font-bold mb-4')
            with ui.scroll_area().classes('w-full h-[60vh] pr-4'):
                nome_input = ui.input('Nome Completo *').classes('w-full mb-2')
                with ui.row().classes('w-full gap-4 mb-2'):
                    idade_input = ui.number('Idade').classes('flex-1')
                    turma_input = ui.input('Turma').classes('flex-1')
                ui.label('Perfil do Aluno').classes('font-bold text-gray-600 mt-4 mb-2')
                obs_input = ui.textarea('Observações gerais').classes('w-full mb-2')
                with ui.row().classes('w-full gap-4 mb-2'):
                    fortes_input = ui.textarea('Pontos fortes').classes('flex-1')
                    dificuldades_input = ui.textarea('Dificuldades').classes('flex-1')
                ui.label('Manejo e Cuidados').classes('font-bold text-gray-600 mt-4 mb-2')
                with ui.row().classes('w-full gap-4 mb-2'):
                    cuidados_input = ui.textarea('Cuidados necessários').classes('flex-1')
                    evitar_input = ui.textarea('O que evitar (Gatilhos)').classes('flex-1')
                estrategias_input = ui.textarea('Estratégias recomendadas').classes('w-full mb-2')
                ui.label('Saúde e Outros').classes('font-bold text-gray-600 mt-4 mb-2')
                medicamentos_input = ui.input('Medicamentos utilizados').classes('w-full mb-2')
                adicionais_input = ui.textarea('Informações adicionais').classes('w-full mb-2')
                anotacoes_input = ui.textarea('Anotações livres').classes('w-full mb-4')
            with ui.row().classes('w-full justify-end gap-2 mt-4 pt-4 border-t'):
                ui.button('Cancelar', on_click=dialog.close).props('flat')
                ui.button('Salvar', on_click=salvar_aluno).props('unelevated color=primary rounded')

        with ui.row().classes('w-full justify-between items-center mb-6'):
            pesquisa_input = ui.input('Pesquisar aluno...').classes('w-1/3')
            with pesquisa_input.add_slot('prepend'):
                ui.icon('search')
            ui.button('Cadastrar Aluno', icon='add', on_click=lambda: abrir_modal()).props('unelevated color=primary rounded-xl')

        container_lista = ui.column().classes('w-full gap-4')

        def atualizar_lista():
            container_lista.clear()
            termo = pesquisa_input.value.lower() if pesquisa_input.value else ''
            with container_lista:
                filtrados = [a for a in alunos if termo in a.get('nome', '').lower()]
                if not filtrados:
                    ui.label('Nenhum aluno encontrado.').classes('text-gray-400 italic')
                for i, a in enumerate(alunos):
                    if termo and termo not in a.get('nome', '').lower():
                        continue
                    with ui.card().classes('w-full p-4 rounded-xl shadow-sm flex flex-row items-center justify-between'):
                        with ui.row().classes('items-center gap-4'):
                            turma = a.get('turma', 'S/T') or 'S/T'
                            ui.label(turma).classes('bg-blue-100 text-primary font-bold px-4 py-2 rounded-lg text-sm text-center min-w-[3rem]')
                            with ui.column().classes('gap-0'):
                                ui.label(a.get('nome', 'Sem nome')).classes('font-bold text-lg text-gray-800 dark:text-gray-100')
                                ui.label(f"Idade: {a.get('idade', '-')} anos").classes('text-sm text-gray-500')
                        with ui.row().classes('gap-2 items-center'):
                            ui.button('Prontuário', icon='folder_open', on_click=lambda i=i, a=a: abrir_modal(a, i)).props('flat color=primary size=sm no-caps')
                            ui.button(icon='delete', on_click=lambda a=a: confirmar_exclusao(a)).props('flat color=red round').tooltip('Remover')

        pesquisa_input.on_value_change(atualizar_lista)
        atualizar_lista()