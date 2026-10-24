param([switch]$DejarMySqlActivo)

$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$procesosArchivo = Join-Path $raiz 'logs\procesos_windows.json'
$camunda = Join-Path $env:USERPROFILE 'Downloads\c8run\c8run.exe'

if (Test-Path -LiteralPath $procesosArchivo) {
    $registros = @((Get-Content -LiteralPath $procesosArchivo -Raw | ConvertFrom-Json))
    foreach ($registro in $registros) {
        $proceso = Get-Process -Id $registro.id -ErrorAction SilentlyContinue
        if ($proceso -and $proceso.StartTime.ToUniversalTime().Ticks -eq $registro.inicioUtc) {
            Stop-Process -Id $registro.id -Force
            Write-Host "Detenido proceso $($registro.id)."
        }
    }
    Remove-Item -LiteralPath $procesosArchivo
}

if (Test-Path -LiteralPath $camunda) {
    Write-Host 'Deteniendo Camunda...'
    Push-Location (Split-Path -Parent $camunda)
    try { & $camunda stop; if ($LASTEXITCODE -ne 0) { Write-Warning 'Camunda informó un error al detenerse.' } }
    finally { Pop-Location }
}

if (-not $DejarMySqlActivo) {
    $mysql = Get-Service -Name 'MySQL80' -ErrorAction SilentlyContinue
    if ($mysql -and $mysql.Status -eq 'Running') {
        try {
            Stop-Service -Name 'MySQL80' -ErrorAction Stop
            Write-Host 'MySQL detenido.'
        } catch {
            Write-Warning 'MySQL sigue activo. Abre PowerShell como administrador y vuelve a ejecutar: Stop-Service MySQL80'
        }
    }
}

Write-Host 'Cierre del proyecto terminado.'
