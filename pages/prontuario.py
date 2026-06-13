from urllib.parse import quote

from nicegui import ui

from database import load_data
from layout import frame


def _texto(valor, padrao='Não informado'):
    valor = str(valor or '').strip()
    return valor if valor else padrao


def _telefone_limpo(valor):
    return ''.join(ch for ch in str(valor or '') if ch.isdigit())


def _normalizar(valor):
    return str(valor or '').strip().lower()


def _whatsapp_url(numero, aluno_nome):
    numero_limpo = _telefone_limpo(numero)
    if not numero_limpo:
        return ''
    numero_final = numero_limpo if numero_limpo.startswith('55') else f'55{numero_limpo}'
    mensagem = quote(f'Olá! Aqui é da Ruth See Escola. Gostaria de conversar sobre {aluno_nome}.')
    return f'https://wa.me/{numero_final}?text={mensagem}'


def _estrategias_sugeridas(aluno, estrategias):
    texto_aluno = _normalizar(' '.join([
        aluno.get('diagnostico', ''),
        aluno.get('necessidades', ''),
        aluno.get('observacoes', ''),
    ]))

    palavras_chave = {
        'sensorial': ['sensorial', 'sensibilidade', 'barulho', 'som', 'toque', 'luz'],
        'comunicação': ['comunicação', 'fala', 'linguagem', 'comunicar'],
        'rotina': ['rotina', 'previsibilidade', 'agenda', 'transição'],
        'crise': ['crise', 'manejo', 'sobrecarga', 'agitação'],
        'social': ['social', 'interação', 'grupo', 'colega'],
    }

    selecionadas = []
    for estrategia in estrategias:
        texto_estrategia = _normalizar(' '.join([
            estrategia.get('titulo', ''),
            estrategia.get('categoria', ''),
            estrategia.get('conteudo', ''),
            estrategia.get('desc', ''),
            estrategia.get('quando_usar', ''),
        ]))

        if any(
            any(palavra in texto_aluno for palavra in palavras)
            and any(palavra in texto_estrategia for palavra in palavras)
            for palavras in palavras_chave.values()
        ):
            selecionadas.append(estrategia)

    return selecionadas[:4] or estrategias[:4]


def render(aluno_index):
    with frame('Prontuário do Aluno'):
        alunos = load_data('alunos.json', [])
        responsaveis = load_data('pais.json', [])
        registros = load_data('registros.json', [])
        estrategias = load_data('estrategias.json', [])

        try:
            index = int(aluno_index)
        except (TypeError, ValueError):
            index = -1

        if index < 0 or index >= len(alunos):
            with ui.column().classes('app-card w-full items-center justify-center gap-3 py-16 text-center'):
                ui.label('🔎').classes('text-5xl')
                ui.label('Aluno não encontrado').classes('text-2xl font-black')
                ui.label('Volte para a lista de alunos e abra o prontuário novamente.').classes('app-muted text-sm')
                ui.button('Voltar para alunos', icon='arrow_back', on_click=lambda: ui.navigate.to('/alunos')).props('unelevated color=primary')
            return

        aluno = alunos[index]
        nome = _texto(aluno.get('nome'), 'Aluno')
        turma = _texto(aluno.get('turma'), 'Sem turma')
        nascimento = _texto(aluno.get('nascimento'))
        diagnostico = _texto(aluno.get('diagnostico'), 'Sem diagnóstico registrado')
        necessidades = _texto(aluno.get('necessidades'), 'Sem necessidades específicas registradas')
        observacoes = _texto(aluno.get('observacoes'), 'Sem observações cadastradas')
        inicial = nome[0].upper()

        responsaveis_aluno = [
            item for item in responsaveis
            if _normalizar(item.get('aluno')) == _normalizar(nome)
        ]
        estrategias_aluno = _estrategias_sugeridas(aluno, estrategias)
        registros_aluno = [
            item for item in registros
            if _normalizar(item.get('aluno')) == _normalizar(nome)
        ]

        ui.add_css('''
            .record-hero {
                background: var(--app-happy) !important;
            }

            .record-section {
                min-height: 100%;
            }

            .record-line {
                background: var(--app-surface-muted) !important;
                border-radius: 8px;
            }
        ''')

        with ui.column().classes('w-full gap-5'):
            with ui.row().classes('app-card-colorful record-hero w-full items-center justify-between gap-5 p-6'):
                with ui.row().classes('items-center gap-5 min-w-0'):
                    ui.avatar(inicial).classes('brand-badge text-white font-black w-20 h-20 text-3xl')
                    with ui.column().classes('gap-2 min-w-0'):
                        ui.label(nome).classes('text-4xl font-black leading-tight line-clamp-1')
                        with ui.row().classes('items-center gap-2 flex-wrap'):
                            ui.label(f'🏫 {turma}').classes('app-pill text-sm font-black px-3 py-1')
                            ui.label(f'📅 {nascimento}').classes('app-pill text-sm font-black px-3 py-1')
                            ui.label(f'👨‍👩‍👧 {len(responsaveis_aluno)} responsável(is)').classes('app-pill text-sm font-black px-3 py-1')

                with ui.row().classes('gap-2'):
                    ui.button('Voltar', icon='arrow_back', on_click=lambda: ui.navigate.to('/alunos')).props('flat color=primary')
                    ui.button('Editar aluno', icon='edit', on_click=lambda: ui.navigate.to('/alunos')).props('unelevated color=primary')

            with ui.grid(columns=1).classes('w-full gap-5 lg:grid-cols-3'):
                with ui.card().classes('app-card record-section w-full p-5 lg:col-span-2'):
                    ui.label('🧩 Perfil de acompanhamento').classes('text-xl font-black mb-4')
                    with ui.grid(columns=1).classes('w-full gap-3 md:grid-cols-2'):
                        with ui.column().classes('record-line gap-1 p-4'):
                            ui.label('Diagnóstico / condição').classes('app-muted text-xs font-black uppercase')
                            ui.label(diagnostico).classes('font-bold leading-relaxed')
                        with ui.column().classes('record-line gap-1 p-4'):
                            ui.label('Nascimento').classes('app-muted text-xs font-black uppercase')
                            ui.label(nascimento).classes('font-bold')
                    with ui.column().classes('record-line gap-2 p-4 mt-3'):
                        ui.label('Necessidades específicas').classes('app-muted text-xs font-black uppercase')
                        ui.label(necessidades).classes('app-muted text-sm leading-relaxed')
                    with ui.column().classes('record-line gap-2 p-4 mt-3'):
                        ui.label('Observações gerais').classes('app-muted text-xs font-black uppercase')
                        ui.label(observacoes).classes('app-muted text-sm leading-relaxed')

                with ui.card().classes('app-card record-section w-full p-5'):
                    ui.label('☎️ Família e contato').classes('text-xl font-black mb-4')
                    if not responsaveis_aluno:
                        with ui.column().classes('items-center text-center gap-3 py-8'):
                            ui.label('📭').classes('text-5xl')
                            ui.label('Nenhum responsável vinculado').classes('font-black')
                            ui.button('Cadastrar contato', icon='person_add', on_click=lambda: ui.navigate.to('/pais')).props('unelevated color=secondary')
                    else:
                        with ui.column().classes('w-full gap-3'):
                            for responsavel in responsaveis_aluno:
                                nome_resp = _texto(responsavel.get('nome'), 'Responsável')
                                parentesco = _texto(responsavel.get('parentesco'), 'Responsável')
                                telefone = _texto(responsavel.get('telefone'))
                                whatsapp = responsavel.get('whatsapp') or responsavel.get('telefone')
                                email = _texto(responsavel.get('email'))
                                whatsapp_url = _whatsapp_url(whatsapp, nome)

                                with ui.column().classes('record-line gap-2 p-4'):
                                    ui.label(f'{parentesco}: {nome_resp}').classes('font-black')
                                    ui.label(f'☎️ {telefone}').classes('app-muted text-sm')
                                    ui.label(f'✉️ {email}').classes('app-muted text-sm')
                                    with ui.row().classes('gap-2'):
                                        if whatsapp_url:
                                            ui.link('WhatsApp', whatsapp_url, new_tab=True).classes('q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle text-primary font-bold px-3 py-2')
                                        if responsavel.get('email'):
                                            ui.link('E-mail', f"mailto:{responsavel.get('email')}", new_tab=True).classes('q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle text-primary font-bold px-3 py-2')

            with ui.grid(columns=1).classes('w-full gap-5 lg:grid-cols-3'):
                with ui.card().classes('app-card w-full p-5'):
                    ui.label('💡 Estratégias úteis').classes('text-xl font-black mb-4')
                    if not estrategias_aluno:
                        ui.label('Nenhuma estratégia cadastrada ainda.').classes('app-muted text-sm')
                    else:
                        with ui.column().classes('w-full gap-3'):
                            for estrategia in estrategias_aluno:
                                titulo = _texto(estrategia.get('titulo'), 'Estratégia')
                                categoria = _texto(estrategia.get('categoria'), 'Geral')
                                conteudo = _texto(estrategia.get('conteudo') or estrategia.get('desc'), 'Sem descrição cadastrada.')
                                with ui.column().classes('record-line gap-2 p-4'):
                                    ui.label(categoria).classes('app-pill text-xs font-black px-3 py-1 w-fit')
                                    ui.label(titulo).classes('font-black')
                                    ui.label(conteudo).classes('app-muted text-sm leading-relaxed')

                with ui.card().classes('app-card w-full p-5'):
                    ui.label('📝 Registros recentes').classes('text-xl font-black mb-4')
                    if not registros_aluno:
                        with ui.column().classes('items-center text-center gap-3 py-8'):
                            ui.label('📝').classes('text-5xl')
                            ui.label('Nenhum registro ainda').classes('font-black')
                            ui.button('Criar registro', icon='note_add', on_click=lambda: ui.navigate.to('/registros')).props('unelevated color=primary')
                    else:
                        with ui.column().classes('w-full gap-3'):
                            for registro in reversed(registros_aluno[-3:]):
                                with ui.column().classes('record-line gap-2 p-4'):
                                    with ui.row().classes('items-center gap-2 flex-wrap'):
                                        ui.label(_texto(registro.get('tipo'), 'Registro')).classes('app-pill text-xs font-black px-3 py-1')
                                        ui.label(_texto(registro.get('intensidade'), 'Neutro')).classes('app-pill text-xs font-black px-3 py-1')
                                    ui.label(_texto(registro.get('descricao'), 'Sem descrição')).classes('app-muted text-sm leading-relaxed line-clamp-3')
                                    ui.label(f"{registro.get('data', '')} · {registro.get('autor', 'Equipe')}").classes('app-muted text-xs font-bold')

                with ui.card().classes('app-card w-full p-5'):
                    ui.label('📌 Ações rápidas').classes('text-xl font-black mb-4')
                    with ui.column().classes('w-full gap-3'):
                        ui.button('Ver todos os responsáveis', icon='contact_phone', on_click=lambda: ui.navigate.to('/pais')).classes('w-full justify-start').props('flat color=secondary no-caps')
                        ui.button('Abrir registros', icon='edit_note', on_click=lambda: ui.navigate.to('/registros')).classes('w-full justify-start').props('flat color=primary no-caps')
                        ui.button('Abrir biblioteca de estratégias', icon='auto_awesome', on_click=lambda: ui.navigate.to('/estrategias')).classes('w-full justify-start').props('flat color=primary no-caps')
                        ui.button('Voltar para lista de alunos', icon='groups', on_click=lambda: ui.navigate.to('/alunos')).classes('w-full justify-start').props('flat color=primary no-caps')
