from nicegui import app, ui


ROLE_PERMISSIONS = {
    'Administrador': {
        'view_dashboard',
        'view_agenda',
        'manage_agenda',
        'view_alunos',
        'manage_alunos',
        'view_turmas',
        'manage_turmas',
        'view_pais',
        'manage_pais',
        'view_registros',
        'manage_registros',
        'view_relatorios',
        'view_impressao',
        'view_estrategias',
        'manage_estrategias',
        'view_admin',
        'manage_comunicados',
        'manage_despesas',
        'manage_backup',
        'manage_lgpd',
        'manage_users',
        'view_config',
    },
    'Coordenador': {
        'view_dashboard',
        'view_agenda',
        'manage_agenda',
        'view_alunos',
        'manage_alunos',
        'view_turmas',
        'manage_turmas',
        'view_pais',
        'manage_pais',
        'view_registros',
        'manage_registros',
        'view_relatorios',
        'view_impressao',
        'view_estrategias',
        'manage_estrategias',
        'view_admin',
        'manage_comunicados',
        'view_config',
    },
    'Professor': {
        'view_dashboard',
        'view_agenda',
        'manage_agenda',
        'view_alunos',
        'view_registros',
        'manage_registros',
        'view_impressao',
        'view_estrategias',
        'view_config',
    },
    'Assistente': {
        'view_dashboard',
        'view_agenda',
        'view_registros',
        'manage_registros',
        'view_estrategias',
        'view_config',
    },
}


PERMISSION_LABELS = {
    'view_dashboard': 'Dashboard',
    'view_agenda': 'Agenda',
    'manage_agenda': 'Criar e editar agenda',
    'view_alunos': 'Alunos e prontuários',
    'manage_alunos': 'Criar, editar e excluir alunos',
    'view_turmas': 'Turmas',
    'manage_turmas': 'Criar, editar e excluir turmas',
    'view_pais': 'Pais e responsáveis',
    'manage_pais': 'Criar, editar e excluir contatos familiares',
    'view_registros': 'Registros de acompanhamento',
    'manage_registros': 'Criar e editar registros',
    'view_relatorios': 'Relatórios',
    'view_impressao': 'Impressão/PDF',
    'view_estrategias': 'Biblioteca de estratégias',
    'manage_estrategias': 'Criar, editar e excluir estratégias',
    'view_admin': 'Painel de administração',
    'manage_comunicados': 'Publicar comunicados',
    'manage_despesas': 'Gerenciar despesas',
    'manage_backup': 'Baixar e restaurar backup',
    'manage_lgpd': 'Controles LGPD',
    'manage_users': 'Gerenciar usuários e cargos',
    'view_config': 'Preferências pessoais',
}


def cargo_atual() -> str:
    return app.storage.user.get('cargo', '') if app.storage.user.get('nome') else ''


def permissoes_do_cargo(cargo: str | None = None) -> set[str]:
    if cargo is None and not app.storage.user.get('nome'):
        return set()
    return ROLE_PERMISSIONS.get(cargo or cargo_atual(), ROLE_PERMISSIONS['Professor'])


def has_permission(permission: str) -> bool:
    return permission in permissoes_do_cargo()


def require_permission(permission: str, *, title='Acesso restrito', description=None) -> bool:
    if has_permission(permission):
        return True

    ui.add_css('''
        .security-denied {
            background: var(--app-surface) !important;
            border: 1px solid var(--app-border);
            border-radius: 8px;
            box-shadow: var(--app-soft-shadow);
        }
    ''')
    with ui.column().classes('security-denied w-full items-center justify-center gap-3 py-16 px-6 text-center'):
        ui.icon('lock', size='4rem').classes('app-muted')
        ui.label(title).classes('text-2xl font-black')
        ui.label(description or 'Seu cargo não possui permissão para acessar esta área.').classes('app-muted text-sm')
        ui.button('Voltar ao dashboard', icon='arrow_back', on_click=lambda: ui.navigate.to('/')).props('unelevated color=primary no-caps')
    return False
