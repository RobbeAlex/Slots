"""
🎰 GEMINI ROYAL CASINO SLOTS 5x4 HD 🎰
Simulador Profesional de Máquina Tragamonedas en Pygame (60 FPS, 1366x768)
Autor: Roberto Alejandro Chagra Martínez

Características Principales:
- Motor Dual: Evaluación por 50 Líneas Geométricas (Paylines) y 1024 Formas (All-Ways).
- Gráficos HD: Renderizado de sprites PNG de alta resolución con escalado suave (assets/*.png).
- Trazado Vectorial de Líneas: Dibuja las líneas ganadoras con badges numerados directamente en la pantalla.
- Física de Partículas: Explosión de monedas doradas y textos flotantes con desvanecimiento alfa.
- Modo Bono de Giros Gratis (Scatter): Disparador automático de giros, multiplicador y ambientación visual.
- Audio Procedural Integrado: Efectos de sonido sintetizados en memoria (no requiere archivos de audio externos).
- Cajero / Depósito Dinámico: Gestión de saldo en tiempo real, apuestas personalizables y botón MAX BET.
- Panel Lateral de Auditoría: Desglose detallado de combinaciones ganadoras y estadísticas de sesión.
"""

import os
import sys
import math
import time
import struct
import random
import pygame

# ==========================================
# CONFIGURACIÓN GENERAL Y CONSTANTES
# ==========================================
ANCHO, ALTO = 1366, 768
FPS = 60
FILAS = 4
COLUMNAS = 5

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Paleta de Colores Casino Premium
NEGRO_FONDO = (12, 12, 18)
FONDO_BONO = (32, 6, 14)
ORO = (255, 215, 0)
ORO_BRILLANTE = (255, 235, 80)
ORO_OSCURO = (180, 140, 20)
VERDE_EXITO = (46, 204, 113)
ROJO_CASINO = (231, 76, 60)
ROJO_HOVER = (255, 100, 85)
AZUL_ACENTO = (41, 128, 185)
BLANCO = (245, 245, 250)
GRIS_OSCURO = (28, 30, 40)
GRIS_CELDA = (38, 40, 52)
GRIS_BORDE = (60, 65, 80)
TEXTO_MUTED = (160, 165, 180)

LINE_COLORS = [
    (255, 23, 68), (0, 230, 118), (41, 121, 255), (255, 234, 0),
    (255, 145, 0), (213, 0, 249), (0, 229, 255), (255, 82, 82),
    (105, 240, 174), (124, 77, 255), (255, 171, 0), (0, 176, 255)
]

# Configuración de Símbolos, Probabilidades y Valores
SYMBOL_NAMES = ["Wild", "Scatter", "Heart", "Diamond", "Fruit", "A", "B", "C", "D"]

SYMBOL_WEIGHTS = {
    "Wild": 8,
    "Scatter": 8,
    "Heart": 12,
    "Diamond": 14,
    "Fruit": 18,
    "A": 22,
    "B": 26,
    "C": 30,
    "D": 34,
}

SYMBOL_BASE_VALUES = {
    "Wild": 200,
    "Scatter": 0,
    "Heart": 120,
    "Diamond": 90,
    "Fruit": 60,
    "A": 30,
    "B": 20,
    "C": 15,
    "D": 10,
}

# 50 Líneas de Pago Vectoriales
PAYLINES = [
    [0, 0, 0, 0, 0], [1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3],
    [0, 1, 2, 1, 0], [3, 2, 1, 2, 3], [1, 2, 3, 2, 1], [2, 1, 0, 1, 2],
    [0, 0, 1, 2, 2], [3, 3, 2, 1, 1], [1, 0, 0, 0, 1], [2, 3, 3, 3, 2],
    [0, 1, 1, 1, 0], [3, 2, 2, 2, 3], [1, 2, 1, 2, 1], [2, 1, 2, 1, 2],
    [0, 2, 0, 2, 0], [3, 1, 3, 1, 3], [0, 1, 0, 1, 0], [3, 2, 3, 2, 3],
    [0, 1, 2, 3, 2], [3, 2, 1, 0, 1], [1, 2, 3, 2, 3], [2, 1, 0, 1, 0],
    [0, 0, 2, 0, 0], [3, 3, 1, 3, 3], [1, 1, 3, 1, 1], [2, 2, 0, 2, 2],
    [0, 2, 2, 2, 0], [3, 1, 1, 1, 3], [1, 0, 2, 0, 1], [2, 3, 1, 3, 2],
    [0, 3, 0, 3, 0], [3, 0, 3, 0, 3], [1, 3, 1, 3, 1], [2, 0, 2, 0, 2],
    [0, 0, 3, 0, 0], [3, 3, 0, 3, 3], [2, 2, 1, 1, 0], [1, 1, 2, 2, 3],
    [0, 1, 3, 1, 0], [3, 2, 0, 2, 3], [0, 2, 1, 2, 0], [3, 1, 2, 1, 3],
    [1, 0, 1, 0, 1], [2, 3, 2, 3, 2], [2, 1, 1, 1, 2], [1, 2, 2, 2, 1],
    [0, 3, 3, 3, 0], [3, 0, 0, 0, 3]
]

# ==========================================
# MOTOR DE AUDIO PROCEDURAL (SINTETIZADO)
# ==========================================
class SoundFXManager:
    """Genera efectos de sonido mediante síntesis procedural en memoria RAM."""
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
            self._sintetizar_efectos()
        except Exception as e:
            print(f"Aviso de audio: Modo silencioso activado ({e})")
            self.enabled = False

    def _generar_onda(self, freq_inicio, freq_fin, duracion, volumen=0.25, tipo="seno"):
        sample_rate = 22050
        n_samples = int(sample_rate * duracion)
        buf = bytearray()
        for i in range(n_samples):
            t = i / sample_rate
            factor = i / n_samples
            freq = freq_inicio + (freq_fin - freq_inicio) * factor
            if tipo == "seno":
                val = math.sin(2 * math.pi * freq * t)
            elif tipo == "cuadrada":
                val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            else:
                val = (2 * (freq * t - math.floor(0.5 + freq * t)))
            # Envolvente para evitar clicks
            env = min(1.0, factor * 10) * min(1.0, (1.0 - factor) * 10)
            muestra = int(32767 * volumen * val * env)
            buf.extend(struct.pack('<h', max(-32768, min(32767, muestra))))
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _sintetizar_efectos(self):
        try:
            self.sounds["spin"] = self._generar_onda(300, 600, 0.08, 0.15)
            self.sounds["stop"] = self._generar_onda(220, 110, 0.09, 0.25)
            self.sounds["win"] = self._generar_onda(523, 784, 0.25, 0.3)
            self.sounds["bonus"] = self._generar_onda(440, 880, 0.45, 0.35)
            self.sounds["coin"] = self._generar_onda(880, 1320, 0.12, 0.2)
        except Exception:
            pass

    def play(self, nombre):
        if not self.enabled or nombre not in self.sounds:
            return
        try:
            self.sounds[nombre].play()
        except Exception:
            pass

    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

# ==========================================
# COMPONENTES DE INTERFAZ GRÁFICA
# ==========================================
class Boton:
    def __init__(self, x, y, ancho, alto, texto, color_base, color_hover, font_size=20, border_radius=12):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.texto = texto
        self.color_base = color_base
        self.color_hover = color_hover
        self.border_radius = border_radius
        self.font_size = font_size
        self.fuente = pygame.font.SysFont("Arial Black", font_size)

    def dibujar(self, pantalla):
        cursor = pygame.mouse.get_pos()
        hover = self.rect.collidepoint(cursor)
        color = self.color_hover if hover else self.color_base

        # Sombra sutil
        sombra = self.rect.copy()
        sombra.y += 3
        pygame.draw.rect(pantalla, (8, 8, 12), sombra, border_radius=self.border_radius)

        pygame.draw.rect(pantalla, color, self.rect, border_radius=self.border_radius)
        borde_color = ORO if hover else (180, 190, 205)
        pygame.draw.rect(pantalla, borde_color, self.rect, 2, border_radius=self.border_radius)

        txt_surf = self.fuente.render(self.texto, True, BLANCO)
        pantalla.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def clicado(self, evento):
        return evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and self.rect.collidepoint(evento.pos)

class InputBox:
    def __init__(self, x, y, w, h, texto_inicial="1000"):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto_inicial
        self.activo = False
        self.fuente = pygame.font.SysFont("Consolas", 36, bold=True)

    def manejar_evento(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.activo = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.activo:
            if event.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            elif event.unicode.isdigit() and len(self.texto) < 7:
                self.texto += event.unicode

    def dibujar(self, pantalla):
        color = ORO if self.activo else GRIS_BORDE
        pygame.draw.rect(pantalla, GRIS_CELDA, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, color, self.rect, 3, border_radius=10)
        txt = self.fuente.render(f"${self.texto}", True, BLANCO if self.texto else (120, 120, 120))
        pantalla.blit(txt, (self.rect.x + 20, self.rect.y + (self.rect.h - txt.get_height()) // 2))

class EfectoParticula:
    """Partícula física con gravedad, dispersión y desvanecimiento alfa."""
    def __init__(self, x, y, tipo="particula", valor=""):
        self.x, self.y = float(x), float(y)
        self.tipo = tipo
        self.valor = valor
        self.vida = 80
        self.vida_max = 80
        if tipo == "particula":
            self.vx = random.uniform(-6, 6)
            self.vy = random.uniform(-9, -2)
            self.color = random.choice([ORO, ORO_BRILLANTE, (255, 255, 200)])
            self.radio = random.randint(4, 7)
        else:
            self.vx = 0.0
            self.vy = -1.4
            self.color = VERDE_EXITO

    def actualizar(self):
        self.vida -= 1
        self.x += self.vx
        self.y += self.vy
        if self.tipo == "particula":
            self.vy += 0.32  # Gravedad

    @property
    def alpha(self):
        return max(0, min(255, int((self.vida / self.vida_max) * 255)))

# ==========================================
# CLASE PRINCIPAL: MOTOR DEL SIMULADOR
# ==========================================
class SlotMachineHD:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Gemini Royal Slots 5x4 HD — Multilínea & All-Ways")
        self.clock = pygame.time.Clock()

        # Fuentes tipográficas
        self.f_peq = pygame.font.SysFont("Arial", 14, bold=True)
        self.f_med = pygame.font.SysFont("Arial Black", 20)
        self.f_tit = pygame.font.SysFont("Arial Black", 32)
        self.f_big = pygame.font.SysFont("Arial Black", 48)
        self.f_mono = pygame.font.SysFont("Consolas", 13)

        self.audio = SoundFXManager()

        # Configuración de Grilla
        self.grid_x = 55
        self.grid_y = 75
        self.celda_w = 155
        self.celda_h = 115
        self.gap = 8

        # Cargar Assets
        self.symbol_surfaces = {}
        self.cargar_assets()

        # Estados y Saldo
        self.estado = "DEPOSITO"  # "DEPOSITO" o "JUEGO"
        self.saldo = 1000.0
        self.saldo_visual = 1000.0

        # Opciones de Líneas/Modos: 10, 20, 50 (Paylines) o 1024 (All-Ways)
        self.modos_lineas = [10, 20, 50, 1024]
        self.idx_modo = 2  # Por defecto 50 líneas
        self.bet_por_linea = 1  # De 1 a 100
        self.auto_spin = False

        # Modo Bono (Giros Gratis)
        self.modo_bono = False
        self.free_spins = 0
        self.total_bonus_win = 0

        # Animación de Carretes
        self.girando = False
        self.tiempo_inicio_giro = 0
        self.carretes_detenidos = [True] * COLUMNAS
        self.cuadricula = [[self.obtener_simbolo_aleatorio() for _ in range(FILAS)] for _ in range(COLUMNAS)]

        # Resultados de la última jugada
        self.ultimo_premio = 0
        self.detalles_ganancias = []
        self.lineas_a_dibujar = []
        self.mensaje_estado = "¡Bienvenido a Gemini Royal Slots! Configura tu apuesta y gira."

        # Estadísticas de Sesión
        self.stats_giros = 0
        self.stats_mayor_premio = 0

        # Efectos visuales activos
        self.efectos = []

        # Interfaz de Cajero
        self.input_deposito = InputBox(ANCHO // 2 - 160, 340, 320, 65, "1000")
        self.btn_entrar = Boton(ANCHO // 2 - 160, 430, 320, 65, "INGRESAR AL CASINO", (39, 174, 96), (46, 204, 113), 22)

        # Botones Rápidos Cajero
        self.btn_dep_500 = Boton(ANCHO // 2 - 250, 515, 150, 45, "+$500", AZUL_ACENTO, (52, 152, 219), 16)
        self.btn_dep_1000 = Boton(ANCHO // 2 - 80, 515, 160, 45, "+$1,000", AZUL_ACENTO, (52, 152, 219), 16)
        self.btn_dep_5000 = Boton(ANCHO // 2 + 100, 515, 150, 45, "+$5,000", AZUL_ACENTO, (52, 152, 219), 16)

        # Botones de la Consola de Juego
        y_ctrl = 645
        self.btn_cajero = Boton(55, y_ctrl + 10, 110, 50, "CAJERO", GRIS_BORDE, (90, 95, 115), 14)
        self.btn_sonido = Boton(175, y_ctrl + 10, 110, 50, "AUDIO: ON", GRIS_BORDE, (90, 95, 115), 13)

        self.btn_lineas = Boton(305, y_ctrl + 10, 150, 50, "50 LÍNEAS", AZUL_ACENTO, (52, 152, 219), 16)
        self.btn_bet_menos = Boton(470, y_ctrl + 10, 50, 50, "-", GRIS_BORDE, (90, 95, 115), 24)
        self.btn_bet_mas = Boton(530, y_ctrl + 10, 50, 50, "+", GRIS_BORDE, (90, 95, 115), 24)

        self.btn_max = Boton(600, y_ctrl, 140, 65, "MAX BET", (142, 68, 173), (155, 89, 182), 18)
        self.btn_spin = Boton(755, y_ctrl - 5, 160, 75, "GIRAR", ROJO_CASINO, ROJO_HOVER, 26)

    def cargar_assets(self):
        """Carga y escala los sprites PNG optimizados para la cuadrícula 5x4."""
        target_size = (self.celda_w - 20, self.celda_h - 18)
        for sym in SYMBOL_NAMES:
            img_path = os.path.join(ASSETS_DIR, f"{sym}.png")
            if os.path.exists(img_path):
                try:
                    surf = pygame.image.load(img_path).convert_alpha()
                    surf_scaled = pygame.transform.smoothscale(surf, target_size)
                    self.symbol_surfaces[sym] = surf_scaled
                except Exception as e:
                    print(f"Error cargando asset {sym}: {e}")
                    self.symbol_surfaces[sym] = None
            else:
                self.symbol_surfaces[sym] = None

    def obtener_simbolo_aleatorio(self):
        bolsa = []
        for s, peso in SYMBOL_WEIGHTS.items():
            bolsa.extend([s] * peso)
        return random.choice(bolsa)

    def apuesta_total(self):
        lineas = self.modos_lineas[self.idx_modo]
        factor_lineas = 50 if lineas == 1024 else lineas
        return factor_lineas * self.bet_por_linea

    def iniciar_giro(self):
        apuesta = self.apuesta_total()
        if not self.modo_bono:
            if self.saldo < apuesta:
                self.mensaje_estado = "¡Saldo insuficiente! Deposita fondos en el cajero."
                return
            self.saldo -= apuesta
        else:
            self.free_spins -= 1

        self.girando = True
        self.tiempo_inicio_giro = pygame.time.get_ticks()
        self.carretes_detenidos = [False] * COLUMNAS
        self.lineas_a_dibujar.clear()
        self.detalles_ganancias.clear()
        self.stats_giros += 1
        self.mensaje_estado = "Los carretes están girando..."
        self.audio.play("spin")

    def calcular_premio(self):
        """Calcula el pago combinando el motor de 50 Líneas de Pago y el de 1024 Formas."""
        modo = self.modos_lineas[self.idx_modo]
        total_ganado = 0
        detalles = []
        lineas_destacadas = []

        if modo == 1024:
            # Motor 1024 Formas (All-Ways)
            for simb in SYMBOL_NAMES:
                if simb == "Scatter":
                    continue
                conteo_cols = []
                for col in self.cuadricula:
                    n = col.count(simb) + col.count("Wild")
                    if n == 0:
                        break
                    conteo_cols.append(n)
                if len(conteo_cols) >= 3:
                    formas = 1
                    for c in conteo_cols:
                        formas *= c
                    multiplicador = {3: 0.60, 4: 0.80, 5: 1.00}[len(conteo_cols)]
                    pago = int(SYMBOL_BASE_VALUES[simb] * self.bet_por_linea * multiplicador * formas)
                    pago = max(pago, 1)
                    total_ganado += pago
                    detalles.append({
                        "tipo": "Ways",
                        "desc": f"{formas}x formas de {len(conteo_cols)}x {simb}",
                        "pago": pago
                    })
        else:
            # Motor Geométrico de Líneas de Pago (10, 20 o 50)
            multiplicadores = {3: 0.60, 4: 0.80, 5: 1.00}
            for i in range(modo):
                trayectoria = PAYLINES[i]
                simbolos_linea = [self.cuadricula[col][trayectoria[col]] for col in range(COLUMNAS)]

                # Identificar símbolo objetivo sustituyendo comodines Wild
                target = None
                for s in simbolos_linea:
                    if s != "Wild" and s != "Scatter":
                        target = s
                        break
                if target is None:
                    target = "Wild"

                coincidencias = 0
                for s in simbolos_linea:
                    if s == target or s == "Wild":
                        coincidencias += 1
                    else:
                        break

                if coincidencias in multiplicadores:
                    tasa = multiplicadores[coincidencias]
                    pago = int(SYMBOL_BASE_VALUES[target] * self.bet_por_linea * tasa)
                    pago = max(pago, 1)
                    total_ganado += pago
                    detalles.append({
                        "tipo": "Línea",
                        "desc": f"Línea {i+1:02d}: {coincidencias}x {target}",
                        "pago": pago
                    })
                    lineas_destacadas.append({
                        "num": i + 1,
                        "matches": coincidencias,
                        "path": trayectoria,
                        "color": LINE_COLORS[len(lineas_destacadas) % len(LINE_COLORS)]
                    })

        # Evaluación de Scatters (Giros Gratis)
        scatters = sum(1 for col in self.cuadricula if "Scatter" in col)
        tiros_ganados = 0
        if scatters >= 3:
            tiros_ganados = {3: 10, 4: 25, 5: 100}.get(scatters, 10)
            self.free_spins += tiros_ganados
            self.modo_bono = True
            self.audio.play("bonus")
            self.efectos.append(EfectoParticula(ANCHO // 2, ALTO // 2, "texto", f"¡BONO: +{tiros_ganados} GIROS GRATIS!"))

        # Multiplicador del 20% adicional durante el modo bono
        if self.modo_bono and total_ganado > 0:
            total_ganado = int(total_ganado * 1.2)

        return total_ganado, detalles, lineas_destacadas, scatters, tiros_ganados

    def actualizar(self):
        # Actualización de saldo visual suavizado (rolling counter)
        if self.saldo_visual < self.saldo:
            diferencia = self.saldo - self.saldo_visual
            self.saldo_visual += max(1.0, diferencia * 0.15)
            if abs(self.saldo - self.saldo_visual) < 1:
                self.saldo_visual = self.saldo
        elif self.saldo_visual > self.saldo:
            self.saldo_visual = self.saldo

        # Bucle de Giro Animado con Parada Escalonada por Carrete
        if self.girando:
            ahora = pygame.time.get_ticks()
            delta = ahora - self.tiempo_inicio_giro

            # Carrete 0 a 4 se detienen secuencialmente (800ms a 1600ms)
            for c in range(COLUMNAS):
                t_frenado = 700 + c * 200
                if delta >= t_frenado:
                    if not self.carretes_detenidos[c]:
                        self.carretes_detenidos[c] = True
                        self.audio.play("stop")
                else:
                    # Carrete sigue rotando símbolos
                    self.cuadricula[c] = [self.obtener_simbolo_aleatorio() for _ in range(FILAS)]

            if all(self.carretes_detenidos):
                self.girando = False
                premio, det, lins, scats, new_spins = self.calcular_premio()
                self.ultimo_premio = premio
                self.detalles_ganancias = det
                self.lineas_a_dibujar = lins
                self.saldo += premio
                if premio > self.stats_mayor_premio:
                    self.stats_mayor_premio = premio

                if premio > 0 or new_spins > 0:
                    self.audio.play("win")
                    msg = f"¡GANANCIA: +${premio}!" if premio > 0 else ""
                    if new_spins > 0:
                        msg += f" | 🎉 ¡{scats} Scatters! +{new_spins} Giros Gratis"
                    self.mensaje_estado = msg
                    self.efectos.append(EfectoParticula(self.grid_x + (5 * self.celda_w) // 2, 280, "texto", f"+${premio}"))
                    for _ in range(45):
                        self.efectos.append(EfectoParticula(
                            random.randint(self.grid_x, self.grid_x + 5 * self.celda_w),
                            random.randint(self.grid_y + 100, self.grid_y + 400)
                        ))
                else:
                    self.mensaje_estado = "Sin combinación premiada. ¡Vuelve a girar!"

        # Ejecución automática durante Modo Bono
        if self.modo_bono and not self.girando and len(self.efectos) == 0:
            if self.free_spins > 0:
                pygame.time.delay(500)
                self.iniciar_giro()
            else:
                self.modo_bono = False
                self.mensaje_estado = "Modo Bono finalizado. ¡Excelente ronda!"

        # Actualizar partículas
        for ef in self.efectos[:]:
            ef.actualizar()
            if ef.vida <= 0:
                self.efectos.remove(ef)

    def dibujar_tablero(self):
        # Marco exterior del tablero
        ancho_grilla = COLUMNAS * self.celda_w + (COLUMNAS - 1) * self.gap
        alto_grilla = FILAS * self.celda_h + (FILAS - 1) * self.gap
        marco_rect = pygame.Rect(self.grid_x - 8, self.grid_y - 8, ancho_grilla + 16, alto_grilla + 16)

        borde_color = ORO if not self.modo_bono else ROJO_CASINO
        pygame.draw.rect(self.screen, (20, 22, 30), marco_rect, border_radius=16)
        pygame.draw.rect(self.screen, borde_color, marco_rect, 3, border_radius=16)

        # Celdas y Símbolos
        for c in range(COLUMNAS):
            for f in range(FILAS):
                cx = self.grid_x + c * (self.celda_w + self.gap)
                cy = self.grid_y + f * (self.celda_h + self.gap)
                celda_rect = pygame.Rect(cx, cy, self.celda_w, self.celda_h)

                # Fondo de la celda
                bg_color = (248, 249, 252) if not self.modo_bono else (45, 15, 25)
                pygame.draw.rect(self.screen, bg_color, celda_rect, border_radius=10)
                pygame.draw.rect(self.screen, (200, 205, 215) if not self.modo_bono else (80, 30, 45), celda_rect, 1, border_radius=10)

                # Renderizar Sprite o Texto de Fallback
                simb = self.cuadricula[c][f]
                img = self.symbol_surfaces.get(simb)
                if img:
                    img_rect = img.get_rect(center=celda_rect.center)
                    self.screen.blit(img, img_rect)
                else:
                    # Fallback visual nítido
                    col_t = ORO if simb == "Scatter" else (AZUL_ACENTO if simb == "Wild" else (30, 30, 40))
                    txt = self.f_med.render(simb, True, col_t)
                    self.screen.blit(txt, txt.get_rect(center=celda_rect.center))

    def trazar_lineas_ganadoras(self):
        """Superpone las líneas vectoriales premiadas con badges numéricos."""
        if self.modos_lineas[self.idx_modo] == 1024 or self.girando:
            return

        for linea in self.lineas_a_dibujar:
            color = linea["color"]
            path = linea["path"]
            matches = linea["matches"]

            puntos = []
            for col in range(matches):
                row = path[col]
                px = self.grid_x + col * (self.celda_w + self.gap) + self.celda_w // 2
                py = self.grid_y + row * (self.celda_h + self.gap) + self.celda_h // 2
                puntos.append((px, py))

            if len(puntos) >= 2:
                pygame.draw.lines(self.screen, color, False, puntos, 5)
                # Badge inicial con el número de línea
                ini_x, ini_y = puntos[0]
                pygame.draw.circle(self.screen, color, (ini_x - 45, ini_y), 14)
                pygame.draw.circle(self.screen, BLANCO, (ini_x - 45, ini_y), 14, 2)
                lbl = self.f_peq.render(str(linea["num"]), True, BLANCO)
                self.screen.blit(lbl, lbl.get_rect(center=(ini_x - 45, ini_y)))

    def dibujar_panel_lateral(self):
        """Panel de Desglose de Ganancias, Estadísticas y Tabla de Pagos."""
        panel_x = 920
        panel_y = self.grid_y - 8
        panel_w = 400
        panel_h = 670

        rect_panel = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(self.screen, (20, 22, 32), rect_panel, border_radius=14)
        pygame.draw.rect(self.screen, GRIS_BORDE, rect_panel, 2, border_radius=14)

        # Encabezado Panel
        pygame.draw.rect(self.screen, (28, 32, 45), (panel_x, panel_y, panel_w, 45), border_top_left_radius=14, border_top_right_radius=14)
        t_aud = self.f_med.render("AUDITORÍA DE PREMIOS", True, ORO)
        self.screen.blit(t_aud, (panel_x + 20, panel_y + 10))

        # Desglose de Líneas Ganadoras
        y_cursor = panel_y + 60
        t_sub = self.f_peq.render("LÍNEAS PREMIADAS EN EL ÚLTIMO GIRO:", True, TEXTO_MUTED)
        self.screen.blit(t_sub, (panel_x + 20, y_cursor))
        y_cursor += 25

        caja_desglose = pygame.Rect(panel_x + 15, y_cursor, panel_w - 30, 230)
        pygame.draw.rect(self.screen, (12, 14, 20), caja_desglose, border_radius=8)
        pygame.draw.rect(self.screen, (40, 44, 60), caja_desglose, 1, border_radius=8)

        if self.detalles_ganancias:
            y_item = y_cursor + 10
            for item in self.detalles_ganancias[:8]:
                cadena = f"• {item['desc']} -> +${item['pago']}"
                t_item = self.f_mono.render(cadena, True, VERDE_EXITO)
                self.screen.blit(t_item, (panel_x + 25, y_item))
                y_item += 25
            if len(self.detalles_ganancias) > 8:
                t_mas = self.f_peq.render(f"... y {len(self.detalles_ganancias)-8} combinaciones más.", True, TEXTO_MUTED)
                self.screen.blit(t_mas, (panel_x + 25, y_item + 5))
        else:
            t_sin = self.f_peq.render("Ninguna línea premiada en este giro.", True, (110, 115, 130))
            self.screen.blit(t_sin, (panel_x + 35, y_cursor + 105))

        y_cursor += 250

        # Estadísticas de Sesión
        pygame.draw.rect(self.screen, (28, 32, 45), (panel_x + 15, y_cursor, panel_w - 30, 120), border_radius=10)
        t_st = self.f_med.render("ESTADÍSTICAS DE SESIÓN", True, BLANCO)
        self.screen.blit(t_st, (panel_x + 25, y_cursor + 10))

        t_g = self.f_peq.render(f"Giros Ejecutados:  {self.stats_giros}", True, TEXTO_MUTED)
        t_mp = self.f_peq.render(f"Mayor Premio:     ${self.stats_mayor_premio}", True, ORO_BRILLANTE)
        t_fs = self.f_peq.render(f"Giros Gratis Activos: {self.free_spins}", True, ROJO_HOVER if self.free_spins > 0 else TEXTO_MUTED)

        self.screen.blit(t_g, (panel_x + 30, y_cursor + 45))
        self.screen.blit(t_mp, (panel_x + 30, y_cursor + 70))
        self.screen.blit(t_fs, (panel_x + 30, y_cursor + 95))

        y_cursor += 135

        # Tabla de Pagos Resumida
        pygame.draw.rect(self.screen, (16, 18, 26), (panel_x + 15, y_cursor, panel_w - 30, 160), border_radius=10)
        t_tp = self.f_peq.render("TABLA DE SÍMBOLOS (Pago Base)", True, ORO)
        self.screen.blit(t_tp, (panel_x + 25, y_cursor + 10))

        y_sym = y_cursor + 35
        simbolos_muestra = [("Wild", "Comodín (200x)"), ("Heart", "120x"), ("Diamond", "90x"),
                            ("Fruit", "60x"), ("Scatter", "Bono Giros")]
        for s, val in simbolos_muestra:
            ts = self.f_peq.render(f"{s}:", True, BLANCO)
            tv = self.f_peq.render(val, True, TEXTO_MUTED)
            self.screen.blit(ts, (panel_x + 30, y_sym))
            self.screen.blit(tv, (panel_x + 160, y_sym))
            y_sym += 24

    def dibujar_consola_inferior(self):
        """Barra inferior de controles, contadores y acciones."""
        ancho_grilla = COLUMNAS * self.celda_w + (COLUMNAS - 1) * self.gap
        rect_consola = pygame.Rect(self.grid_x - 8, 595, ancho_grilla + 16, 145)
        pygame.draw.rect(self.screen, (22, 24, 34), rect_consola, border_radius=16)
        pygame.draw.rect(self.screen, GRIS_BORDE, rect_consola, 2, border_radius=16)

        # Barra de Estado / Notificaciones
        t_est = self.f_peq.render(self.mensaje_estado, True, ORO_BRILLANTE if "GANANCIA" in self.mensaje_estado or "BONO" in self.mensaje_estado else BLANCO)
        self.screen.blit(t_est, (self.grid_x + 15, 608))

        # Panel de Saldo (Smoothed Rolling Counter)
        rect_saldo = pygame.Rect(self.grid_x + 10, 645, 230, 75)
        pygame.draw.rect(self.screen, (14, 16, 24), rect_saldo, border_radius=12)
        pygame.draw.rect(self.screen, (40, 44, 60), rect_saldo, 1, border_radius=12)

        t_lbl_s = self.f_peq.render("CRÉDITOS DISPONIBLES", True, TEXTO_MUTED)
        t_val_s = self.f_med.render(f"${int(self.saldo_visual):,}", True, VERDE_EXITO)
        self.screen.blit(t_lbl_s, (self.grid_x + 25, 655))
        self.screen.blit(t_val_s, (self.grid_x + 25, 680))

        # Indicador de Apuesta Total
        rect_ap = pygame.Rect(self.grid_x + 250, 645, 180, 75)
        pygame.draw.rect(self.screen, (14, 16, 24), rect_ap, border_radius=12)
        pygame.draw.rect(self.screen, (40, 44, 60), rect_ap, 1, border_radius=12)

        t_lbl_a = self.f_peq.render("APUESTA TOTAL", True, TEXTO_MUTED)
        t_val_a = self.f_med.render(f"${self.apuesta_total():,}", True, ORO)
        self.screen.blit(t_lbl_a, (self.grid_x + 265, 655))
        self.screen.blit(t_val_a, (self.grid_x + 265, 680))

        # Selector de Líneas
        modo_txt = "1024 FORMAS" if self.modos_lineas[self.idx_modo] == 1024 else f"{self.modos_lineas[self.idx_modo]} LÍNEAS"
        self.btn_lineas.texto = modo_txt
        self.btn_lineas.rect.x = self.grid_x + 440
        self.btn_lineas.rect.y = 660
        self.btn_lineas.dibujar(self.screen)

        # Ajuste de Apuesta por línea (- / +)
        self.btn_bet_menos.rect.x = self.grid_x + 605
        self.btn_bet_menos.rect.y = 660
        self.btn_bet_menos.dibujar(self.screen)

        t_bet = self.f_peq.render(f"${self.bet_por_linea}/L", True, BLANCO)
        self.screen.blit(t_bet, (self.grid_x + 663, 675))

        self.btn_bet_mas.rect.x = self.grid_x + 715
        self.btn_bet_mas.rect.y = 660
        self.btn_bet_mas.dibujar(self.screen)

        # Botón MAX BET
        self.btn_max.rect.x = self.grid_x + 780
        self.btn_max.rect.y = 650
        self.btn_max.dibujar(self.screen)

        # Botón GIRAR
        self.btn_spin.rect.x = self.grid_x + ancho_grilla - 150
        self.btn_spin.rect.y = 645
        self.btn_spin.texto = "GIRANDO..." if self.girando else "GIRAR"
        self.btn_spin.color_base = GRIS_OSCURO if self.girando else ROJO_CASINO
        self.btn_spin.dibujar(self.screen)

    def dibujar_encabezado(self):
        """Barra superior con título, estado del bono y controles rápidos."""
        pygame.draw.rect(self.screen, (16, 18, 26), (0, 0, ANCHO, 60))
        pygame.draw.line(self.screen, (35, 40, 55), (0, 60), (ANCHO, 60), 2)

        # Título Casino
        t_tit = self.f_med.render("🎰 GEMINI ROYAL CASINO SLOTS", True, ORO)
        self.screen.blit(t_tit, (50, 15))

        # Giros Gratis Badge
        if self.modo_bono:
            t_bono = self.f_med.render(f"🔥 MODO BONO: {self.free_spins} GIROS GRATIS RESTANTES (1.2x) 🔥", True, ROJO_HOVER)
            self.screen.blit(t_bono, (ANCHO // 2 - t_bono.get_width() // 2, 15))

        # Botones Rápidos Superior
        self.btn_cajero.rect.x = ANCHO - 260
        self.btn_cajero.rect.y = 12
        self.btn_cajero.alto = 38
        self.btn_cajero.dibujar(self.screen)

        self.btn_sonido.texto = "AUDIO: ON" if self.audio.enabled else "AUDIO: OFF"
        self.btn_sonido.rect.x = ANCHO - 135
        self.btn_sonido.rect.y = 12
        self.btn_sonido.alto = 38
        self.btn_sonido.dibujar(self.screen)

    def dibujar_cajero(self):
        """Pantalla de Bienvenida y Depósito de Créditos."""
        self.screen.fill(NEGRO_FONDO)

        # Tarjeta Central Glassmorphism
        caja_w, caja_h = 600, 450
        caja_rect = pygame.Rect(ANCHO // 2 - caja_w // 2, ALTO // 2 - caja_h // 2, caja_w, caja_h)
        pygame.draw.rect(self.screen, (22, 24, 34), caja_rect, border_radius=20)
        pygame.draw.rect(self.screen, ORO, caja_rect, 3, border_radius=20)

        # Título Cajero
        t_tit = self.f_tit.render("CAJERO PRINCIPAL", True, ORO)
        t_sub = self.f_peq.render("Ingresa la cantidad de créditos con la que deseas jugar:", True, TEXTO_MUTED)
        self.screen.blit(t_tit, (ANCHO // 2 - t_tit.get_width() // 2, caja_rect.y + 35))
        self.screen.blit(t_sub, (ANCHO // 2 - t_sub.get_width() // 2, caja_rect.y + 85))

        self.input_deposito.dibujar(self.screen)
        self.btn_entrar.dibujar(self.screen)

        t_rap = self.f_peq.render("Depósitos Rápidos:", True, TEXTO_MUTED)
        self.screen.blit(t_rap, (ANCHO // 2 - 250, 485))

        self.btn_dep_500.dibujar(self.screen)
        self.btn_dep_1000.dibujar(self.screen)
        self.btn_dep_5000.dibujar(self.screen)

    def ejecutar(self):
        """Bucle Principal de Juego (Game Loop)."""
        while True:
            eventos = pygame.event.get()
            for e in eventos:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if self.estado == "DEPOSITO":
                    self.input_deposito.manejar_evento(e)

                    if self.btn_entrar.clicado(e) and self.input_deposito.texto:
                        monto = float(self.input_deposito.texto)
                        if monto > 0:
                            self.saldo = monto
                            self.saldo_visual = monto
                            self.estado = "JUEGO"
                            self.audio.play("coin")

                    if self.btn_dep_500.clicado(e):
                        self.input_deposito.texto = str(int(self.input_deposito.texto or 0) + 500)
                    if self.btn_dep_1000.clicado(e):
                        self.input_deposito.texto = str(int(self.input_deposito.texto or 0) + 1000)
                    if self.btn_dep_5000.clicado(e):
                        self.input_deposito.texto = str(int(self.input_deposito.texto or 0) + 5000)

                elif self.estado == "JUEGO":
                    # Atajos de Teclado
                    if e.type == pygame.KEYDOWN:
                        if e.key in (pygame.K_SPACE, pygame.K_RETURN) and not self.girando:
                            self.iniciar_giro()
                        elif e.key == pygame.K_m and not self.girando:
                            self.idx_modo = 2  # 50 líneas
                            self.bet_por_linea = 100
                            self.iniciar_giro()
                        elif e.key == pygame.K_l and not self.girando:
                            self.idx_modo = (self.idx_modo + 1) % len(self.modos_lineas)
                        elif e.key == pygame.K_UP and not self.girando:
                            if self.bet_por_linea < 100:
                                self.bet_por_linea += 1
                        elif e.key == pygame.K_DOWN and not self.girando:
                            if self.bet_por_linea > 1:
                                self.bet_por_linea -= 1
                        elif e.key == pygame.K_c:
                            self.estado = "DEPOSITO"

                    # Botones de Acción
                    if self.btn_spin.clicado(e) and not self.girando:
                        self.iniciar_giro()

                    if self.btn_max.clicado(e) and not self.girando:
                        self.idx_modo = 2  # 50 líneas
                        self.bet_por_linea = 100
                        self.iniciar_giro()

                    if self.btn_lineas.clicado(e) and not self.girando:
                        self.idx_modo = (self.idx_modo + 1) % len(self.modos_lineas)

                    if self.btn_bet_mas.clicado(e) and not self.girando:
                        if self.bet_por_linea < 100:
                            self.bet_por_linea += 1

                    if self.btn_bet_menos.clicado(e) and not self.girando:
                        if self.bet_por_linea > 1:
                            self.bet_por_linea -= 1

                    if self.btn_cajero.clicado(e):
                        self.estado = "DEPOSITO"

                    if self.btn_sonido.clicado(e):
                        self.audio.toggle()

            self.actualizar()

            # Renderizado
            if self.estado == "DEPOSITO":
                self.dibujar_cajero()
            else:
                self.screen.fill(NEGRO_FONDO if not self.modo_bono else FONDO_BONO)
                self.dibujar_encabezado()
                self.dibujar_tablero()
                self.trazar_lineas_ganadoras()
                self.dibujar_panel_lateral()
                self.dibujar_consola_inferior()

                # Renderizar Partículas y Textos Flotantes
                for ef in self.efectos:
                    if ef.tipo == "particula":
                        pygame.draw.circle(self.screen, ef.color, (int(ef.x), int(ef.y)), ef.radio)
                    else:
                        txt_gan = self.f_big.render(ef.valor, True, ef.color)
                        txt_gan.set_alpha(ef.alpha)
                        self.screen.blit(txt_gan, (ef.x - txt_gan.get_width() // 2, ef.y))

            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    SlotMachineHD().ejecutar()
