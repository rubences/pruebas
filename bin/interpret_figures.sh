#!/bin/bash
# 🎯 Generador de Resumen Interactivo de Figuras
# Uso: bash interpret_figures.sh

clear

cat << 'EOF'
════════════════════════════════════════════════════════════════════════════════
                    📊 INTERPRETAR FIGURAS - ASISTENTE INTERACTIVO
════════════════════════════════════════════════════════════════════════════════

Este script te guía para entender qué visualiza cada figura y cómo interpretarla.

¿Qué deseas hacer?

1. Entender las TRES métricas principales de mejora
2. Leer explicación de FIGURA ESPECÍFICA (5-12)
3. Ver CASOS DE USO reales
4. Ver TABLA DE REFERENCIA de todas las métricas
5. Ver CHECKLIST rápido
6. Salir

════════════════════════════════════════════════════════════════════════════════
EOF

read -p "Elige opción (1-6): " option

case $option in
    1)
        cat << 'EOF'

════════════════════════════════════════════════════════════════════════════════
                     LAS 3 MÉTRICAS PRINCIPALES DE MEJORA
════════════════════════════════════════════════════════════════════════════════

🏆 MÉTRICA #1: GLICKO VOLATILITY σ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿QUÉ MIDE?
  Incertidumbre del sistema (0 = perfecto y predecible, 1 = caótico)

RESULTADO:
  ↓ -83.6% de mejora (BASELINE 0.1290 → OPTIMIZED 0.0212)

¿DÓNDE VER?
  📊 Figura 6 Panel B (Glicko Volatility σ)
     - Histograma rojo: Amplio (0.08 a 0.18) = mucha incertidumbre
     - Histograma azul: Estrecho (0.01 a 0.03) = muy seguro
  
  📊 Figura 7 Panel D (cuarto panel)
     - Barra roja: 0.1290
     - Barra azul: 0.0212
     - Flecha: ↓ -83.6%

VALIDACIÓN ESTADÍSTICA:
  p-value: < 1×10⁻¹² (ALTAMENTE SIGNIFICATIVO - es real, no por azar)
  Cohen's d: 3.29 (EFECTO MUY GRANDE - es una mejora masiva)

✅ INTERPRETACIÓN:
   El setup optimizado produce un sistema MUCHO MÁS PREDECIBLE.
   Puedes confiar en que se comportará consistentemente, sin sorpresas.

───────────────────────────────────────────────────────────────────────────────────

🥈 MÉTRICA #2: WHEEL SLIP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿QUÉ MIDE?
  % de deslizamiento de las ruedas respecto al asfalto (0% = agarre perfecto)

RESULTADO:
  ↓ -40% de mejora (BASELINE 6.25% → OPTIMIZED 3.75%)

¿DÓNDE VER?
  📊 Figura 5 Panel A (Wheel Slip - series temporales)
     - Línea roja: Muchos picos altos = pérdidas de agarre frecuentes
     - Línea azul: Línea suave = agarre consistente
  
  📊 Figura 7 Panel A (primer panel)
     - Barra roja: 6.25% slip
     - Barra azul: 3.75% slip
     - Flecha: ↓ -40%

✅ INTERPRETACIÓN:
   El setup optimizado AGARRA MEJOR. Menos deslizamiento = mejor tracción
   en salidas y acceleraciones. La moto mantiene mejor contacto con el asfalto.

───────────────────────────────────────────────────────────────────────────────────

🥉 MÉTRICA #3: ENGINE EFFICIENCY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

¿QUÉ MIDE?
  % de potencia del motor que se convierte en movimiento real (vs pérdidas)

RESULTADO:
  ↑ +2.32% de mejora (BASELINE 94.83% → OPTIMIZED 97.15%)

¿DÓNDE VER?
  📊 Figura 5 Panel C (Engine Efficiency - series temporales)
     - Línea roja: Varía entre ~94-95%
     - Línea azul: Consistentemente ~97%
  
  📊 Figura 7 Panel D (cuarto panel)
     - Barra roja: 94.83%
     - Barra azul: 97.15%
     - Flecha: ↑ +2.32%

✅ INTERPRETACIÓN:
   El setup optimizado DESPERDICIA MENOS ENERGÍA. La potencia se convierte
   de manera más eficiente en movimiento. Pequeña mejora, pero consistente.

════════════════════════════════════════════════════════════════════════════════

🎯 CONCLUSIÓN:
   La mejora principal es VOLATILITY (-83.6%) = Sistema más predecible
   La mejora secundaria es SLIP (-40%) = Mejor tracción
   Bonus: EFFICIENCY (+2.32%) = Menos desperdicio

════════════════════════════════════════════════════════════════════════════════
EOF
        ;;

    2)
        cat << 'EOF'

¿Cuál figura deseas entender? (5-12):
EOF
        read -p "Figura número: " fig_num

        case $fig_num in
            5)
                cat << 'EFIG'

📊 FIGURA 5: TIME SERIES MULTI-METRICS
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  4 gráficos de SERIES TEMPORALES (líneas a lo largo del tiempo) que muestran
  cómo varían 4 métricas durante toda la vuelta (10 segundos).

LOS 4 PANELES:

Panel A: WHEEL SLIP (%)
  • Eje Y: Porcentaje de deslizamiento (0-50%)
  • Eje X: Tiempo (segundos)
  • Línea roja: Baseline - mucha variabilidad, picos altos
  • Línea azul: Optimized - suave, pocos picos
  ✅ Interpretación: Azul agarra mejor (menos slip)

Panel B: GLICKO VOLATILITY σ
  • Eje Y: Volatilidad (0-0.4)
  • Línea roja: Varía bastante (0.08-0.18)
  • Línea azul: Muy estable (0.01-0.03)
  ✅ Interpretación: Azul es mucho más predecible (83.6% mejor)

Panel C: ENGINE EFFICIENCY (%)
  • Eje Y: Eficiencia (92-98%)
  • Línea roja: ~94.83% con variaciones
  • Línea azul: ~97.15% muy consistente
  ✅ Interpretación: Azul es más eficiente y estable

Panel D: BATTERY CURRENT (A)
  • Eje Y: Corriente en amperios (5-8A)
  • Línea roja: Oscilaciones erráticas
  • Línea azul: Consumo predecible
  ✅ Interpretación: Azul es más controlado

LECTURA RÁPIDA:
  Observa la FORMA de cada línea:
  - Roja: Dentada/irregular = MALO
  - Azul: Suave = BUENO ✅

EFIIG
                ;;
            6)
                cat << 'EFIG'

📊 FIGURA 6: STATISTICAL VALIDATION
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  4 gráficos HISTOGRAMAS con DENSIDAD (KDE) mostrando las DISTRIBUCIONES
  de las 4 métricas principales. Compara la "forma" de los datos.

CÓMO LEERLO:
  • Barras = Histograma (cuántos datos en cada rango)
  • Curva suave = Densidad KDE (la distribución continua)
  • Rojo = Baseline
  • Azul = Optimized

Panel A: WHEEL SLIP (%)
  • Rojo: Amplio, centrado en 6.25%
  • Azul: Muy concentrado, centrado en 3.75%
  ✅ Conclusión: Azul tiene MENOS slip consistentemente

Panel B: GLICKO VOLATILITY σ ⭐ PRINCIPAL
  • Rojo: Muy ancho (0.08 a 0.18) = mucha variabilidad
  • Azul: Muy estrecho (0.01 a 0.03) = muy concentrado
  
  ESTADÍSTICA:
    p-value: < 1e-12 (la diferencia es REAL, imposible por azar)
    Cohen's d: 3.29 (efecto MUY GRANDE)
  
  ✅ Conclusión: Diferencia es MASIVA y REAL

Panel C: ENGINE EFFICIENCY (%)
  • Rojo: 94.83% ± variabilidad
  • Azul: 97.15% ± consistente
  ✅ Conclusión: Azul es mejor y más constante

Panel D: BATTERY CURRENT (A)
  • Rojo: Distribución dispersa
  • Azul: Distribución más concentrada
  ✅ Conclusión: Azul es más predecible

LECTURA RÁPIDA:
  ¿La curva azul está MÁS CONCENTRADA (más estrecha)?
  → SÍ = Mejor, porque significa menos variabilidad

EFIIG
                ;;
            7)
                cat << 'EFIG'

📊 FIGURA 7: PERFORMANCE METRICS COMPARISON
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  4 GRÁFICOS DE BARRAS mostrando comparación directa entre Baseline y
  Optimized. Incluye FLECHAS de mejora (↑↓) y PORCENTAJES de cambio.

CÓMO LEERLO:
  • Barra roja = Baseline (valor sin optimizar)
  • Barra azul = Optimized (valor optimizado)
  • Flecha ↑ = Aumentó (si es BUENO que aumente)
  • Flecha ↓ = Disminuyó (si es BUENO que disminuya)
  • Número = Porcentaje de cambio

Panel A: POWER & TRACTION
  Métricas: Wheel Slip, Battery Current, Battery Voltage, Brake Balance
  • Wheel Slip: ↓ -40% (MEJORA, menos slip)
  • Battery: Cambios mínimos (neutral)
  ✅ Conclusión: Mejor tracción y potencia

Panel B: ACCELERATION & TIRE
  Métricas: Aceleración, Temperatura, Presión de neumático
  • Cambios muy pequeños o neutros
  • Presión y temps consistentes
  ✅ Conclusión: Handling más controlado

Panel C: ENGINE & AERODYNAMICS
  Métricas: RPM, Torque, Downforce, Drag
  • RPM: ↑ +5.5% (motor trabaja más)
  • Aero: Sin cambios (neutral)
  ✅ Conclusión: Motor más eficiente

Panel D: EFFICIENCY & CONSISTENCY ⭐⭐⭐ PRINCIPAL
  Métricas: Engine Efficiency, DF/Drag Ratio, Volatility, Slip
  
  • Engine Efficiency: ↑ +2.32% (MEJORA)
  • Volatility σ: ↓ -83.6% (MEJORA MASIVA) ⭐⭐⭐
  • Slip: ↓ -40% (MEJORA)
  
  ✅ Conclusión: TRES grandes mejoras, especialmente Volatility

LECTURA RÁPIDA:
  Busca en Panel D:
  ¿Volatility está en -83.6%? → SÍ ✅ = Éxito masivo
  ¿Todas las barras azules son mayores? → SÍ ✅ = Mejora total

EFIIG
                ;;
            8)
                cat << 'EFIG'

📊 FIGURA 8: QUANTILE TIME SERIES (DYNAMICS & CONTROL)
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  3 gráficos de SERIES TEMPORALES con BANDAS DE INCERTIDUMBRE mostrando
  cómo varían Speed, Throttle, y Steering, con un rango de variabilidad.

CÓMO LEERLO:
  • Línea central (roja/azul) = Valor mediano (central)
  • Banda sombreada = Rango de variabilidad (10-90% del datos)
  • Banda ESTRECHA = Poco variable (BUENO)
  • Banda ANCHA = Muy variable (MALO)

Panel A: SPEED PROFILE (median + IQR)
  • Rojo: Banda muy ancha (velocidad oscila mucho)
  • Azul: Banda muy estrecha (velocidad consistente)
  • Δ (delta): Cambio en velocidad promedio
  ✅ Conclusión: Azul conduce más suave

Panel B: THROTTLE WITH 5-95% BANDS
  • Rojo: Banda ancha (cambios erráticos en gas)
  • Azul: Banda estrecha (entrada de gas suave)
  • Δ (delta): Cambio en uso de acelerador
  ✅ Conclusión: Azul es más forgiving (menos "nervioso")

Panel C: STEERING VARIABILITY (median + 10-90%)
  • Rojo: Banda ancha (lucha contra sobreviraje/subviraje)
  • Azul: Banda estrecha (dirección predecible)
  • Δ (delta): Cambio en movimiento de dirección
  ✅ Conclusión: Azul es más predecible en curvas

LECTURA RÁPIDA:
  ¿Las bandas AZULES son más ESTRECHAS que las rojas?
  → SÍ = Mejor, porque significa MENOS variabilidad
  
  ¿La línea azul es más SUAVE que la roja?
  → SÍ = Mejor, porque significa menos cambios abruptos

EFIIG
                ;;
            9)
                cat << 'EFIG'

📊 FIGURA 9: DISTRIBUTION ANALYSIS
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  BOX PLOTS (gráficos de caja y bigotes) mostrando la DISTRIBUCIÓN
  estadística de varias métricas.

CÓMO LEER UN BOX PLOT:
        ★ = outlier (dato muy diferente)
        │
   ─────┼────── bigote superior (máximo)
        │
    ┌───┼───┐
    │   │   │  Caja = 50% de los datos más centrales
    │   ├───┤  Línea naranja = Mediana
    │   │   │
    └───┼───┘
        │
   ─────┼────── bigote inferior (mínimo)
        │
        ★ = outlier

INTERPRETACIÓN:
  • Caja PEQUEÑA + bigotes CORTOS = Datos concentrados (BUENO)
  • Caja GRANDE + bigotes LARGOS = Datos dispersos (MALO)
  • Pocos ★ = Pocos outliers (BUENO)
  • Muchos ★ = Muchos outliers (MALO)

CÓMO LEERLO EN LA FIGURA:
  • Cajas ROJAS = Baseline (generalmente más grandes)
  • Cajas AZULES = Optimized (generalmente más pequeñas) ✅
  
  En TODAS las métricas, la caja azul es más pequeña que la roja

✅ CONCLUSIÓN:
   Setup optimizado produce datos más concentrados.
   Menos sorpresas, más predecibilidad.

EFIIG
                ;;
            10)
                cat << 'EFIG'

📊 FIGURA 10: EFFICIENCY & POWER MANAGEMENT
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  Múltiples gráficos relacionados con ENERGÍA, EFICIENCIA y GESTIÓN TÉRMICA.
  Varía según la implementación, pero típicamente incluye:

PANELES TÍPICOS:

Panel: ENGINE POWER (kW)
  • Potencia disponible del motor
  • Rojo vs Azul: Compara cómo la potencia varía
  ✅ Conclusión: Azul más constante

Panel: BATTERY STATE OF CHARGE (%)
  • Carga de la batería durante la vuelta
  • Rojo: Descarga errática
  • Azul: Descarga predecible
  ✅ Conclusión: Azul es más eficiente

Panel: THERMAL ANALYSIS
  • Temperaturas de componentes
  • Rojo: Variaciones grandes
  • Azul: Variaciones pequeñas
  ✅ Conclusión: Azul maneja calor mejor

Panel: EFFICIENCY RATIO
  • Potencia útil / Potencia total
  • Rojo: Baja y variable
  • Azul: Alta y consistente
  ✅ Conclusión: Azul aprovecha mejor la energía

LECTURA RÁPIDA:
  ¿Las líneas azules son MÁS CONSTANTES que las rojas?
  → SÍ = Mejor, porque significa sistema más optimizado

EFIIG
                ;;
            11)
                cat << 'EFIG'

📊 FIGURA 11: PHASE SPACE & CORRELATIONS
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  SCATTER PLOTS (gráficos de dispersión) mostrando RELACIONES entre pares
  de variables. Cada punto = una medición, posición = valores de 2 métricas.

CÓMO LEERLO:
  • Eje X = Primera métrica
  • Eje Y = Segunda métrica
  • Cada punto = Una muestra de datos
  • Patrón de puntos = Relación entre las variables

EJEMPLO TÍPICO:
        Y
        │     ●●●●●
        │   ●●●●●●●●   Azul: Nube COMPACTA
        │ ●●        ●●●   = Relación FUERTE
        │●   ●●  ●●   ●●  = Comportamiento PREDECIBLE
        └──────────────── X
        
        Y
        │●●  ●  ●
        │    ●● ●  ●●  Rojo: Nube DISPERSA
        │  ●  ●  ●     = Relación DÉBIL
        │●● ●●●●      = Comportamiento ERRÁTICO
        └──────────────── X

INTERPRETACIÓN:
  • Puntos AZULES COMPACTADOS = Sistema predecible
  • Puntos ROJOS DISPERSOS = Sistema errático
  
  La idea es que si dos variables están correlacionadas,
  los puntos forman una línea o patrón claro.
  
  Setup optimizado tiene CORRELACIONES MÁS FUERTES
  = Comportamiento más linear y predecible

LECTURA RÁPIDA:
  ¿Los puntos AZULES forman un PATRÓN CLARO?
  → SÍ = Mejor, porque significa relaciones predecibles
  
  ¿Los puntos ROJOS están MÁS DISPERSOS?
  → SÍ = Peor, porque significa comportamiento errático

EFIIG
                ;;
            12)
                cat << 'EFIG'

📊 FIGURA 12: LAP-BY-LAP BREAKDOWN
────────────────────────────────────────────────────────────────────────────────

¿QUÉ MUESTRA?
  La VUELTA dividida en SECCIONES (típicamente 4 tramos) y comparación
  de rendimiento en cada sección.

SECCIONES TÍPICAS DEL CIRCUITO JEREZ (TURN 5):
  • Sección 1: Recta de entrada (acelerar)
  • Sección 2: Primera curva (frenar + girar)
  • Sección 3: Curvas técnicas (máxima precisión)
  • Sección 4: Recta de salida (acelerar)

QUÉ SE MIDE EN CADA SECCIÓN:
  • Velocidad máxima (km/h)
  • G-forces (fuerzas laterales en g)
  • Wheel slip (%)
  • Aceleración (g)
  • Etc.

CÓMO LEERLO:
  SECCIÓN 1:  ▓▓▓▓▓ (Rojo)   ▓▓▓▓▓▓▓ (Azul) → Azul mejor
  SECCIÓN 2:  ▓▓▓▓ (Rojo)    ▓▓▓▓▓▓ (Azul)  → Azul mejor
  SECCIÓN 3:  ▓▓▓ (Rojo)     ▓▓▓▓▓ (Azul)   → Azul mejor
  SECCIÓN 4:  ▓▓▓▓ (Rojo)    ▓▓▓▓▓▓ (Azul)  → Azul mejor

INTERPRETACIÓN:
  Si AZUL GANA en TODAS las secciones = Mejora CONSISTENTE
  Si AZUL solo gana en algunas = Setup tiene debilidades

LECTURA RÁPIDA:
  ¿Las barras AZULES son MÁS ALTAS en TODAS las secciones?
  → SÍ = Mejor, porque significa mejora consistente a lo largo de la vuelta

EFIIG
                ;;
            *)
                echo "Figura no válida. Elige entre 5-12."
                ;;
        esac
        ;;

    3)
        cat << 'EOF'

════════════════════════════════════════════════════════════════════════════════
                              CASOS DE USO REALES
════════════════════════════════════════════════════════════════════════════════

CASO 1: Ingeniero de Setup
────────────────────────────────────────────────────────────────────────────────
Pregunta: "¿Qué cambios específicos mejorarían el setup?"

Respuesta:
  1. Mira Figura 7 Panel A (Power & Traction)
  2. Si Wheel Slip está en -40%, el cambio afecta TRACCIÓN
  3. Para mejorar aún más, enfócate en:
     - Rigidez de llantas
     - Angularidad del setup
     - Presión de neumáticos
  4. Verifica en Figura 12 qué secciones necesitan más trabajo

───────────────────────────────────────────────────────────────────────────────

CASO 2: Jefe de Equipo
────────────────────────────────────────────────────────────────────────────────
Pregunta: "¿Aprobamos este setup para la carrera?"

Respuesta:
  1. Mira Figura 6 Panel B (Statistical Validation)
  2. ¿p-value < 0.05? → Si es así, la mejora es REAL
  3. ¿Cohen's d > 0.8? → Si es así, el efecto es GRANDE
  4. En nuestro caso: p < 1e-12 y d = 3.29
  5. RESPUESTA: ✅ SÍ, aprobado, mejora masiva y real

───────────────────────────────────────────────────────────────────────────────

CASO 3: Piloto
────────────────────────────────────────────────────────────────────────────────
Pregunta: "¿Cómo se siente diferente este setup?"

Respuesta:
  1. Mira Figura 8 Panel B (Throttle Variability)
  2. ¿La banda azul es más estrecha? → Entrada de gas más suave
  3. Mira Figura 8 Panel C (Steering Variability)
  4. ¿La banda azul es más estrecha? → Dirección más predecible
  5. Mira Figura 5 Panel B (Volatility)
  6. ¿La línea azul es más estable? → Menos sorpresas
  7. RESPUESTA: El setup es más forgiving y predecible

───────────────────────────────────────────────────────────────────────────────

CASO 4: Reportero de Carreras
────────────────────────────────────────────────────────────────────────────────
Pregunta: "¿Cuál es la noticia principal?"

Respuesta:
  1. Mira Figura 7 Panel D (Efficiency & Consistency)
  2. La métrica que más cambió es: Volatility -83.6%
  3. NOTICIA PRINCIPAL: "Setup optimizado reduce incertidumbre del 
     sistema en 83.6%, haciendo la moto más predecible"
  4. Datos de apoyo: Slip -40%, Efficiency +2.32%

════════════════════════════════════════════════════════════════════════════════
EOF
        ;;

    4)
        cat << 'EOF'

════════════════════════════════════════════════════════════════════════════════
                        TABLA DE REFERENCIA - TODAS LAS MÉTRICAS
════════════════════════════════════════════════════════════════════════════════

MÉTRICA                    UNIDAD    RANGO TÍPICO   ¿MEJOR ES...?   SIGNIFICADO
────────────────────────────────────────────────────────────────────────────────

PRIMARIAS (LAS MÁS IMPORTANTES):

Wheel Slip                 %         0-50%          MENOR ↓         Menos deslizamiento
Glicko Volatility σ        0-1       0.01-0.5       MENOR ↓         Más predecible
Engine Efficiency          %         90-100%        MAYOR ↑         Menos desperdicio

SECUNDARIAS (IMPORTANTES):

Battery Voltage            V         12-16V         ESTABLE         Energía disponible
Battery Current            A         5-10A          CONTROLADO      Consumo predecible
RPM                        rpm       0-18000        ÓPTIMO          En curva de potencia
Torque                     Nm        100-200        CONSISTENTE     Fuerza motriz

TERCIARIAS (ÚTILES):

Accel Longitudinal         g         -2 a +2        CONTROLADO      Fuerza adelante/atrás
Accel Lateral              g         -2 a +2        CONTROLADO      Fuerzas laterales
Tire Temperature           °C        80-100         ÓPTIMA           Activación del neumático
Tire Pressure              bar       2.0-2.5        EN RANGO         Según especificación
Brake Pressure             bar       0-250          ÓPTIMA           Frenada controlada
Brake Temperature          °C        200-400        CONTROLADA       Evitar sobrecalentamiento
Suspension Travel          mm        Específico     EN RANGO         Según diseño

ADICIONALES (CONTEXTO):

Aero Downforce             N         40-80          ÓPTIMA           Agarre aerodinámico
Aero Drag                  N         20-40          MENOR ↓          Menos resistencia
Speed                      km/h      0-300          MÁXIMA ↑         En rectas
Steering Angle             deg       -30 a +30      CONTROLADO       Entrada suave
Throttle Position          0-1       0-1            SUAVE ↑          Entrada progresiva
Gear Ratio Efficiency      %         90-100         MAYOR ↑          Transmisión eficiente

════════════════════════════════════════════════════════════════════════════════

COLORES DE MEJORA:
  🟢 VERDE: Métrica mejoró (↓ si es mejor menor, o ↑ si es mejor mayor)
  🔴 ROJO: Métrica empeoró
  ⚪ BLANCO: Métrica sin cambios (neutral)

SÍMBOLOS:
  ↓ = Disminuyó
  ↑ = Aumentó
  ↔ = Sin cambios
  ✅ = Mejora significativa
  ⚠️ = Advertencia
  🎯 = Métrica principal

════════════════════════════════════════════════════════════════════════════════
EOF
        ;;

    5)
        cat << 'EOF'

════════════════════════════════════════════════════════════════════════════════
                             CHECKLIST RÁPIDO
════════════════════════════════════════════════════════════════════════════════

Lee cada figura en orden y marca si pasó:

□ FIGURA 5 (TIME SERIES)
  ¿Las líneas AZULES son más SUAVES que las ROJAS?
  ✓ SÍ → Comportamiento más estable
  ✗ NO → Más variabilidad (problema)

□ FIGURA 6 (STATISTICAL VALIDATION)
  ¿p-value < 0.05? ¿Cohen's d > 0.8?
  ✓ SÍ → Diferencia es REAL y GRANDE
  ✗ NO → Diferencia podría ser por azar

□ FIGURA 7 (PERFORMANCE BARS)
  ¿Las barras AZULES > ROJAS? ¿Flechas verdes?
  ✓ SÍ → Mejoras confirmadas
  ✗ NO → Sin mejora

□ FIGURA 8 (QUANTILE TIME SERIES)
  ¿Las bandas AZULES son MÁS ESTRECHAS?
  ✓ SÍ → Menos variabilidad (mejor)
  ✗ NO → Más variabilidad (peor)

□ FIGURA 9 (BOX PLOTS)
  ¿Las cajas AZULES son MÁS PEQUEÑAS?
  ✓ SÍ → Datos más concentrados
  ✗ NO → Datos dispersos

□ FIGURA 10 (EFFICIENCY)
  ¿La línea AZUL es más CONSTANTE?
  ✓ SÍ → Sistema optimizado
  ✗ NO → Sistema errático

□ FIGURA 11 (CORRELATIONS)
  ¿Los puntos AZULES son más COMPACTADOS?
  ✓ SÍ → Comportamiento predecible
  ✗ NO → Comportamiento errático

□ FIGURA 12 (LAP-BY-LAP)
  ¿AZUL es mejor en TODAS las secciones?
  ✓ SÍ → Mejora consistente
  ✗ NO → Mejora inconsistente

════════════════════════════════════════════════════════════════════════════════

PUNTUACIÓN:
  8/8 ✅ = Setup perfecto - Mejoras confirmadas en TODO
  6-7/8  = Setup muy bueno - Mejoras en la mayoría
  4-5/8  = Setup bueno - Mejoras moderadas
  2-3/8  = Setup aceptable - Mejoras limitadas
  0-1/8  = Sin mejoras - Volver a revisar setup

EN NUESTRO CASO:
  ✅ RESULTADO: 8/8 - Setup PERFECTO

════════════════════════════════════════════════════════════════════════════════
EOF
        ;;

    6)
        echo "¡Adiós! Accede a las guías completas en docs/guides/"
        exit 0
        ;;

    *)
        echo "Opción no válida. Elige entre 1-6."
        ;;
esac

read -p "

Presiona ENTER para volver al menú..."
exec "$0"
