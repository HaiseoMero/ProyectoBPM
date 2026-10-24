# Pruebas de los bloques reales del arranque. Comandos de procesos simulados:
# no inicia/detiene servicios ni modifica el firewall.
$ErrorActionPreference = 'Stop'
$rutaInicio = Join-Path $PSScriptRoot '..\..\iniciar_windows.ps1'
$errores = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile($rutaInicio, [ref]$null, [ref]$errores)
if ($errores.Count -gt 0) { throw 'El script de arranque contiene errores de sintaxis.' }

function Assert-Equal($actual, $esperado, [string]$mensaje) {
    if ($actual -ne $esperado) { throw "$mensaje. Esperado: $esperado; recibido: $actual" }
}

$funcionEscucha = $ast.EndBlock.Statements | Where-Object {
    $_ -is [System.Management.Automation.Language.FunctionDefinitionAst] -and $_.Name -eq 'Test-EscuchaWifi'
}
. ([scriptblock]::Create($funcionEscucha.Extent.Text))
function netstat { $script:lineasNetstat }
$script:lineasNetstat = @('  TCP    127.0.0.1:5173    0.0.0.0:0    LISTENING    17')
Assert-Equal (Test-EscuchaWifi) $false 'Loopback no es modo Wi-Fi'
$script:lineasNetstat = @('  TCP    0.0.0.0:5174    0.0.0.0:0    LISTENING    17')
Assert-Equal (Test-EscuchaWifi) $false 'Otro puerto no es el frontend del proyecto'
$script:lineasNetstat = @('  TCP    0.0.0.0:5173    0.0.0.0:0    LISTENING    17')
Assert-Equal (Test-EscuchaWifi) $true 'Detecta el frontend accesible en la red'
Write-Host 'PASS: detección del modo local, Wi-Fi y otros puertos.'

$cambioModo = $ast.EndBlock.Statements | Where-Object {
    $_ -is [System.Management.Automation.Language.IfStatementAst] -and $_.Extent.Text.Contains('$registroFrontend =')
}
if (-not $cambioModo) { throw 'No se encontró el bloque de cambio de modo.' }
$bloqueCambio = [scriptblock]::Create($cambioModo.Extent.Text)
function Test-Pagina { return $true }
function Test-EscuchaWifi { return $false }
function Obtener-PidPuerto { return 17 }
function Test-Puerto { return $false }
function Get-Process { return [pscustomobject]@{ Id = 17; StartTime = $script:inicioProceso } }
function Stop-Process { param([int]$Id, [switch]$Force); $script:detenidos += $Id }
$Wifi = $true
$script:inicioProceso = [datetime]'2026-10-01T10:00:00Z'

$activos = @()
$script:detenidos = @()
$fallo = $false
try { & $bloqueCambio } catch { $fallo = $_.Exception.Message -like '*fuera de este script*' }
Assert-Equal $fallo $true 'Rechaza detener un proceso ajeno'
Assert-Equal $script:detenidos.Count 0 'No se detuvo ningún proceso ajeno'
Write-Host 'PASS: un frontend ajeno no se detiene.'

$activos = @([pscustomobject]@{ id = 17; inicioUtc = 0 })
$script:detenidos = @()
$fallo = $false
try { & $bloqueCambio } catch { $fallo = $_.Exception.Message -like '*proceso del frontend cambió*' }
Assert-Equal $fallo $true 'Rechaza un PID reutilizado'
Assert-Equal $script:detenidos.Count 0 'No se detuvo un PID reutilizado'
Write-Host 'PASS: un PID reutilizado no se detiene.'

$activos = @([pscustomobject]@{ id = 17; inicioUtc = $script:inicioProceso.ToUniversalTime().Ticks },
    [pscustomobject]@{ id = 99; inicioUtc = 0 })
$script:detenidos = @()
& $bloqueCambio
Assert-Equal $script:detenidos.Count 1 'Solo debe detenerse un proceso'
Assert-Equal $script:detenidos[0] 17 'Solo se detiene el frontend registrado'
Write-Host 'PASS: el cambio de modo reinicia solo el frontend registrado.'
