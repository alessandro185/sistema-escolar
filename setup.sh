#!/bin/bash
# Script de inicialização do Escola Sistema
# Linux/Mac

echo ""
echo "========================================"
echo "  Escola Sistema - Setup Inicial"
echo "========================================"
echo ""

# 1. Criar virtual environment
echo "[1/6] Criando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

# 2. Instalar dependências
echo ""
echo "[2/6] Instalando dependências..."
pip install -q -r requirements.txt

# 3. Executar migrações
echo ""
echo "[3/6] Executando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

# 4. Criar usuários e dados de teste
echo ""
echo "[4/6] Criando usuários e dados de teste..."
python manage.py shell < init_db.py

# 5. Coletar arquivos estáticos
echo ""
echo "[5/6] Coletando arquivos estáticos..."
python manage.py collectstatic --noinput -q

# 6. Iniciar servidor
echo ""
echo "[6/6] Iniciando servidor..."
echo ""
echo "========================================"
echo "  Servidor iniciado em:"
echo "  http://localhost:8000"
echo "========================================"
echo ""
echo "Contas de teste:"
echo "  - Usuario: admin | Senha: admin123"
echo "  - Usuario: prof1 | Senha: prof123"
echo "  - Usuario: admin_esc | Senha: admin123"
echo ""
echo "Pressione CTRL+C para parar o servidor"
echo ""

# Iniciar servidor Django
python manage.py runserver
echo "========================================"
echo ""

python manage.py runserver
