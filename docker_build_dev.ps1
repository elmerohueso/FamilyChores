# Check if Docker engine is running
$dockerRunning = docker info 2>$null
if (-not $dockerRunning) {
    Write-Host "Docker engine is not running. Starting Docker Desktop..." -ForegroundColor Yellow
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    
    Write-Host "Waiting for Docker engine to start..." -ForegroundColor Yellow
    $timeout = 60
    $elapsed = 0
    while ($elapsed -lt $timeout) {
        Start-Sleep -Seconds 2
        $elapsed += 2
        $dockerRunning = docker info 2>$null
        if ($dockerRunning) {
            Write-Host "Docker engine started successfully." -ForegroundColor Green
            break
        }
    }
    
    if (-not $dockerRunning) {
        Write-Host "Docker engine failed to start within $timeout seconds. Please start Docker Desktop manually." -ForegroundColor Red
        exit 1
    }
}

docker compose -f docker-compose-dev.yml up --build
