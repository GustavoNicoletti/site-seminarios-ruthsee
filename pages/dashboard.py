from nicegui import ui
from layout import frame
from database import load_data

def render():
    with frame('Dashboard'):
        # Carrega os dados de todos os arquivos JSON
        alunos_data = load_data('alunos.json', [])
        despesas_data = load_data('despesas.json', [])
        comunicados_data = load_data('comunicados.json', [])
        estrategias_data = load_data('estrategias.json', [])
        
        # Calcula os totais
        total_alunos = len(alunos_data)
        total_despesas = sum(float(d.get('valor', 0)) for d in despesas_data)
        total_estrategias = len(estrategias_data)

        # Cards de Indicadores
        with ui.row().classes('w-full gap-6 mb-8 flex-wrap md:flex-nowrap'):
            with ui.card().classes('flex-1 min-w-[200px] items-center p-6 rounded-2xl shadow-sm border-l-4 border-primary'):
                ui.icon('groups').classes('text-4xl text-primary mb-2')
                ui.label(str(total_alunos)).classes('text-3xl font-bold')
                ui.label('Alunos Cadastrados').classes('text-gray-500 text-center')
                
            with ui.card().classes('flex-1 min-w-[200px] items-center p-6 rounded-2xl shadow-sm border-l-4 border-secondary'):
                ui.icon('account_balance_wallet').classes('text-4xl text-secondary mb-2')
                ui.label(f'R$ {total_despesas:.2f}').classes('text-3xl font-bold')
                ui.label('Despesas Registradas').classes('text-gray-500 text-center')
                
            with ui.card().classes('flex-1 min-w-[200px] items-center p-6 rounded-2xl shadow-sm border-l-4 border-accent'):
                ui.icon('psychology').classes('text-4xl text-accent mb-2')
                ui.label(str(total_estrategias)).classes('text-3xl font-bold')
                ui.label('Estratégias na Biblioteca').classes('text-gray-500 text-center')

        # Seção de Comunicados
        ui.label('Comunicados Internos').classes('text-xl font-bold mb-4')
        
        if not comunicados_data:
            ui.label('Nenhum comunicado no momento.').classes('text-gray-500 italic')
        else:
            with ui.grid(columns=1).classes('w-full gap-4 md:grid-cols-2'):
                for c in comunicados_data:
                    with ui.card().classes('w-full p-6 rounded-2xl shadow-sm bg-blue-50 dark:bg-slate-800 border-l-4 border-blue-400'):
                        with ui.row().classes('w-full justify-between items-center mb-2'):
                            ui.label(c.get('titulo', '')).classes('font-bold text-lg text-blue-800 dark:text-blue-300')
                            ui.label(c.get('data', '')).classes('text-xs text-gray-500')
                        ui.label(c.get('mensagem', '')).classes('text-gray-700 dark:text-gray-300')