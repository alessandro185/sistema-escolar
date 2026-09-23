# 📚 Escola Sistema - Sistema de Gestão Escolar

Sistema completo de gestão escolar desenvolvido em Django para escolas de ensino médio.

## 🎯 Características

- **Autenticação e controle de acesso** - Diretor, professor e administrativo
- **Gestão de alunos** - Cadastro completo com foto, endereço e responsáveis
- **Gestão de turmas** - Criação e organização de turmas por ano
- **Gestão de professores** - Cadastro com disciplinas e carga horária
- **Sistema de notas** - Lançamento de notas com cálculo automático de média
- **Dashboard** - Painel com estatísticas gerais
- **Interface simples** - Design limpo e intuitivo com Tailwind CSS

## 🛠️ Stack Tecnológico

- **Backend**: Django 4.2
- **Banco de Dados**: SQLite local e PostgreSQL em producao
- **Frontend**: Django Templates + Tailwind CSS + Alpine.js
- **Upload de arquivos**: Django media (fotos de alunos)

## 📋 Estrutura de Apps

```text
.
├── backend/                 # Django: apps, config, scripts e manage.py
├── frontend/                # Templates Django e arquivos estáticos
├── requirements.txt         # Dependências Python instaladas pela Vercel
├── vercel.json              # Inclui templates no pacote da Function
└── .python-version          # Versão Python usada na Vercel
```

## 🚀 Instalação e Configuração

### 1. Clonar o repositório

```bash
git clone <repository-url>
cd escola_sistema
```

### 2. Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar banco de dados MySQL

```bash
# Criar banco de dados
CREATE DATABASE escola_sistema_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'escola_user'@'localhost' IDENTIFIED BY 'senha_segura';
GRANT ALL PRIVILEGES ON escola_sistema_db.* TO 'escola_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Configurar variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas configurações
# DB_NAME=escola_sistema_db
# DB_USER=escola_user
# DB_PASSWORD=senha_segura
# DB_HOST=localhost
# DB_PORT=3306
# SECRET_KEY=sua-chave-secreta-altere-em-producao
```

### 6. Executar migrações

```bash
python backend/manage.py migrate
```

### 7. Criar superusuário

```bash
python backend/manage.py createsuperuser
```

### 8. Criar usuários de teste

```bash
python backend/manage.py create_test_users
```

### 9. Coletar arquivos estáticos

```bash
python backend/manage.py collectstatic --noinput
```

### 10. Executar servidor de desenvolvimento

```bash
python backend/manage.py runserver
```

Acesse em: `http://localhost:8000`

## 👥 Contas de Teste

Após executar `python backend/manage.py create_test_users`:

| Cargo          | Usuário   | Senha    |
| -------------- | --------- | -------- |
| Diretor        | admin     | admin123 |
| Professor      | prof1     | prof123  |
| Administrativo | admin_esc | admin123 |

## 📝 Uso do Sistema

### Login

- Acesse `http://localhost:8000/usuarios/login/`
- Use uma das contas de teste acima

### Dashboard

- Visualize estatísticas gerais do sistema
- Acesse ações rápidas para os diferentes módulos

### Alunos

- Cadastre novos alunos com foto e informações completas
- Busque alunos por nome ou CPF
- Transfira alunos entre turmas

### Turmas

- Crie turmas para cada ano (1º, 2º, 3º)
- Visualize alunos por turma
- Associe professores às turmas

### Notas

- Professores lançam notas dos alunos
- Sistema calcula automaticamente a média
- Acompanhe o desempenho dos alunos

## 🔒 Segurança

- Todas as views exigem autenticação
- Confirmação obrigatória antes de exclusões
- CSRF protection em todos os formulários
- Variáveis de ambiente para dados sensíveis

## 📱 Responsividade

A interface é totalmente responsiva e funciona bem em:

- Computadores desktop
- Tablets
- Smartphones

## 🤝 Contribuir

Para contribuir com o projeto:

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 📧 Suporte

Para suporte, envie um email ou abra uma issue no repositório.

---

**Desenvolvido por:** Seu Nome  
**Última atualização:** Maio de 2026
