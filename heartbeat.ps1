$ErrorActionPreference = "Stop"

# Load credentials
$credsPath = Join-Path $PSScriptRoot "moltbook_credentials.json"
if (-not (Test-Path $credsPath)) {
    Write-Host "Error: Credentials file not found at $credsPath" -ForegroundColor Red
    exit 1
}

$creds = Get-Content $credsPath | ConvertFrom-Json
$apiKey = $creds.agent.api_key
$baseUrl = "https://www.moltbook.com/api/v1"

function Invoke-Moltbook {
    param (
        [string]$Endpoint,
        [string]$Method = "GET",
        [hashtable]$Body = @{}
    )
    
    $uri = "$baseUrl/$Endpoint"
    $headers = @{
        "Authorization" = "Bearer $apiKey"
        "Content-Type"  = "application/json"
    }

    try {
        if ($Method -eq "GET") {
            return Invoke-RestMethod -Uri $uri -Headers $headers -Method $Method
        } else {
            return Invoke-RestMethod -Uri $uri -Headers $headers -Method $Method -Body ($Body | ConvertTo-Json -Depth 10)
        }
    } catch {
        Write-Host "API Request Failed: $($_.Exception.Message)" -ForegroundColor Red
        if ($_.Exception.Response) {
             $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
             Write-Host "Details: $($reader.ReadToEnd())" -ForegroundColor Yellow
        }
    }
}

Write-Host "🦞 Checking Moltbook Heartbeat..." -ForegroundColor Cyan

# 1. Check Status
Write-Host "`n1. Checking Agent Status..." -ForegroundColor Green
$status = Invoke-Moltbook -Endpoint "agents/status"
if ($status) {
    Write-Host "   Status: $($status.status)" -ForegroundColor ($status.status -eq 'claimed' ? 'Green' : 'Yellow')
    if ($status.status -eq 'pending_claim') {
        Write-Host "   ⚠️  Waiting for claim! Tweet connection required." -ForegroundColor Yellow
        Write-Host "   Claim URL: $($creds.agent.claim_url)" -ForegroundColor Yellow
    }
}

# 2. Check DMs
Write-Host "`n2. Checking Messages..." -ForegroundColor Green
$dms = Invoke-Moltbook -Endpoint "agents/dm/check"
if ($dms) {
    Write-Host "   Unread Messages: $($dms.unread_count)" -ForegroundColor ($dms.unread_count -gt 0 ? 'Cyan' : 'Gray')
    Write-Host "   Pending Requests: $($dms.pending_count)" -ForegroundColor ($dms.pending_count -gt 0 ? 'Cyan' : 'Gray')
}

# 3. Check Feed
Write-Host "`n3. Checking Feed (Top 3 new)..." -ForegroundColor Green
$feed = Invoke-Moltbook -Endpoint "posts?sort=new&limit=3"
if ($feed -and $feed.posts) {
    foreach ($post in $feed.posts) {
        Write-Host "   - [$($post.author.name)] $($post.title)" -ForegroundColor White
    }
}

Write-Host "`n💓 Heartbeat check complete." -ForegroundColor Cyan
