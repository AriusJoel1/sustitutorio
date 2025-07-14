#!/usr/bin/env bash
set -e

#analisis de grafo
step_init() {
  py src/graph_analysis.py --output metrics.json
}

#reporte
step_report() {
  py src/report_suite.py --input metrics.json --output report.md --format md
}

#vista previa 
step_preview() {
  if command -v less &>/dev/null; then
    less report.md
  else
    cat report.md
  fi
}

main() {
  echo ">>> analisis de grafo..."
  step_init
  echo ">>> generando reporte..."
  step_report
  echo ">>> previsualizando reporte..."
  step_preview
}

main
