# Deploy na Vercel

O projeto usa Django com WSGI (`config.wsgi.application`). A Vercel detecta o `manage.py`, instala as dependências de `requirements.txt` e executa `collectstatic` durante o build. Os arquivos estáticos são servidos pela CDN da Vercel.

## Configuração do projeto

1. Importe o repositório na Vercel.
2. Deixe **Root Directory** na raiz do repositório. A raiz contém `requirements.txt`; o `manage.py` está em `backend/`.
3. Use o preset Django/Python detectado automaticamente. Não defina um Build Command personalizado.
4. Adicione as variáveis abaixo em **Settings → Environment Variables** para Production e Preview conforme necessário.

| Variável | Valor |
| --- | --- |
| `DEBUG` | `False` |
| `SECRET_KEY` | Segredo aleatório longo e exclusivo; gere um valor novo, não reutilize a chave local. |
| `DATABASE_URL` | URL de um PostgreSQL gerenciado, com SSL quando exigido pelo provedor. |
| `ALLOWED_HOSTS` | `.vercel.app,seu-dominio.com` (inclua seu domínio próprio, se usar). |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app,https://seu-dominio.com` (inclua a origem HTTPS do domínio próprio). |

`ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` podem ser omitidas se usar somente o domínio `*.vercel.app`. O banco não deve ser SQLite: o sistema de arquivos de uma Function não é armazenamento persistente. Crie/conecte um PostgreSQL por um provedor integrado à Vercel e use a URL de conexão de produção.

## Banco de dados

Depois de configurar as variáveis, aplique as migrações no banco de produção uma vez:

```bash
vercel env pull .env
python backend/manage.py migrate
```

Execute isso a partir da raiz do repositório, com o projeto Vercel já vinculado (`vercel link`). O `.env` já está no `.gitignore`; não o envie ao repositório. Não carregue dados de teste em produção.

## Limitação de fotos dos alunos

As fotos são gravadas em `MEDIA_ROOT` no disco local. Esse disco é efêmero nas Vercel Functions, então uploads não são duráveis e podem sumir ou não aparecer em outra instância. Antes de usar fotos em produção, configure armazenamento persistente externo para mídia (por exemplo, S3 compatível) e adapte o storage do Django. O deploy da aplicação pode funcionar sem isso, mas uploads não estão prontos para produção.

## Verificação local de produção

Com as variáveis de produção disponíveis no ambiente e antes do deploy:

```bash
python backend/manage.py check --deploy
python backend/manage.py migrate --check
```

O HTTPS é terminado pela Vercel; as configurações de produção do Django redirecionam HTTP para HTTPS, habilitam cookies seguros e HSTS. Se mudar `SECURE_HSTS_SECONDS` ou o domínio, revise as variáveis antes de publicar.
