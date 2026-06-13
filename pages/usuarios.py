from nicegui import ui
from layout import frame
from database import load_data, save_data
import datetime

def render():
    with frame('Gestão de Usuários'):
        usuarios = load_data('usuarios.json', [])
        
        editing_index = {'value': -1}

        def abrir_modal(user=None, index=-1):
            editing_index['value'] = index
            if user:
                nome_input.value = user.get('nome', '')
                email_input.value = user.get('email', '')
                senha_input.value = user.get('senha', '')
                cargo_input.value = user.get('cargo', 'Professor')
                dialog_title.set_text('Editar Usuário')
            else:
                nome_input.value = ''
                email_input.value = ''
                senha_input.value = ''
                cargo_input.value = 'Professor'
                dialog_title.set_text('Novo Usuário')
            dialog.open()

        def salvar_usuario():
            if not nome_input.value or not email_input.value or not senha_input.value:
                ui.notify('Preencha nome, e-mail e senha.', type='warning')
                return
                
            dados = {
                'nome': nome_input.value,
                'email': email_input.value,
                'senha': senha_input.value,
                'cargo': cargo_input.value,
                'data_criacao': datetime.datetime.now().strftime("%d/%m/%Y")
            }
            
            if editing_index['value'] >= 0:
                dados['data_criacao'] = usuarios[editing_index['value']].get('data_criacao', dados['data_criacao'])
                usuarios[editing_index['value']] = dados
                ui.notify('Usuário atualizado com sucesso!', type='positive')
            else:
                usuarios.append(dados)
                ui.notify('Usuário criado com sucesso!', type='positive')
                
            save_data('usuarios.json', usuarios)
            dialog.close()
            atualizar_lista()

        def confirmar_exclusao(user):
            with ui.dialog() as confirm_dialog, ui.card().classes('p-6 rounded-2xl'):
                ui.label('Confirmar Exclusão').classes('text-xl font-bold text-red-600 mb-4')
                ui.label(f'Tem certeza que deseja apagar o usuário "{user["nome"]}"?')
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Apagar', on_click=lambda: apagar_usuario(user, confirm_dialog)).props('unelevated color=red rounded')
            confirm_dialog.open()

        def apagar_usuario(user, confirm_dialog):
            usuarios.remove(user)
            save_data('usuarios.json', usuarios)
            ui.notify('Usuário removido.', type='warning')
            confirm_dialog.close()
            atualizar_lista()

        with ui.dialog() as dialog, ui.card().classes('w-full max-w-md p-6 rounded-2xl'):
            dialog_title = ui.label('Novo Usuário').classes('text-2xl font-bold mb-4')
            nome_input = ui.input('Nome Completo *').classes('w-full mb-2')
            email_input = ui.input('E-mail *').classes('w-full mb-2')
            senha_input = ui.input('Senha *').props('type=password').classes('w-full mb-2')
            cargo_input = ui.select(['Administrador', 'Coordenador', 'Professor', 'Assistente'], label='Cargo *').classes('w-full mb-4')
            with ui.row().classes('w-full justify-end gap-2 mt-4 pt-4 border-t'):
                ui.button('Cancelar', on_click=dialog.close).props('flat')
                ui.button('Salvar', on_click=salvar_usuario).props('unelevated color=primary rounded')

        with ui.row().classes('w-full justify-between items-center mb-6'):
            pesquisa_input = ui.input('Pesquisar usuário...').classes('w-full md:w-1/3')
            with pesquisa_input.add_slot('prepend'):
                ui.icon('search')
            ui.button('Novo Usuário', icon='person_add', on_click=lambda: abrir_modal()).props('unelevated color=primary rounded-xl')

        container_lista = ui.column().classes('w-full gap-4')

        def atualizar_lista():
            container_lista.clear()
            termo = pesquisa_input.value.lower() if pesquisa_input.value else ''
            with container_lista:
                filtrados = [u for u in usuarios if termo in u.get('nome', '').lower() or termo in u.get('email', '').lower() or termo in u.get('cargo', '').lower()]
                if not filtrados:
                    ui.label('Nenhum usuário encontrado.').classes('text-gray-400 italic w-full mt-4')
                for i, u in enumerate(usuarios):
                    if termo and termo not in u.get('nome', '').lower() and termo not in u.get('email', '').lower() and termo not in u.get('cargo', '').lower():
                        continue
                    with ui.card().classes('w-full p-4 rounded-xl shadow-sm flex-row items-center justify-between'):
                        with ui.row().classes('items-center gap-4'):
                            primeira_letra = u.get('nome', 'U')[0].upper()
                            ui.avatar(primeira_letra).classes('bg-primary text-white font-bold w-12 h-12')
                            with ui.column().classes('gap-0'):
                                ui.label(u.get('nome', 'Sem nome')).classes('font-bold text-lg text-gray-800 dark:text-gray-100')
                                ui.label(u.get('email', '')).classes('text-sm text-gray-500')
                        with ui.row().classes('items-center gap-6'):
                            cargo = u.get('cargo', 'Professor')
                            cor_badge = 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300'
                            if cargo == 'Administrador': cor_badge = 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                            elif cargo == 'Coordenador': cor_badge = 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300'
                            elif cargo == 'Professor': cor_badge = 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                            ui.label(cargo).classes(f'text-xs font-bold px-3 py-1 rounded-full {cor_badge} hidden sm:block')
                            with ui.row().classes('gap-2'):
                                ui.button(icon='edit', on_click=lambda i=i, u=u: abrir_modal(u, i)).props('flat color=primary round size=sm').tooltip('Editar')
                                ui.button(icon='delete', on_click=lambda u=u: confirmar_exclusao(u)).props('flat color=red round size=sm').tooltip('Remover')

        pesquisa_input.on_value_change(atualizar_lista)
        atualizar_lista()