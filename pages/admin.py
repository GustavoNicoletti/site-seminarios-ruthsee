import datetime

from nicegui import app, ui

from database import load_data, save_data
from layout import frame


def _valor_filtro(valor, padrao='Todos'):
    if isinstance(valor, dict):
        return str(valor.get('label') or valor.get('value') or padrao)
    return str(valor or padrao)


def _opcoes_autores(items):
    autores = {item.get('autor', '').strip() for item in items if item.get('autor', '').strip()}
    return ['Todos'] + sorted(autores)


def _opcoes_datas(items):
    datas = {item.get('data', '').strip() for item in items if item.get('data', '').strip()}
    return ['Todas'] + sorted(datas, reverse=True)


def render():
    with frame('Administração do Sistema'):
        if app.storage.user.get('cargo') not in ['Administrador', 'Coordenador']:
            with ui.column().classes('app-card w-full items-center justify-center gap-3 py-16 text-center'):
                ui.icon('lock', size='4rem').classes('app-muted')
                ui.label('Acesso restrito').classes('text-2xl font-black')
                ui.label('Esta área é reservada para administração e coordenação.').classes('app-muted text-sm')
                ui.button('Voltar ao dashboard', icon='arrow_back', on_click=lambda: ui.navigate.to('/')).props('unelevated color=primary')
            return

        comunicados = load_data('comunicados.json', [])
        despesas = load_data('despesas.json', [])

        def salvar_comunicado():
            if not titulo_input.value or not mensagem_input.value:
                ui.notify('Preencha o título e a mensagem. 😊', type='warning')
                return

            novo_aviso = {
                'titulo': titulo_input.value.strip(),
                'mensagem': mensagem_input.value.strip(),
                'data': datetime.datetime.now().strftime('%d/%m/%Y'),
                'autor': app.storage.user.get('nome', 'Administração').split(' ')[0],
            }

            comunicados.append(novo_aviso)
            save_data('comunicados.json', comunicados)
            ui.notify('Comunicado publicado com sucesso! 📣', type='positive')

            titulo_input.value = ''
            mensagem_input.value = ''
            atualizar_opcoes_comunicados()
            atualizar_lista_comunicados()

        def confirmar_exclusao_comunicado(aviso):
            with ui.dialog() as confirm_dialog, ui.card().classes('app-card w-full max-w-md p-6'):
                ui.label('Excluir comunicado').classes('text-xl font-black text-red-600 mb-3')
                ui.label(f'Deseja apagar "{aviso["titulo"]}"?').classes('app-muted text-sm')
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Excluir', icon='delete', on_click=lambda: apagar_comunicado(aviso, confirm_dialog)).props('unelevated color=red')
            confirm_dialog.open()

        def apagar_comunicado(aviso, confirm_dialog):
            comunicados.remove(aviso)
            save_data('comunicados.json', comunicados)
            ui.notify('Comunicado removido.', type='warning')
            confirm_dialog.close()
            atualizar_opcoes_comunicados()
            atualizar_lista_comunicados()

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
                'descricao': desc_despesa_input.value.strip(),
                'valor': valor_float,
                'data': datetime.datetime.now().strftime('%d/%m/%Y'),
                'autor': app.storage.user.get('nome', 'Administração').split(' ')[0],
            }

            despesas.append(nova_despesa)
            save_data('despesas.json', despesas)
            ui.notify('Despesa registrada com sucesso! 💰', type='positive')

            desc_despesa_input.value = ''
            valor_despesa_input.value = ''
            atualizar_opcoes_despesas()
            atualizar_lista_despesas()

        def confirmar_exclusao_despesa(despesa):
            with ui.dialog() as confirm_dialog, ui.card().classes('app-card w-full max-w-md p-6'):
                ui.label('Excluir despesa').classes('text-xl font-black text-red-600 mb-3')
                ui.label(f'Deseja apagar "{despesa["descricao"]}"?').classes('app-muted text-sm')
                with ui.row().classes('w-full justify-end gap-2 mt-4'):
                    ui.button('Cancelar', on_click=confirm_dialog.close).props('flat')
                    ui.button('Excluir', icon='delete', on_click=lambda: apagar_despesa(despesa, confirm_dialog)).props('unelevated color=red')
            confirm_dialog.open()

        def apagar_despesa(despesa, confirm_dialog):
            despesas.remove(despesa)
            save_data('despesas.json', despesas)
            ui.notify('Despesa removida.', type='warning')
            confirm_dialog.close()
            atualizar_opcoes_despesas()
            atualizar_lista_despesas()

        with ui.column().classes('w-full gap-5'):
            with ui.row().classes('app-card-colorful w-full items-center justify-between gap-5 p-6'):
                with ui.column().classes('gap-2'):
                    ui.label('📣 Coordenação').classes('app-muted text-sm font-black uppercase')
                    ui.label('Avisos e organização da escola').classes('text-3xl font-black')
                    ui.label('Publique comunicados e acompanhe registros financeiros simples.').classes('app-muted text-sm')
                ui.label('🧭').classes('text-5xl')

            with ui.tabs().classes('w-full') as tabs:
                tab_comunicados = ui.tab('📣 Comunicados', icon='campaign')
                tab_despesas = ui.tab('💰 Despesas', icon='account_balance_wallet')

            with ui.tab_panels(tabs, value=tab_comunicados).classes('w-full bg-transparent p-0'):
                with ui.tab_panel(tab_comunicados).classes('p-0'):
                    with ui.card().classes('app-card w-full p-5 mb-5'):
                        ui.label('📌 Publicar novo comunicado').classes('text-xl font-black mb-4')
                        titulo_input = ui.input('Título do comunicado *').props('outlined').classes('w-full mb-4')
                        mensagem_input = ui.textarea('Mensagem *').props('outlined autogrow').classes('w-full mb-4')
                        with ui.row().classes('w-full justify-end'):
                            ui.button('Publicar comunicado ✨', icon='send', on_click=salvar_comunicado).props('unelevated color=primary')

                    ui.label('Comunicados ativos').classes('text-xl font-black mb-3')
                    with ui.row().classes('app-toolbar w-full justify-between items-center gap-4 p-4 mb-4'):
                        with ui.row().classes('flex-1 items-center gap-3 flex-wrap'):
                            busca_comunicado_input = ui.input(placeholder='Buscar por título, mensagem ou autor').props('outlined dense').classes('w-full md:max-w-md flex-1')
                            with busca_comunicado_input.add_slot('prepend'):
                                ui.icon('search').classes('app-muted')
                            autor_comunicado_filter = ui.select(_opcoes_autores(comunicados), value='Todos', label='Autor').props('outlined dense').classes('w-full sm:w-48')
                            data_comunicado_filter = ui.select(_opcoes_datas(comunicados), value='Todas', label='Data').props('outlined dense').classes('w-full sm:w-40')

                    container_comunicados = ui.column().classes('w-full gap-3')

                    def atualizar_opcoes_comunicados():
                        filtros = [
                            (autor_comunicado_filter, _opcoes_autores(comunicados), 'Todos'),
                            (data_comunicado_filter, _opcoes_datas(comunicados), 'Todas'),
                        ]
                        for filtro, opcoes, padrao in filtros:
                            valor_atual = _valor_filtro(filtro.value, padrao)
                            filtro.options = opcoes
                            filtro.value = valor_atual if valor_atual in opcoes else padrao
                            filtro.update()

                    def atualizar_lista_comunicados():
                        termo = (busca_comunicado_input.value or '').strip().lower()
                        autor_selecionado = _valor_filtro(autor_comunicado_filter.value)
                        data_selecionada = _valor_filtro(data_comunicado_filter.value, 'Todas')
                        filtrados = []

                        for comunicado in comunicados:
                            texto_busca = ' '.join([
                                comunicado.get('titulo', ''),
                                comunicado.get('mensagem', ''),
                                comunicado.get('autor', ''),
                                comunicado.get('data', ''),
                            ]).lower()
                            if termo and termo not in texto_busca:
                                continue
                            if autor_selecionado != 'Todos' and comunicado.get('autor') != autor_selecionado:
                                continue
                            if data_selecionada != 'Todas' and comunicado.get('data') != data_selecionada:
                                continue
                            filtrados.append(comunicado)

                        container_comunicados.clear()
                        with container_comunicados:
                            if not filtrados:
                                with ui.column().classes('app-card w-full items-center justify-center gap-3 py-12 text-center'):
                                    ui.label('📭').classes('text-5xl')
                                    ui.label('Nenhum comunicado encontrado').classes('text-xl font-black')
                                    ui.label('Ajuste os filtros ou publique um novo aviso.').classes('app-muted text-sm')

                            for comunicado in reversed(filtrados):
                                with ui.card().classes('app-card w-full p-4'):
                                    with ui.row().classes('w-full justify-between items-start gap-4'):
                                        with ui.column().classes('gap-1 flex-1'):
                                            ui.label(comunicado.get('titulo', '')).classes('font-black text-lg')
                                            ui.label(f"Publicado em {comunicado.get('data', '')} por {comunicado.get('autor', '')}").classes('app-muted text-xs font-bold')
                                            ui.label(comunicado.get('mensagem', '')).classes('app-muted text-sm leading-relaxed mt-2')
                                        ui.button(icon='delete', on_click=lambda c=comunicado: confirmar_exclusao_comunicado(c)).props('flat color=red round size=sm').tooltip('Remover')

                    busca_comunicado_input.on_value_change(lambda _: atualizar_lista_comunicados())
                    autor_comunicado_filter.on_value_change(lambda _: atualizar_lista_comunicados())
                    data_comunicado_filter.on_value_change(lambda _: atualizar_lista_comunicados())
                    atualizar_lista_comunicados()

                with ui.tab_panel(tab_despesas).classes('p-0'):
                    with ui.card().classes('app-card w-full p-5 mb-5'):
                        ui.label('💰 Registrar nova despesa').classes('text-xl font-black mb-4')
                        with ui.grid(columns=2).classes('w-full gap-4'):
                            desc_despesa_input = ui.input('Descrição da despesa *').props('outlined').classes('w-full')
                            valor_despesa_input = ui.input('Valor (R$) *').props('outlined type=number step=0.01').classes('w-full')
                        with ui.row().classes('w-full justify-end mt-4'):
                            ui.button('Registrar despesa ✨', icon='add_circle', on_click=salvar_despesa).props('unelevated color=positive')

                    ui.label('Histórico de despesas').classes('text-xl font-black mb-3')
                    with ui.row().classes('app-toolbar w-full justify-between items-center gap-4 p-4 mb-4'):
                        with ui.row().classes('flex-1 items-center gap-3 flex-wrap'):
                            busca_despesa_input = ui.input(placeholder='Buscar por descrição, autor ou data').props('outlined dense').classes('w-full md:max-w-md flex-1')
                            with busca_despesa_input.add_slot('prepend'):
                                ui.icon('search').classes('app-muted')
                            autor_despesa_filter = ui.select(_opcoes_autores(despesas), value='Todos', label='Autor').props('outlined dense').classes('w-full sm:w-48')
                            data_despesa_filter = ui.select(_opcoes_datas(despesas), value='Todas', label='Data').props('outlined dense').classes('w-full sm:w-40')
                            valor_despesa_filter = ui.select(['Todos', 'Até R$ 100', 'Acima de R$ 100', 'Acima de R$ 500'], value='Todos', label='Valor').props('outlined dense').classes('w-full sm:w-44')

                    container_despesas = ui.column().classes('w-full gap-3')

                    def atualizar_opcoes_despesas():
                        filtros = [
                            (autor_despesa_filter, _opcoes_autores(despesas), 'Todos'),
                            (data_despesa_filter, _opcoes_datas(despesas), 'Todas'),
                        ]
                        for filtro, opcoes, padrao in filtros:
                            valor_atual = _valor_filtro(filtro.value, padrao)
                            filtro.options = opcoes
                            filtro.value = valor_atual if valor_atual in opcoes else padrao
                            filtro.update()

                    def atualizar_lista_despesas():
                        termo = (busca_despesa_input.value or '').strip().lower()
                        autor_selecionado = _valor_filtro(autor_despesa_filter.value)
                        data_selecionada = _valor_filtro(data_despesa_filter.value, 'Todas')
                        valor_selecionado = _valor_filtro(valor_despesa_filter.value)
                        filtradas = []

                        for despesa in despesas:
                            texto_busca = ' '.join([
                                despesa.get('descricao', ''),
                                despesa.get('autor', ''),
                                despesa.get('data', ''),
                            ]).lower()
                            valor = float(despesa.get('valor', 0) or 0)

                            if termo and termo not in texto_busca:
                                continue
                            if autor_selecionado != 'Todos' and despesa.get('autor') != autor_selecionado:
                                continue
                            if data_selecionada != 'Todas' and despesa.get('data') != data_selecionada:
                                continue
                            if valor_selecionado == 'Até R$ 100' and valor > 100:
                                continue
                            if valor_selecionado == 'Acima de R$ 100' and valor <= 100:
                                continue
                            if valor_selecionado == 'Acima de R$ 500' and valor <= 500:
                                continue
                            filtradas.append(despesa)

                        container_despesas.clear()
                        with container_despesas:
                            if not filtradas:
                                with ui.column().classes('app-card w-full items-center justify-center gap-3 py-12 text-center'):
                                    ui.label('🧾').classes('text-5xl')
                                    ui.label('Nenhuma despesa encontrada').classes('text-xl font-black')
                                    ui.label('Ajuste os filtros ou registre uma nova despesa.').classes('app-muted text-sm')

                            for despesa in reversed(filtradas):
                                valor_formatado = f"R$ {float(despesa.get('valor', 0)):.2f}".replace('.', ',')
                                with ui.card().classes('app-card w-full p-4 flex-row justify-between items-center'):
                                    with ui.column().classes('gap-0'):
                                        ui.label(despesa.get('descricao', '')).classes('font-black text-lg')
                                        ui.label(f"Registrado em {despesa.get('data', '')} por {despesa.get('autor', '')}").classes('app-muted text-xs font-bold')

                                    with ui.row().classes('items-center gap-4'):
                                        ui.label(valor_formatado).classes('text-xl font-black tone-green')
                                        ui.button(icon='delete', on_click=lambda d=despesa: confirmar_exclusao_despesa(d)).props('flat color=red round size=sm').tooltip('Remover')

                    busca_despesa_input.on_value_change(lambda _: atualizar_lista_despesas())
                    autor_despesa_filter.on_value_change(lambda _: atualizar_lista_despesas())
                    data_despesa_filter.on_value_change(lambda _: atualizar_lista_despesas())
                    valor_despesa_filter.on_value_change(lambda _: atualizar_lista_despesas())
                    atualizar_lista_despesas()
