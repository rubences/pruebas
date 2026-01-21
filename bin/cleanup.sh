#!/bin/bash
# cleanup.sh - Limpiar archivos duplicados y versiones antiguas

echo "🧹 Limpiando archivos duplicados y reorganizando..."

# Mover figuras antiguas a un subdirectorio
mkdir -p outputs/figures/legacy
mv outputs/figures/Figure_5_TimeSeries.* outputs/figures/legacy/ 2>/dev/null || true
mv outputs/figures/Figure_6_StatisticalValidation.* outputs/figures/legacy/ 2>/dev/null || true
mv outputs/figures/Figure_7_PhaseSpace.* outputs/figures/legacy/ 2>/dev/null || true
mv outputs/figures/Figure_8_HeatMap.* outputs/figures/legacy/ 2>/dev/null || true

# Mover tablas duplicadas de outputs/tables a data/tables
cp outputs/tables/*.csv data/tables/ 2>/dev/null || true

# Limpiar README antiguo
mv README_old.md docs/README_old.md 2>/dev/null || true

# Verificar estructura
echo "✅ Limpieza completada!"
echo ""
echo "📁 Estructura actualizada:"
tree -L 2 -I '__pycache__|*.pyc|.git|legacy' --dirsfirst

echo ""
echo "🎯 Siguiente paso:"
echo "   python bin/run_all.py  # Regenerar todo con nueva estructura"
