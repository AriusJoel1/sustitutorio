Write-Host "analisis del grafo:"
py src/graph_analysis.py --output metrics.json

Write-Host "generando reporte:"
py src/report_suite.py --input metrics.json --output report.md --format md

Write-Host "viendo el reporte:"
if (Test-Path report.md) {
    $lineCount = (Get-Content report.md).Count
    if ($lineCount -ge 50) {
        Write-Host " reporte OK. lineas: $lineCount"
        notepad report.md  
        exit 0
    } else {
        Write-Host " reporte incompleto. solo $lineCount lineas"
        exit 1
    }
} else {
    Write-Host " no se encontro report.md"
    exit 1
}
