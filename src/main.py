"""
🎰 GEMINI ROYAL CASINO SLOTS — UNIFIED LAUNCHER 🎰
Punto de entrada unificado para el simulador de tragamonedas multilínea.
Permite ejecutar el motor gráfico principal en Pygame (HD 60 FPS) o el motor clásico en Tkinter (Pillow).
"""

import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Simulador de Casino: Máquina Tragamonedas Multilínea 5x4")
    parser.add_argument(
        "--engine",
        choices=["pygame", "tkinter"],
        default="pygame",
        help="Motor gráfico a ejecutar: 'pygame' (HD 60 FPS, Recomendado) o 'tkinter' (Escritorio clásico)"
    )
    args = parser.parse_args()

    if args.engine == "tkinter":
        print("🎮 Iniciando Simulador en modo clásico (Tkinter + Pillow)...")
        import tkinter as tk
        from slot_tkinter import SlotMachine
        root = tk.Tk()
        app = SlotMachine(master=root)
        root.mainloop()
    else:
        print("🎰 Iniciando Gemini Royal Slots HD 60 FPS (Pygame)...")
        from slots import SlotMachineHD
        SlotMachineHD().ejecutar()

if __name__ == "__main__":
    main()
