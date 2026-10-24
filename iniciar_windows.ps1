param([switch]$NoAbrirNavegador, [switch]$Wifi)

$ErrorActionPreference = 'Stop'
$raiz = $PSScriptRoot
$camunda = Join-Path $env:USERPROFILE 'Downloads\c8run\c8run.exe'
$python = Join-Path $raiz 'backend\venv\Scripts\python.exe'
$node = 'C:\Program Files\nodejs\node.exe'
$vite = Join-Path $raiz 'node_modules\vite\bin\vite.js'
$registros = Join-Path $raiz 'logs'
$procesosArchivo = Join-Path $registros 'procesos_windows.json'

function Test-Puerto([int]$puerto) {
    $cliente = [System.Net.Sockets.TcpClient]::new()
    try {
        $resultado = $cliente.BeginConnect('127.0.0.1', $puerto, $null, $null)
        return ($resultado.AsyncWaitHandle.WaitOne(1000) -and $cliente.Connected)
    } catch {
        return $false
    } finally {
        $cliente.Dispose()
    }
}

function Esperar-Puerto([int]$puerto, [int]$segundos) {
    $limite = (Get-Date).AddSeconds($segundos)
    do {
        if (Test-Puerto $puerto) { return }
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $limite)
    throw "El puerto $puerto no respondió. Revisa los archivos de logs."
}

function Test-Pagina {
    try {
        $respuesta = Invoke-WebRequest -Uri 'http://127.0.0.1:5173/' -TimeoutSec 2 -UseBasicParsing
        return $respuesta.StatusCode -eq 200 -and $respuesta.Content -match 'id="app"'
    }
    catch { return $false }
}

function Test-Api {
    try {
        $respuesta = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/' -TimeoutSec 2
        return $respuesta.status -eq 'ok' -and $respuesta.service -eq 'vocalis-api'
    } catch { return $false }
}

function Obtener-PidPuerto([int]$puerto) {
    foreach ($linea in (netstat -ano)) {
        if ($linea -match "^\s*TCP\s+\S+:$puerto\s+\S+\s+LISTENING\s+(\d+)\s*$") {
            return [int]$Matches[1]
        }
    }
    return $null
}

function Registro-Proceso([int]$idProceso) {
    $proceso = Get-Process -Id $idProceso -ErrorAction Stop
    return [pscustomobject]@{
        id = $idProceso
        inicioUtc = $proceso.StartTime.ToUniversalTime().Ticks
    }
}

function Test-EscuchaWifi {
    return [bool](@(netstat -ano | Where-Object {
        $_ -match '^\s*TCP\s+0\.0\.0\.0:5173\s+\S+\s+LISTENING\s+\d+\s*$'
    }).Count)
}

function Obtener-UrlsWifi {
    foreach ($adaptador in [System.Net.NetworkInformation.NetworkInterface]::GetAllNetworkInterfaces()) {
        if ($adaptador.OperationalStatus -ne 'Up' -or $adaptador.NetworkInterfaceType -eq 'Loopback') { continue }
        $propiedades = $adaptador.GetIPProperties()
        if ($propiedades.GatewayAddresses.Count -eq 0) { continue }
        foreach ($direccion in $propiedades.UnicastAddresses) {
            if ($direccion.Address.AddressFamily -eq 'InterNetwork' -and $direccion.Address.IPAddressToString -notlike '169.254.*') {
                "http://$($direccion.Address.IPAddressToString):5173/"
            }
        }
    }
}

foreach ($ruta in @($camunda, $python, $node, $vite, (Join-Path $raiz 'backend\.env'), (Join-Path $raiz '.env'))) {
    if (-not (Test-Path -LiteralPath $ruta)) { throw "Falta: $ruta" }
}
New-Item -ItemType Directory -Path $registros -Force | Out-Null

$mysql = Get-Service -Name 'MySQL80' -ErrorAction Stop
if ($mysql.Status -ne 'Running') {
    try { Start-Service -Name 'MySQL80' -ErrorAction Stop }
    catch { throw 'No se pudo iniciar MySQL80. Abre PowerShell como administrador y vuelve a ejecutar el script.' }
}
Esperar-Puerto 3306 30

if (-not (Test-Puerto 26500)) {
    Write-Host 'Iniciando Camunda...'
    Push-Location (Split-Path -Parent $camunda)
    try { & $camunda start; if ($LASTEXITCODE -ne 0) { throw 'Camunda no pudo iniciarse.' } }
    finally { Pop-Location }
}
Esperar-Puerto 26500 150

$guardados = @()
if (Test-Path -LiteralPath $procesosArchivo) {
    $guardados = @((Get-Content -LiteralPath $procesosArchivo -Raw | ConvertFrom-Json))
}
$activos = @($guardados | Where-Object {
    $proceso = Get-Process -Id $_.id -ErrorAction SilentlyContinue
    $proceso -and $proceso.StartTime.ToUniversalTime().Ticks -eq $_.inicioUtc
})

if ((Test-Puerto 8000) -and -not (Test-Api)) {
    throw 'El puerto 8000 está ocupado por otro servicio o la API no está sana.'
}
if (-not (Test-Api)) {
    Write-Host 'Iniciando API...'
    $proceso = Start-Process -FilePath $python -ArgumentList @('-B', '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000') -WorkingDirectory (Join-Path $raiz 'backend') -WindowStyle Hidden -RedirectStandardOutput (Join-Path $registros 'backend.out.log') -RedirectStandardError (Join-Path $registros 'backend.err.log') -PassThru
    Esperar-Puerto 8000 45
    if (-not (Test-Api)) { throw 'La API se inició, pero no respondió correctamente.' }
    $activos += Registro-Proceso $proceso.Id
    $servidorPid = Obtener-PidPuerto 8000
    if ($servidorPid -and $servidorPid -ne $proceso.Id) { $activos += Registro-Proceso $servidorPid }
}

if ((Test-Puerto 5173) -and -not (Test-Pagina)) {
    throw 'El puerto 5173 está ocupado por otro servicio. No se cambiará a otro puerto.'
}

# Cambiar de modo solo reinicia el frontend que este script registró.
if ((Test-Pagina) -and ((Test-EscuchaWifi) -ne [bool]$Wifi)) {
    $frontendPid = Obtener-PidPuerto 5173
    $registroFrontend = $activos | Where-Object { $_.id -eq $frontendPid } | Select-Object -First 1
    if (-not $registroFrontend) {
        throw 'La página fue iniciada fuera de este script. Cierra su terminal y vuelve a iniciar en el modo deseado.'
    }
    $frontend = Get-Process -Id $registroFrontend.id -ErrorAction Stop
    if ($frontend.StartTime.ToUniversalTime().Ticks -ne $registroFrontend.inicioUtc) {
        throw 'El proceso del frontend cambió. No se detuvo ningún proceso.'
    }
    Stop-Process -Id $frontend.Id -Force
    $activos = @($activos | Where-Object { $_.id -ne $frontend.Id })
    $limite = (Get-Date).AddSeconds(10)
    while ((Test-Puerto 5173) -and (Get-Date) -lt $limite) { Start-Sleep -Milliseconds 250 }
    if (Test-Puerto 5173) { throw 'El puerto 5173 no se liberó después de cerrar el frontend.' }
}

if (-not (Test-Pagina)) {
    Write-Host 'Iniciando página...'
    $hostPagina = if ($Wifi) { '0.0.0.0' } else { '127.0.0.1' }
    # Mantener /api aunque el entorno anterior conserve una URL con localhost.
    $apiAnterior = $env:VITE_API_BASE_URL
    try {
        $env:VITE_API_BASE_URL = '/api'
        $proceso = Start-Process -FilePath $node -ArgumentList @($vite, '--host', $hostPagina, '--port', '5173', '--strictPort') -WorkingDirectory $raiz -WindowStyle Hidden -RedirectStandardOutput (Join-Path $registros 'frontend.out.log') -RedirectStandardError (Join-Path $registros 'frontend.err.log') -PassThru
    } finally { $env:VITE_API_BASE_URL = $apiAnterior }
    $limite = (Get-Date).AddSeconds(45)
    do {
        if (Test-Pagina) { break }
        Start-Sleep -Seconds 2
    } while ((Get-Date) -lt $limite)
    if (-not (Test-Pagina)) { throw 'La página no respondió en el puerto 5173.' }
    $activos += Registro-Proceso $proceso.Id
}

$lista = @($activos | Sort-Object id -Unique)
ConvertTo-Json -InputObject $lista -Depth 3 | Set-Content -LiteralPath $procesosArchivo -Encoding utf8
Write-Host 'Proyecto disponible en http://localhost:5173/'
if ($Wifi) {
    Write-Host 'En el teléfono conectado al mismo Wi-Fi, abre una de estas direcciones:'
    $urlsWifi = @(Obtener-UrlsWifi | Sort-Object -Unique)
    if ($urlsWifi.Count -eq 0) { Write-Warning 'No se encontró una dirección de red. Revisa la conexión del computador.' }
    $urlsWifi | ForEach-Object { Write-Host $_ }
    Write-Host 'Si Windows bloquea el acceso, consulta MOVIL_WINDOWS.md.'
}
if (-not $NoAbrirNavegador) { Start-Process 'http://localhost:5173/' }
