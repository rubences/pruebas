#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  📁 PROYECTO MotoGP DATASET & GLICKO-2 SIMULATOR               ║"
echo "║     Estructura Organizacional Completa                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

echo "🗂️  RAÍZ (Documentación & Config)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
ls -lh | grep -E "\.md|\.txt|\.csv" | awk '{print "  " $9 " (" $5 ")"}'
echo ""

echo "📊 data/ - DATASETS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  raw/        $(ls -1 data/raw/ 2>/dev/null | wc -l) files"
for f in data/raw/*; do echo "    • $(basename $f) ($(du -h $f | cut -f1))"; done
echo "  versioned/  $(ls -1 data/versioned/ 2>/dev/null | wc -l) versions"
for f in data/versioned/*; do echo "    • $(basename $f) ($(du -h $f | cut -f1))"; done
echo ""

echo "🐍 scripts/ - CÓDIGO PYTHON"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  generators/  $(ls -1 scripts/generators/ 2>/dev/null | wc -l) scripts"
ls -1 scripts/generators/ 2>/dev/null | sed 's/^/    • /'
echo "  analysis/    $(ls -1 scripts/analysis/ 2>/dev/null | wc -l) scripts"
ls -1 scripts/analysis/ 2>/dev/null | sed 's/^/    • /'
echo "  utils/       $(ls -1 scripts/utils/ 2>/dev/null | wc -l) scripts"
ls -1 scripts/utils/ 2>/dev/null | sed 's/^/    • /'
echo ""

echo "📈 outputs/ - RESULTADOS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  tables/      $(ls -1 outputs/tables/ 2>/dev/null | wc -l) files"
ls -1 outputs/tables/ 2>/dev/null | sed 's/^/    • /'
echo "  figures/     $(ls -1 outputs/figures/ 2>/dev/null | wc -l) files"
ls -1 outputs/figures/ 2>/dev/null | wc -l | xargs echo "    ($1 figuras publicables: PDF 300DPI + PNG)"
echo "  reports/     $(ls -1 outputs/reports/ 2>/dev/null | wc -l) files"
ls -1 outputs/reports/ 2>/dev/null | sed 's/^/    • /'
echo ""

echo "📚 docs/ - DOCUMENTACIÓN"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  guides/      $(ls -1 docs/guides/ 2>/dev/null | wc -l) files"
ls -1 docs/guides/ 2>/dev/null | sed 's/^/    • /'
echo "  summaries/   $(ls -1 docs/summaries/ 2>/dev/null | wc -l) files"
ls -1 docs/summaries/ 2>/dev/null | sed 's/^/    • /'
echo ""

echo "📊 ESTADÍSTICAS DEL PROYECTO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
TOTAL_FILES=$(find . -type f ! -path './.git/*' | wc -l)
TOTAL_SIZE=$(du -sh . | cut -f1)
SCRIPTS=$(find scripts -name "*.py" | wc -l)
DATA=$(find data -name "*.csv" -o -name "*.mf4" | wc -l)
DOCS=$(find docs outputs -name "*.md" | wc -l)

echo "  Archivos totales:     $TOTAL_FILES"
echo "  Tamaño total:         $TOTAL_SIZE"
echo "  Scripts Python:       $SCRIPTS"
echo "  Archivos de datos:    $DATA"
echo "  Documentación:        $DOCS"
echo ""

echo "✅ LISTO PARA USAR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
