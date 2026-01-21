#!/bin/bash

# INTERPRETAR FIGURAS - Asistente Interactivo
# Uso: bash bin/interpret_figures.sh

# Colors
RED='\033[0;31m'
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

show_menu() {
    clear
    echo -e "${BOLD}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}                    📊 INTERPRETAR FIGURAS - ASISTENTE INTERACTIVO${NC}"
    echo -e "${BOLD}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${CYAN}¿Qué deseas hacer?${NC}"
    echo ""
    echo -e "${YELLOW}1.${NC} Entender las TRES métricas principales"
    echo -e "${YELLOW}2.${NC} Leer FIGURA ESPECÍFICA (5-12)"
    echo -e "${YELLOW}3.${NC} Ver CASOS DE USO reales"
    echo -e "${YELLOW}4.${NC} Ver TABLA DE REFERENCIA"
    echo -e "${YELLOW}5.${NC} Ver CHECKLIST rápido"
    echo -e "${YELLOW}6.${NC} Salir"
    echo ""
    echo -e "${BOLD}════════════════════════════════════════════════════════════════════════════════${NC}"
    read -p "Elige opción (1-6): " choice
    
    case $choice in
        1) show_metrics ;;
        2) show_figures ;;
        3) show_use_cases ;;
        4) show_reference ;;
        5) show_checklist ;;
        6) exit 0 ;;
        *) echo "Opción no válida" && sleep 2 && show_menu ;;
    esac
}

show_metrics() {
    clear
    echo -e "${GREEN}🔑 LAS TRES MÉTRICAS PRINCIPALES${NC}"
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}1. GLICKO VOLATILITY σ: -83.6% ⭐ PRINCIPAL${NC}"
    echo "   Baseline: 0.1290 → Optimized: 0.0212"
    echo "   p < 1e-12, Cohen's d = 3.29"
    echo "   → Setup mucho MÁS PREDECIBLE"
    echo ""
    echo -e "${BOLD}2. WHEEL SLIP: -40%${NC}"
    echo "   Baseline: 6.25% → Optimized: 3.75%"
    echo "   → Mejor TRACCIÓN en salidas"
    echo ""
    echo -e "${BOLD}3. ENGINE EFFICIENCY: +2.32%${NC}"
    echo "   Baseline: 94.83% → Optimized: 97.15%"
    echo "   → Menos DESPERDICIO de energía"
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════════════════${NC}"
    read -p "Presiona ENTER para volver al menú..."
    show_menu
}

show_figures() {
    clear
    echo -e "${GREEN}📊 FIGURAS (5-12)${NC}"
    echo ""
    echo -e "${YELLOW}Elige figura:${NC}"
    echo "5 - Time Series (líneas en el tiempo)"
    echo "6 - Statistical Validation ⭐ PRINCIPAL (histogramas)"
    echo "7 - Performance Metrics (barras de mejora)"
    echo "8 - Dynamics & Control (bandas)"
    echo "9 - Box Plot (cajas)"
    echo "10 - Scatter Plot (puntos)"
    echo "11 - Efficiency by Section (por secciones)"
    echo "12 - Advanced Metrics (métricas avanzadas)"
    echo "0 - Volver al menú"
    echo ""
    read -p "Elige figura (0-12): " fig
    
    case $fig in
        5)
            clear
            echo -e "${GREEN}FIGURA 5: TIME SERIES${NC}"
            echo "Líneas mostrando cómo cambian métricas en el tiempo"
            echo "✓ Busca: Líneas AZULES más SUAVES que ROJAS"
            echo "✓ Significa: Setup estable, predecible"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        6)
            clear
            echo -e "${GREEN}FIGURA 6: STATISTICAL VALIDATION ⭐${NC}"
            echo "Histogramas con distribuciones (PRINCIPAL)"
            echo "✓ Busca: Curva AZUL concentrada, ROJA dispersa"
            echo "✓ Significa: -83.6% Volatility (REAL, p < 1e-12)"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        7)
            clear
            echo -e "${GREEN}FIGURA 7: PERFORMANCE METRICS${NC}"
            echo "Barras comparativas de las 3 métricas"
            echo "✓ Busca: Todas AZULES mejores"
            echo "✓ Significa: Sin trade-offs, mejora en TODO"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        8)
            clear
            echo -e "${GREEN}FIGURA 8: DYNAMICS & CONTROL${NC}"
            echo "Líneas + bandas sombreadas"
            echo "✓ Busca: Bandas AZULES mucho más ESTRECHAS"
            echo "✓ Significa: Menos variabilidad, más controlable"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        9)
            clear
            echo -e "${GREEN}FIGURA 9: BOX PLOT${NC}"
            echo "Cajas y bigotes para múltiples métricas"
            echo "✓ Busca: Cajas AZULES más PEQUEÑAS"
            echo "✓ Significa: Menos dispersión, más consistencia"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        10)
            clear
            echo -e "${GREEN}FIGURA 10: SCATTER PLOT${NC}"
            echo "Puntos dispersos (correlación)"
            echo "✓ Busca: Nube AZUL más COMPACTA"
            echo "✓ Significa: Mejor control, relación predecible"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        11)
            clear
            echo -e "${GREEN}FIGURA 11: EFFICIENCY BY SECTION${NC}"
            echo "Eficiencia desglosada por secciones"
            echo "✓ Busca: AZUL > ROJA en TODAS"
            echo "✓ Significa: Mejora uniforme en toda pista"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        12)
            clear
            echo -e "${GREEN}FIGURA 12: ADVANCED METRICS${NC}"
            echo "Métricas de control avanzadas"
            echo "✓ Busca: Curvas AZUL más SUAVES"
            echo "✓ Significa: Dinámicas controladas, predecibles"
            echo ""
            read -p "Presiona ENTER..."
            show_figures
            ;;
        0)
            show_menu
            ;;
        *)
            echo "Opción no válida" && sleep 2 && show_figures
            ;;
    esac
}

show_use_cases() {
    clear
    echo -e "${GREEN}🎯 CASOS DE USO REALES${NC}"
    echo ""
    echo -e "${BOLD}CASO 1: Clasificación${NC}"
    echo "¿Cuál setup usar? Optimized (volatility -83.6%)"
    echo ""
    echo -e "${BOLD}CASO 2: Carrera${NC}"
    echo "¿Cuál será más rápido? Optimized (slip -40%)"
    echo ""
    echo -e "${BOLD}CASO 3: Análisis en tiempo real{{NC}"
    echo "¿Por qué predecible? Distribución concentrada (Figura 6)"
    echo ""
    echo -e "${BOLD}CASO 4: Validación estadística${NC}"
    echo "¿Real o casualidad? p < 1e-12 (99.99999999% real)"
    echo ""
    echo -e "${BOLD}CASO 5: Futuro{{NC}"
    echo "¿Dónde mejorar más? Efficiency (+2.32% aún bajo)"
    echo ""
    read -p "Presiona ENTER..."
    show_menu
}

show_reference() {
    clear
    echo -e "${GREEN}📋 TABLA DE REFERENCIA${NC}"
    echo ""
    printf "${BOLD}%-30s %-15s %-15s %-10s${NC}\n" "MÉTRICA" "BASELINE" "OPTIMIZED" "MEJORA"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    printf "%-30s %-15s %-15s %-10s\n" "Glicko Volatility σ" "0.1290" "0.0212" "-83.6%"
    printf "%-30s %-15s %-15s %-10s\n" "Wheel Slip %" "6.25" "3.75" "-40%"
    printf "%-30s %-15s %-15s %-10s\n" "Engine Efficiency %" "94.83" "97.15" "+2.32%"
    echo ""
    echo "p-value: < 1e-12"
    echo "Cohen's d: 3.29"
    echo ""
    read -p "Presiona ENTER..."
    show_menu
}

show_checklist() {
    clear
    echo -e "${GREEN}✅ CHECKLIST${NC}"
    echo ""
    echo -e "${BOLD}¿Entiendes las 3 métricas?${NC}"
    echo "  ☐ Glicko Volatility (-83.6%): predecibilidad"
    echo "  ☐ Wheel Slip (-40%): tracción"
    echo "  ☐ Engine Efficiency (+2.32%): rendimiento"
    echo ""
    echo -e "${BOLD}¿Interpretas cada figura?${NC}"
    echo "  ☐ Fig 5: Líneas suaves = estable"
    echo "  ☐ Fig 6: Curva estrecha = consistente ⭐"
    echo "  ☐ Fig 7: Todas AZUL mejores = sin trade-offs"
    echo "  ☐ Fig 8: Banda estrecha = poco variable"
    echo "  ☐ Fig 9: Caja pequeña = poco disperso"
    echo "  ☐ Fig 10: Nube compacta = relación clara"
    echo "  ☐ Fig 11: AZUL > ROJA todas = consistente"
    echo "  ☐ Fig 12: Curvas suaves = controlable"
    echo ""
    echo -e "${BOLD}¿Confirmas validez?${NC}"
    echo "  ☐ p < 1e-12 (no casualidad)"
    echo "  ☐ Cohen's d = 3.29 (efecto MASIVO)"
    echo ""
    read -p "Presiona ENTER..."
    show_menu
}

# Start
show_menu
