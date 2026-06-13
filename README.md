# Ruth See Escola

Aplicação em NiceGUI para gerenciar alunos, estratégias pedagógicas, usuários, comunicados e despesas.

## Como rodar

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

Acesse `http://localhost:8080`.

Se a porta `8080` já estiver ocupada, informe outra porta:

```powershell
python main.py 8090
```

Nesse caso, acesse `http://localhost:8090`.

## Login inicial

Por padrão, o administrador local é:

- E-mail: `admin@adaptaescola.com`
- Senha: `admin123`

Para trocar sem editar código, configure as variáveis de ambiente:

```powershell
$env:ADAPTAESCOLA_ADMIN_EMAIL = 'seu-email@exemplo.com'
$env:ADAPTAESCOLA_ADMIN_PASSWORD = 'uma-senha-forte'
$env:ADAPTAESCOLA_STORAGE_SECRET = 'um-segredo-longo-e-aleatorio'
python main.py
```

Os dados da aplicação ficam em arquivos JSON dentro da pasta `data/`.

