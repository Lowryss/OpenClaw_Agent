# OpenClaw Dashboard Launcher
# Forces use of 'principal' agent

Write-Host "🦞 Iniciando OpenClaw Dashboard com agente 'principal'..." -ForegroundColor Cyan

# Set environment variable to force agent selection
$env:OPENCLAW_AGENT = "principal"

# Launch dashboard
try {
    openclaw dashboard
} catch {
    Write-Host "❌ Erro ao iniciar dashboard:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
}
