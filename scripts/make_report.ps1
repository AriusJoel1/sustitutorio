Write-Host ">>> Análisis de grafo..."
py src/graph_analysis.py --output metrics.json

Write-Host ">>> Generando reporte..."
py src/report_suite.py --input metrics.json --output report.md --format md

Write-Host ">>> Previsualizando reporte..."
if (Test-Path report.md) {
    $lineCount = (Get-Content report.md).Count
    if ($lineCount -ge 50) {
        Write-Host " Reporte OK. Líneas: $lineCount"
        notepad report.md  # o cámbialo por 'more report.md' si no quieres abrir notepad
        exit 0
    } else {
        Write-Host " Reporte incompleto. Solo $lineCount líneas"
        exit 1
    }
} else {
    Write-Host " No se encontró report.md"
    exit 1
}
