# Generate PWA Icons
# Creates placeholder icons for the Progressive Web App

Write-Host "Generating PWA icons for Family Chores..." -ForegroundColor Cyan

# Check if PIL/Pillow is installed
$pipList = pip list 2>$null | Select-String "Pillow"

if (-not $pipList) {
    Write-Host "Installing Pillow (PIL) for icon generation..." -ForegroundColor Yellow
    pip install Pillow
}

# Run the icon generator
python scripts\generate_pwa_icons.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`nIcons generated successfully!" -ForegroundColor Green
    Write-Host "Location: static\icons\" -ForegroundColor Gray
    Write-Host "`nNote: These are placeholder icons. Consider creating custom icons for production." -ForegroundColor Yellow
} else {
    Write-Host "`nIcon generation failed!" -ForegroundColor Red
    exit 1
}
