from nicegui import app, ui

from database import load_data
from layout import frame


def _to_float(value):
    try:
        return float(str(value).replace(',', '.'))
    except (TypeError, ValueError):
        return 0.0


def render():
    with frame('Dashboard'):
        alunos_data = load_data('alunos.json', [])
        pais_data = load_data('pais.json', [])
        comunicados_data = load_data('comunicados.json', [])
        registros_data = load_data('registros.json', [])
        estrategias_data = load_data('estrategias.json', [])
        cargo_usuario = app.storage.user.get('cargo', 'Professor')
        pode_gerir = cargo_usuario in ['Administrador', 'Coordenador']

        total_alunos = len(alunos_data)
        total_pais = len(pais_data)
        total_registros = len(registros_data)
        total_estrategias = len(estrategias_data)
        total_com_atencao = sum(1 for aluno in alunos_data if aluno.get('diagnostico') or aluno.get('necessidades'))

        ui.add_css('''
            .dashboard-focus {
                background: var(--app-happy) !important;
            }

            .dashboard-shortcut {
                min-height: 124px;
                cursor: pointer;
                transition: transform 160ms ease, border-color 160ms ease;
            }

            .dashboard-summary {
                width: 8.75rem;
                height: 5.35rem;
            }

            .dashboard-shortcut:hover {
                transform: translateY(-2px);
                border-color: var(--app-primary);
            }

            .shortcut-icon {
                width: 2.25rem;
                height: 2.25rem;
                border-radius: 8px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 1.05rem;
            }

            .shortcut-value {
                background: var(--app-surface-muted);
                border: 1px solid var(--app-border);
                border-radius: 999px;
                font-size: 0.78rem;
                font-weight: 900;
                line-height: 1;
                padding: 0.38rem 0.58rem;
            }

            .summary-number {
                color: var(--app-text) !important;
                font-size: 1.55rem;
                line-height: 1;
                font-weight: 900;
            }

            .summary-title {
                color: var(--app-muted) !important;
                font-size: 0.68rem;
                font-weight: 900;
                line-height: 1.15;
                text-transform: uppercase;
            }
        ''')

        with ui.card().classes('app-card-colorful dashboard-focus w-full p-6'):
            with ui.row().classes('w-full justify-between items-start gap-5 mb-4'):
                with ui.column().classes('gap-1'):
                    ui.label('📣 Comunicados internos').classes('text-2xl font-black')
                    ui.label('Avisos importantes da escola para toda a equipe.').classes('app-muted text-sm')
                if pode_gerir:
                    ui.button('Publicar comunicado', icon='campaign', on_click=lambda: ui.navigate.to('/admin')).props('unelevated color=primary')

            if not comunicados_data:
                with ui.column().classes('w-full items-center justify-center gap-3 py-10 text-center'):
                    ui.label('📭').classes('text-5xl')
                    ui.label('Nenhum comunicado no momento').classes('text-lg font-black')
                    ui.label('Quando a coordenação publicar avisos, eles aparecerão em destaque aqui.').classes('app-muted text-sm')
            else:
                with ui.column().classes('w-full gap-3'):
                    for comunicado in reversed(comunicados_data[-3:]):
                        with ui.row().classes('w-full gap-3 p-4 rounded-lg soft-blue'):
                            ui.label('📌').classes('text-2xl')
                            with ui.column().classes('gap-1 flex-1'):
                                ui.label(comunicado.get('titulo', 'Sem título')).classes('font-black text-lg')
                                ui.label(f"{comunicado.get('data', '')} · {comunicado.get('autor', '')}").classes('app-muted text-xs font-bold')
                                ui.label(comunicado.get('mensagem', '')).classes('app-muted text-sm leading-relaxed')

        with ui.column().classes('w-full gap-3'):
            ui.label('Resumo da escola').classes('text-xl font-black')
            ui.label('Números principais para leitura rápida da rotina.').classes('app-muted text-sm')

            with ui.row().classes('w-full gap-4 flex-wrap'):
                def resumo(titulo, valor, emoji, cor):
                    with ui.card().classes('app-card dashboard-summary p-3'):
                        with ui.column().classes('w-full h-full justify-between gap-2'):
                            ui.label(titulo).classes('summary-title')
                            with ui.row().classes('w-full items-end justify-between gap-2'):
                                ui.label(valor).classes('summary-number')
                                ui.label(emoji).classes(f'shortcut-icon {cor}')

                resumo('Alunos', str(total_alunos), '☀️', 'soft-blue')
                resumo('Famílias', str(total_pais), '☎️', 'soft-teal')
                resumo('Registros', str(total_registros), '📝', 'soft-coral')
                resumo('Atenção registrada', str(total_com_atencao), '💛', 'soft-amber')
                resumo('Estratégias', str(total_estrategias), '💡', 'soft-violet')

        with ui.column().classes('w-full gap-3'):
            ui.label('Atalhos do sistema').classes('text-xl font-black')
            ui.label('Clique em um card para abrir a área correspondente.').classes('app-muted text-sm')

            with ui.grid(columns=1).classes('w-full gap-5 lg:grid-cols-2'):
                with ui.card().classes('app-card w-full p-5'):
                    ui.label('☎️ Comunicação com famílias').classes('text-xl font-black mb-2')
                    ui.label('Mantenha contatos de pais e responsáveis sempre à mão para recados, combinados e acolhimento.').classes('app-muted text-sm leading-relaxed mb-4')
                    ui.button('Abrir página de pais', icon='contact_phone', on_click=lambda: ui.navigate.to('/pais')).props('unelevated color=secondary')

            with ui.grid(columns=1).classes('w-full gap-4 md:grid-cols-2 lg:grid-cols-3'):
                def atalho(titulo, descricao, valor, emoji, cor, rota):
                    card = ui.card().classes('app-card dashboard-shortcut w-full p-4')
                    card.on('click', lambda r=rota: ui.navigate.to(r))
                    with card:
                        with ui.column().classes('w-full h-full justify-between gap-4'):
                            with ui.row().classes('w-full items-center justify-between gap-3'):
                                ui.label(emoji).classes(f'shortcut-icon {cor}')
                                ui.label(valor).classes('shortcut-value')
                            with ui.column().classes('gap-1'):
                                ui.label(titulo).classes('text-lg font-black leading-tight')
                                ui.label(descricao).classes('app-muted text-xs leading-relaxed')
                            with ui.row().classes('w-full justify-end'):
                                ui.icon('arrow_forward', size='xs').classes('app-muted')

                atalho('Alunos', 'Cadastro e prontuários individuais.', str(total_alunos), '☀️', 'soft-blue', '/alunos')
                atalho('Famílias', 'Contatos rápidos dos responsáveis.', str(total_pais), '☎️', 'soft-teal', '/pais')
                atalho('Registros', 'Diário de acompanhamento escolar.', str(total_registros), '📝', 'soft-coral', '/registros')
                atalho('Acompanhamento', 'Alunos com atenção registrada.', str(total_com_atencao), '💛', 'soft-amber', '/alunos')
                atalho('Estratégias', 'Biblioteca de apoio pedagógico.', str(total_estrategias), '💡', 'soft-violet', '/estrategias')
                if pode_gerir:
                    atalho('Administração', 'Comunicados e registros internos.', 'Gestão', '📣', 'soft-green', '/admin')

        with ui.grid(columns=1).classes('w-full gap-5 lg:grid-cols-2'):
            with ui.card().classes('app-card w-full p-5'):
                ui.label('💡 Estratégias pedagógicas').classes('text-xl font-black mb-2')
                ui.label('Consulte orientações práticas para rotina, comunicação, sensibilidade sensorial e reforço positivo.').classes('app-muted text-sm leading-relaxed mb-4')
                ui.button('Abrir estratégias', icon='auto_awesome', on_click=lambda: ui.navigate.to('/estrategias')).props('unelevated color=primary')
