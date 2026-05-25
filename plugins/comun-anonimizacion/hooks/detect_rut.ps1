<#
.SYNOPSIS
    Detecta RUTs chilenos reales en stdin. Sale con código no-cero si encuentra alguno.

.DESCRIPTION
    Hook para Claude Code. Lee stdin (que puede ser JSON con campo 'prompt'/'content',
    o texto plano). Aplica regex para RUTs chilenos. Valida módulo 11. Excluye dummies
    11111111-1, 22222222-2, 33333333-3. Si encuentra RUT real, escribe warning a stderr
    y sale con código 1 (PostToolUse no-bloqueante, UserPromptSubmit no-bloqueante).
#>

[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'

# Leer stdin completo
$raw = [Console]::In.ReadToEnd()

# Intentar parsear como JSON; extraer 'prompt' o 'content' si existe
$text = $raw
try {
    $payload = $raw | ConvertFrom-Json -ErrorAction Stop
    if ($payload.prompt) {
        $text = [string]$payload.prompt
    } elseif ($payload.content) {
        $text = [string]$payload.content
    } elseif ($payload.tool_input -and $payload.tool_input.content) {
        $text = [string]$payload.tool_input.content
    }
} catch {
    # No es JSON, usar raw
    $text = $raw
}

# Regex RUT chileno: 1-2 dígitos, opcional punto, 3 dígitos, opcional punto, 3 dígitos, opcional guión, 1 dígito o K
$pattern = '\b\d{1,2}\.?\d{3}\.?\d{3}-?[\dkK]\b|\b\d{7,8}-?[\dkK]\b'
$matches = [regex]::Matches($text, $pattern)

if ($matches.Count -eq 0) {
    exit 0
}

# Validador módulo 11
function Test-RutCheckDigit {
    param([string]$Rut)

    $clean = ($Rut -replace '\.', '') -replace '-', ''
    $clean = $clean.ToUpper()
    if ($clean.Length -lt 2) { return $false }

    $body = $clean.Substring(0, $clean.Length - 1)
    $dv = $clean.Substring($clean.Length - 1, 1)

    if ($body -notmatch '^\d+$') { return $false }

    $multipliers = @(2, 3, 4, 5, 6, 7)
    $total = 0
    $bodyChars = $body.ToCharArray()
    [array]::Reverse($bodyChars)
    for ($i = 0; $i -lt $bodyChars.Length; $i++) {
        $digit = [int][string]$bodyChars[$i]
        $mult = $multipliers[$i % $multipliers.Length]
        $total += $digit * $mult
    }

    $remainder = $total % 11
    $expected = 11 - $remainder

    if ($expected -eq 11) {
        $expectedDv = '0'
    } elseif ($expected -eq 10) {
        $expectedDv = 'K'
    } else {
        $expectedDv = [string]$expected
    }

    return $dv -eq $expectedDv
}

# Filtrar: solo RUTs que pasan módulo 11 Y no son dummies
$dummies = @('11111111-1', '22222222-2', '33333333-3')
$realRuts = @()
foreach ($m in $matches) {
    $rutValue = $m.Value
    if ((Test-RutCheckDigit -Rut $rutValue) -and ($dummies -notcontains $rutValue)) {
        $realRuts += $rutValue
    }
}

if ($realRuts.Count -gt 0) {
    $sample = $realRuts[0]
    [Console]::Error.WriteLine("`n[comun-anonimizacion] Detectado(s) $($realRuts.Count) RUT(s) chileno(s) posiblemente reales en este input. Considera ejecutar /anonimizar primero.")
    [Console]::Error.WriteLine("Ejemplo: $sample")
    exit 1
}

exit 0
