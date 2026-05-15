# Deploy no Streamlit Community Cloud

Este repositório já está preparado para publicar o painel Streamlit no `share.streamlit.io`.

## O que será publicado

O Streamlit Community Cloud vai publicar somente a interface Streamlit.

O backend FastAPI precisa estar publicado separadamente e acessível por HTTPS, incluindo:

- `/health`
- `/api/routes`
- `/api/users`
- `/api/alerts`
- `/api/demo/notifications`
- `/api/search/deals`

## Arquivo de entrada

Use este arquivo como entrypoint:

```text
streamlit_app.py
```

## Python

Escolha Python `3.11` em **Advanced settings** no momento do deploy.

## Secrets

Cole este conteúdo em **Advanced settings > Secrets**:

```toml
BACKEND_BASE_URL = "https://seu-backend.exemplo.com"
REQUEST_TIMEOUT_SECONDS = 15
```

Se o backend já expõe `/api` no fim da URL, o app remove esse sufixo automaticamente.

## Passo a passo

1. Suba o projeto para o GitHub.
2. Acesse `https://share.streamlit.io/`.
3. Clique em **Create app**.
4. Escolha o repositório, branch e o arquivo `streamlit_app.py`.
5. Abra **Advanced settings**.
6. Selecione Python `3.11`.
7. Cole os secrets.
8. Clique em **Deploy**.

## Estrutura usada pelo Cloud

- `streamlit_app.py`: entrypoint do app
- `.streamlit/config.toml`: configuração global do Streamlit
- `.streamlit/secrets.toml.example`: modelo dos secrets
- `requirements.txt`: dependências Python

## Observações importantes

- O Streamlit Community Cloud executa o app a partir da raiz do repositório.
- O arquivo `.streamlit/config.toml` precisa ficar na raiz do projeto.
- Não comite `.streamlit/secrets.toml`.
- O app abre mesmo se o backend estiver offline, mas exibirá aviso de conectividade.

## Teste local

```bash
streamlit run streamlit_app.py
```

## Referências oficiais

- Streamlit docs: file organization
  - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization
- Streamlit docs: app dependencies
  - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/app-dependencies
- Streamlit docs: secrets management
  - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management
- Streamlit docs: deploy
  - https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy
