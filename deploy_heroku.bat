@echo off
echo ========================================
echo CLAWTASKS BR - DEPLOY HEROKU
echo ========================================
echo.

REM Navegar para o diretório
cd /d C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent

echo [1/7] Verificando Heroku CLI...
where heroku >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Heroku CLI nao encontrado!
    echo.
    echo Solucoes:
    echo 1. Feche e abra um NOVO terminal
    echo 2. Ou adicione ao PATH: C:\Program Files\heroku\bin
    echo 3. Ou execute manualmente os comandos do DEPLOY_COMANDOS.md
    pause
    exit /b 1
)
echo OK - Heroku encontrado!
echo.

echo [2/7] Fazendo login no Heroku...
echo (Uma janela do navegador vai abrir)
heroku login
if %errorlevel% neq 0 (
    echo ERRO no login!
    pause
    exit /b 1
)
echo.

echo [3/7] Criando app no Heroku...
heroku create clawtasks-br
if %errorlevel% neq 0 (
    echo App ja existe ou erro. Tentando outro nome...
    heroku create clawtasks-brasil-%RANDOM%
)
echo.

echo [4/7] Configurando variaveis de ambiente...
heroku config:set EFI_CLIENT_ID=Client_Id_bc7b525b1d251d931ca0330e0c908bc0b07bd723
heroku config:set EFI_CLIENT_SECRET=Client_Secret_0e43d64ca0290804471442f6d093783898c0a8e1
heroku config:set EFI_CERTIFICATE_PATH=producao-872278-clawdbot.pem
heroku config:set EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7
heroku config:set EFI_SANDBOX=false
echo.

echo [5/7] Fazendo deploy...
git push heroku main
if %errorlevel% neq 0 (
    echo Tentando branch master...
    git push heroku master
)
echo.

echo [6/7] Abrindo app no navegador...
heroku open
echo.

echo [7/7] Mostrando URL do app...
heroku info -s | findstr web_url
echo.

echo ========================================
echo DEPLOY CONCLUIDO!
echo ========================================
echo.
echo Proximos passos:
echo 1. Configure o webhook Efi com a URL acima
echo 2. Teste uma compra
echo 3. Divulgue e comece a vender!
echo.
pause
