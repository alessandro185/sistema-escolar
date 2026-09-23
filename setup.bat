@echo off
REM Script de inicialização do Escola Sistema
REM Windows

echo.
echo ========================================
echo   Escola Sistema - Setup Inicial
echo ========================================
echo.

REM 1. Criar virtual environment
echo [1/6] Criando ambiente virtual...
python -m venv venv
call venv\Scripts\activate.bat

REM 2. Instalar dependências
echo.
echo [2/6] Instalando dependências...
pip install -q -r requirements.txt

REM 3. Executar migrações
echo.
echo [3/6] Executando migrações do banco de dados...
python backend/manage.py makemigrations
python backend/manage.py migrate

REM 4. Criar usuários e dados de teste
echo.
echo [4/6] Criando usuários e dados de teste...
python backend/manage.py shell < backend/scripts/init_db.py

REM 5. Coletar arquivos estáticos
echo.
echo [5/6] Coletando arquivos estáticos...
python backend/manage.py collectstatic --noinput -q

REM 6. Iniciar servidor
echo.
echo [6/6] Iniciando servidor...
echo.
echo ========================================
echo   Servidor iniciado em:
echo   http://localhost:8000
echo ========================================
echo.
echo Contas de teste:
echo   - Usuario: admin | Senha: admin123
echo   - Usuario: professor1 | Senha: professor123
echo   - Usuario: admin_esc | Senha: admin123
echo.
echo Pressione CTRL+C para parar o servidor
echo.

python backend/manage.py runserver
echo ========================================
echo.

python backend/manage.py runserver
