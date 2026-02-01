# ClawTasks BR - Deploy Heroku (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLAWTASKS BR - DEPLOY HEROKU" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navegar para o diretório
Set-Location "C:\Users\Amauri\.gemini\antigravity\scratch\OpenClaw_Agent"

Write-Host "[1/7] Verificando Heroku CLI..." -ForegroundColor Yellow
$herokuPath = Get-Command heroku -ErrorAction SilentlyContinue
if (-not $herokuPath) {
    Write-Host "ERRO: Heroku CLI não encontrado!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Soluções:" -ForegroundColor Yellow
    Write-Host "1. Feche e abra um NOVO PowerShell"
    Write-Host "2. Ou adicione ao PATH: C:\Program Files\heroku\bin"
    Write-Host "3. Ou execute manualmente os comandos do DEPLOY_COMANDOS.md"
    Read-Host "Pressione ENTER para sair"
    exit 1
}
Write-Host "OK - Heroku encontrado!" -ForegroundColor Green
Write-Host ""

Write-Host "[2/7] Fazendo login no Heroku..." -ForegroundColor Yellow
Write-Host "(Uma janela do navegador vai abrir)" -ForegroundColor Gray
heroku login
Write-Host ""

Write-Host "[3/7] Criando app no Heroku..." -ForegroundColor Yellow
$appName = "clawtasks-br"
heroku create $appName 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "App já existe ou erro. Tentando outro nome..." -ForegroundColor Yellow
    $randomSuffix = Get-Random -Minimum 1000 -Maximum 9999
    $appName = "clawtasks-brasil-$randomSuffix"
    heroku create $appName
}
Write-Host ""

Write-Host "[4/7] Configurando variáveis de ambiente..." -ForegroundColor Yellow
heroku config:set EFI_CLIENT_ID=Client_Id_bc7b525b1d251d931ca0330e0c908bc0b07bd723
heroku config:set EFI_CLIENT_SECRET=Client_Secret_0e43d64ca0290804471442f6d093783898c0a8e1
heroku config:set EFI_CERTIFICATE_PATH=producao-872278-clawdbot.pem
heroku config:set EFI_PIX_KEY=56bbb9d4-d884-4456-97bd-8c32ea5ce8d7
heroku config:set EFI_SANDBOX=false
Write-Host ""

Write-Host "[5/7] Fazendo deploy..." -ForegroundColor Yellow
git push heroku main 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Tentando branch master..." -ForegroundColor Yellow
    git push heroku master
}
Write-Host ""

Write-Host "[6/7] Abrindo app no navegador..." -ForegroundColor Yellow
heroku open
Write-Host ""

Write-Host "[7/7] Informações do app..." -ForegroundColor Yellow
$appInfo = heroku info
Write-Host $appInfo
Write-Host ""

Write-Host "========================================" -ForegroundColor Green
Write-Host "DEPLOY CONCLUÍDO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Configure o webhook Efí com a URL acima"
Write-Host "2. Teste uma compra"
Write-Host "3. Divulgue e comece a vender!"
Write-Host ""
Read-Host "Pressione ENTER para sair"
