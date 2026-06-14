# Ruth See Escola

Aplicação em NiceGUI para gerenciar agenda diária, alunos, turmas, famílias, registros, estratégias pedagógicas, relatórios, impressões, usuários, comunicados, backups e despesas.

## Como rodar no computador

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

Se o `venv` já existir, normalmente basta ativar e rodar:

```powershell
.\venv\Scripts\Activate.ps1
python main.py
```

Se aparecer erro de "Acesso negado" apontando para Python da Microsoft Store, recrie o `venv` usando uma instalação normal do Python:

```powershell
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

## Ver no celular

Na mesma rede Wi-Fi do computador:

1. Deixe o sistema rodando no computador com `python main.py`.
2. No PowerShell, rode `ipconfig` e procure o "Endereço IPv4" da sua rede Wi-Fi.
3. No celular, abra `http://SEU-IP:8080`, por exemplo `http://192.168.0.25:8080`.

Se não abrir, permita o Python/NiceGUI no Firewall do Windows ou libere a porta usada.

Fora da mesma rede, `localhost` e o IP local não funcionam. Para acessar com segurança, prefira Tailscale, ZeroTier ou Cloudflare Tunnel. Evite abrir porta no roteador diretamente, porque o sistema guarda dados escolares.

## Login inicial

Por padrão, o administrador local é:

- Usuário: `gustavo`
- Senha: `123`

Para trocar sem editar código, configure as variáveis de ambiente:

```powershell
$env:ADAPTAESCOLA_ADMIN_USER = 'seu-usuario'
$env:ADAPTAESCOLA_ADMIN_PASSWORD = 'uma-senha-forte'
$env:ADAPTAESCOLA_STORAGE_SECRET = 'um-segredo-longo-e-aleatorio'
python main.py
```

Os dados da aplicação ficam no banco SQLite local `data/ruthsee.db`. Os arquivos JSON antigos da pasta `data/` são usados como base para a primeira migração quando o banco ainda não existe.

