# Guia de Início Rápido - Escola Sistema

## 🚀 Inicialização Rápida

### Windows

```bash
# 1. Abrir PowerShell ou CMD
# 2. Navegar até a pasta do projeto
cd caminho\para\escola_sistema

# 3. Executar o script de setup
setup.bat
```

### Linux / Mac

```bash
# 1. Abrir terminal
# 2. Navegar até a pasta do projeto
cd /caminho/para/escola_sistema

# 3. Dar permissão de execução
chmod +x setup.sh

# 4. Executar o script de setup
./setup.sh
```

## 📋 Instruções Manuais (se não usar o script)

### 1. Criar e ativar ambiente virtual

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar banco de dados MySQL

```sql
CREATE DATABASE escola_sistema_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'escola_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON escola_sistema_db.* TO 'escola_user'@'localhost';
FLUSH PRIVILEGES;
```

Ou usando o usuário root (padrão):

- DB_NAME: escola_sistema_db
- DB_USER: root
- DB_PASSWORD: (deixar em branco se sem senha)

### 4. Configurar variáveis de ambiente

Editar arquivo `.env`:

```
DB_NAME=escola_sistema_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3306
```

### 5. Executar migrações

```bash
python backend/manage.py migrate
```

### 6. Criar usuários de teste

```bash
python backend/manage.py create_test_users
```

### 7. Coletar arquivos estáticos

```bash
python backend/manage.py collectstatic --noinput
```

### 8. Iniciar o servidor

```bash
python backend/manage.py runserver
```

## 🌐 Acessar o Sistema

- **URL:** http://localhost:8000
- **Admin:** http://localhost:8000/admin

## 👥 Contas de Teste

| Cargo          | Usuário   | Senha    |
| -------------- | --------- | -------- |
| Diretor        | admin     | admin123 |
| Professor      | prof1     | prof123  |
| Administrativo | admin_esc | admin123 |

## 🔍 Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'django'"

Solução: Ativar o ambiente virtual e instalar dependências novamente

```bash
pip install -r requirements.txt
```

### Erro: "django.db.utils.OperationalError"

Solução: Verificar se o MySQL está rodando e as credenciais estão corretas no `.env`

### Erro: "Port 8000 is already in use"

Solução: Executar em outra porta

```bash
python backend/manage.py runserver 8001
```

## 📝 Próximos Passos

1. Acessar o admin em http://localhost:8000/admin
2. Criar turmas (1A, 1B, 1C, 1D, 2A, 2B, 2C, 2D, 3A, 3B, 3C, 3D)
3. Criar professores
4. Adicionar alunos às turmas
5. Começar a lançar notas

## 📚 Documentação Completa

Veja [README.md](README.md) para mais informações sobre o projeto.
