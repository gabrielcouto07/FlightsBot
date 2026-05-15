# Deploy do backend na Vercel

Este projeto usa o Streamlit Community Cloud apenas para o painel. O backend FastAPI deve ser publicado em um projeto separado na Vercel.

## Resumo

- Repositorio: o mesmo `flight-bot`
- Projeto Vercel: novo projeto separado
- Root Directory: raiz do repositorio
- Entrypoint: `app/main.py`
- Install Command: `pip install -r requirements-vercel.txt`

## O que esta pronto no codigo

- [vercel.json](./vercel.json) roteia todas as requisicoes para `app/main.py`
- [requirements-vercel.txt](./requirements-vercel.txt) contem apenas as dependencias necessarias para o backend serverless
- [.python-version](./.python-version) fixa Python `3.12`, que e compativel com esse stack na Vercel

## Criar o projeto na Vercel

1. No dashboard da Vercel, clique em **Add New > Project**.
2. Importe o mesmo repositorio GitHub usado pelo Streamlit.
3. Crie um projeto novo, separado do frontend e separado do Streamlit.
4. Em **Root Directory**, use a raiz do projeto `flight-bot`.
5. Em **Framework Preset**, deixe `Other`.
6. Em **Install Command**, configure:

```bash
pip install -r requirements-vercel.txt
```

7. Mantenha o `vercel.json` do repositorio ativo.

## Variaveis de ambiente recomendadas

Para um deploy de demo funcional:

```text
DATABASE_URL=sqlite+aiosqlite:////tmp/flight_bot.db
DEMO_MODE=true
WHATSAPP_ENABLED=false
LOG_LEVEL=INFO
```

Se quiser ativar busca real:

```text
KIWI_API_KEY=seu_token
```

## Limites importantes

- O arquivo SQLite em `/tmp` e efemero na Vercel. Serve para demo, nao para persistencia real.
- O scheduler em ambiente serverless nao e ideal para jobs longos ou estado persistente.
- Se voce precisar de agendamento confiavel, use Vercel Cron Jobs ou mova o backend para Render/Railway.

## Testes apos o deploy

Depois do primeiro deploy, valide:

```text
https://seu-backend.vercel.app/health
https://seu-backend.vercel.app/
https://seu-backend.vercel.app/api/search/airports
```

## Conectar no Streamlit

No Streamlit Cloud, abra **Manage app > Settings > Secrets** e adicione:

```toml
BACKEND_BASE_URL = "https://seu-backend.vercel.app"
REQUEST_TIMEOUT_SECONDS = 15
```
