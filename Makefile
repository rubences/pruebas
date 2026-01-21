# 🎯 Makefile - Comandos rápidos para el proyecto
# ═══════════════════════════════════════════════════════════════════════════

.PHONY: help install setup data tables verify figures mdf4 all clean

help:
	@echo ""
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║  🎯 COMANDOS DISPONIBLES - MotoGP Dataset & Glicko-2 v4.0    ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Instalación:"
	@echo "  make install        Instalar dependencias (requirements.txt)"
	@echo "  make setup          Instalar + crear carpetas"
	@echo ""
	@echo "Ejecución Principal:"
	@echo "  make data           Generar dataset v4.0 (20K muestras, 35 canales)"
	@echo "  make tables         Generar 7 tablas métricas"
	@echo "  make verify         Verificar integridad del dataset"
	@echo "  make figures        Generar figuras publicables (300 DPI)"
	@echo "  make mdf4           Generar formato MDF4 industrial"
	@echo ""
	@echo "Conjuntos Útiles:"
	@echo "  make all            Ejecutar TODO (data+tablas+verify+figuras+MDF4)"
	@echo "  make quick          Ejecutar rápido (data+tablas+verify)"
	@echo "  make full           Alias para 'make all'"
	@echo ""
	@echo "Utilidades:"
	@echo "  make status         Mostrar estructura y estadísticas"
	@echo "  make info-data      Info sobre datasets versionados"
	@echo "  make info-scripts   Info sobre scripts disponibles"
	@echo "  make clean          Limpiar outputs (CUIDADO: borra resultados)"
	@echo "  make docs           Ver documentación del proyecto"
	@echo ""

install:
	@echo "📦 Instalando dependencias..."
	pip install -r requirements.txt
	@echo "✅ Instalación completada"

setup: install
	@echo "🔧 Configurando proyecto..."
	mkdir -p data/{raw,processed,versioned}
	mkdir -p scripts/{generators,analysis,utils}
	mkdir -p outputs/{tables,figures,mdf4,reports}
	mkdir -p docs/{guides,summaries}
	@echo "✅ Proyecto configurado"

data:
	@echo "📊 Generando dataset v4.0..."
	python run_all.py --data-only
	@echo "✅ Dataset v4.0 generado"

tables: data
	@echo "📋 Generando tablas métricas..."
	python run_all.py --tables-only
	@echo "✅ Tablas generadas"

verify: data
	@echo "✓ Verificando dataset..."
	python scripts/analysis/verify_dataset_v4.py
	@echo "✅ Verificación completada"

figures: data
	@echo "📈 Generando figuras..."
	python run_all.py --with-figures
	@echo "✅ Figuras generadas"

mdf4: data
	@echo "🔢 Generando MDF4 industrial..."
	python run_all.py --with-mdf4
	@echo "✅ MDF4 generado"

quick: data tables verify
	@echo "✅ Ejecución rápida completada"

all: setup data tables verify figures mdf4
	@echo "✅ TODO completado exitosamente"

full: all
	@echo "✅ Ejecución completa finalizada"

status:
	@echo "📊 Estado del Proyecto:"
	bash show_structure.sh

info-data:
	@echo "📊 Datasets disponibles:"
	ls -lh data/versioned/ | awk 'NR>1 {print "  " $$9 " (" $$5 ")"}'

info-scripts:
	@echo "🐍 Scripts disponibles:"
	@echo "  Generadores:"
	ls -1 scripts/generators/*.py | sed 's/^/    /'
	@echo "  Análisis:"
	ls -1 scripts/analysis/*.py | sed 's/^/    /'
	@echo "  Utils:"
	ls -1 scripts/utils/*.py | sed 's/^/    /'

docs:
	@echo "📚 Documentación disponible:"
	@echo ""
	@echo "  Principal:"
	@echo "    cat PROJECT_STRUCTURE.md       # Estructura del proyecto"
	@echo "    cat README.md                  # Overview"
	@echo ""
	@echo "  Por carpeta:"
	@echo "    cat data/README.md             # Info datasets"
	@echo "    cat scripts/README.md          # Info scripts"
	@echo "    cat outputs/README.md          # Info resultados"
	@echo "    cat docs/README.md             # Info docs"
	@echo ""
	@echo "  Guías:"
	@echo "    cat docs/guides/GUIA_INTEGRACION_PAPER.md"
	@echo ""

clean:
	@echo "⚠️  Limpiando archivos generados..."
	rm -f data/versioned/*.csv
	rm -f data/versioned/*.mf4
	rm -f outputs/tables/*.csv
	rm -f outputs/figures/*.pdf
	rm -f outputs/figures/*.png
	@echo "✅ Archivos limpios (puedes regenerar con 'make all')"

# Funciones auxiliares silenciosas
_check_python:
	@command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 no encontrado"; exit 1; }

_check_data:
	@test -f data/versioned/NLA_CaseStudy_Jerez_Q1_v4_MEGA.csv || { echo "❌ Dataset no encontrado. Ejecuta 'make data'"; exit 1; }
