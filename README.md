# 🎰 Gemini Royal Slots 5x4 HD — Plataforma Unificada de Simulación de Casino

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Pygame](https://img.shields.io/badge/Engine-Pygame%2060%20FPS-green)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter%20Classic-orange)
![Resolution](https://img.shields.io/badge/Resolution-1366x768%20HD-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

Simulador profesional de máquina tragamonedas multilínea de casino ($5\text{ columnas} \times 4\text{ filas}$) que unifica la experiencia interactiva de alta definición a $60\text{ FPS}$ en **Pygame** con la edición clásica de escritorio en **Tkinter + Pillow**.

---

## 🌟 Características Principales del Motor Fisionado

- **Arquitectura de Motor Dual**:
  - **Pygame HD (`src/slots.py` / `src/slots_pygame.py`)**: Interfaz cinematográfica a 60 FPS ($1366 \times 768$) con sprites PNG escalados suavemente, física de partículas, giro secuencial de carretes y trazado de líneas ganadoras en tiempo real.
  - **Tkinter Classic (`src/slot_tkinter.py`)**: Modo ligero y portátil para cualquier entorno de escritorio sin dependencias pesadas de aceleración gráfica.
  - **Lanzador Unificado (`src/main.py`)**: Permite alternar entre motores mediante parámetros de línea de comandos (`--engine pygame` o `--engine tkinter`).

- **Doble Modalidad de Evaluación de Premios**:
  - **50 Líneas de Pago Geométricas (`PAYLINES`)**: Recorre las 50 trayectorias vectoriales de izquierda a derecha, sustituye comodines (*Wild*) y calcula multiplicadores por longitud (0.60x en 3 coincidencias, 0.80x en 4, 1.00x en 5).
  - **1024 Formas de Ganar (*All-Ways to Win*)**: Calcula combinaciones de símbolos adyacentes mediante producto cartesiano ($\prod n_c$).
  - Selector en caliente entre `10`, `20`, `50` líneas y `1024` formas.

- **Renderizado de Sprites HD (`assets/`)**:
  - Gráficos transparentes de alta resolución reescalados dinámicamente con preservación de canal alfa (`wild.png`, `Scatter.png`, `heart.png`, `diamond.png`, `fruit.png`, `A.png`, `B.png`, `C.png`, `D.png`).
  - Fallback gráfico inteligente en caso de ausencia de recursos.

- **Trazado Vectorial de Líneas Ganadoras**:
  - Dibuja sobre la cuadrícula las líneas vectoriales premiadas con colores diferenciados y badges circulares numerados indicando la línea activa ganadora.

- **Modo Bono de Giros Gratis (*Scatter*)**:
  - Al acumular 3, 4 o 5 símbolos Scatter en columnas distintas, otorga **10, 25 o 100 Giros Gratis**.
  - Durante el modo bono, la iluminación ambiental cambia a rojo carmesí, se aplica un multiplicador de ganancia del **1.2x** y los giros se ejecutan automáticamente en cascada.

- **Efectos Visuales y Física de Partículas**:
  - Explosiones de monedas doradas con vector de aceleración gravitatoria ($\Delta v_y = +0.32$), dispersión lateral y desvanecimiento alfa.
  - Contador de saldo animado suavizado (*Rolling balance counter*).
  - Textos flotantes de premio con elevación y atenuación gradual.

- **Audio Procedural Sintetizado**:
  - Sistema de audio en memoria RAM que genera ondas sinusoidales para clicks de giro, frenado de carretes, monedas y fanfarrias sin requerir archivos de sonido externos.

- **Cajero y Panel de Auditoría**:
  - Pantalla de depósito interactiva con atajos rápidos (+$500, +$1,000, +$5,000) y recarga en caliente durante el juego.
  - Panel lateral con auditoría detallada de cada línea premiada y métricas de la sesión.

---

## 🗂️ Estructura del Proyecto

```text
Slots/
├── assets/                       # Sprites gráficos en alta resolución
│   ├── wild.png                  # Comodín / Sustituto (pago 200x)
│   ├── Scatter.png               # Dispersor / Bono Giros Gratis
│   ├── heart.png                 # Símbolo Premium Corazón (pago 120x)
│   ├── diamond.png               # Símbolo Premium Diamante (pago 90x)
│   ├── fruit.png                 # Símbolo Fruta (pago 60x)
│   ├── A.png                     # Denominación A (pago 30x)
│   ├── B.png                     # Denominación B (pago 20x)
│   ├── C.png                     # Denominación C (pago 15x)
│   └── D.png                     # Denominación D (pago 10x)
│
├── src/
│   ├── main.py                   # Lanzador unificado con selector de motor
│   ├── slots.py                  # Motor principal Pygame 5x4 HD 60 FPS
│   ├── slots_pygame.py           # Alias directo para el motor Pygame
│   └── slot_tkinter.py           # Edición de escritorio en Tkinter + Pillow
│
├── requirements.txt              # Dependencias (pygame, pillow)
├── DOCUMENTACION_TECNICA.md      # Especificación matemática, modelos y arquitectura
├── .gitignore                    # Exclusiones de control de versiones
└── LICENSE                       # Licencia MIT
```

---

## ⚙️ Instalación y Ejecución

### 1. Activar Entorno Virtual e Instalar Dependencias
```bash
python -m venv .venv
# En Windows:
.venv\Scripts\activate

# Instalar requerimientos:
pip install -r requirements.txt
```

### 2. Ejecución

- **Lanzador General (Recomendado - Inicia Pygame HD)**:
  ```bash
  python src/main.py
  ```

- **Iniciar en modo clásico (Tkinter)**:
  ```bash
  python src/main.py --engine tkinter
  # o directamente:
  python src/slot_tkinter.py
  ```

- **Iniciar directamente el motor Pygame**:
  ```bash
  python src/slots.py
  ```

---

## 🎮 Controles y Atajos de Teclado (Motor Pygame)

| Control | Acción |
| :--- | :--- |
| **`ESPACIO` / `ENTER`** | Iniciar giro (*Spin*) |
| **`M`** | Apuesta Máxima instantánea (*Max Bet*) |
| **`L`** | Alternar entre 10, 20, 50 Líneas y 1024 Formas |
| **`FLECHA ARRIBA` / `+`** | Incrementar valor de apuesta por línea |
| **`FLECHA ABAJO` / `-`** | Disminuir valor de apuesta por línea |
| **`C`** | Abrir Cajero para depositar más créditos |
| **`ESC`** | Volver al cajero o salir |

---

## 📄 Licencia

Desarrollado por **Roberto Alejandro Chagra Martínez**.  
Distribuido bajo la licencia **MIT**. Consulta el archivo `LICENSE` para más información.
