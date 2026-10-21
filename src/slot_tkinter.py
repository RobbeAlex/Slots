import os
import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

# ==========================================
# 1. RUTAS DE TUS IMÁGENES
# Pega aquí las rutas a tus archivos (.png, .gif, .ppm)
# Si no existe la ruta, se dibujará una ficha con texto.
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SYMBOL_PATHS = {
    "Wild": os.path.join(BASE_DIR, "assets", "wild.png"),
    "Scatter": os.path.join(BASE_DIR, "assets", "Scatter.png"),
    "Heart": os.path.join(BASE_DIR, "assets", "heart.png"),
    "Diamond": os.path.join(BASE_DIR, "assets", "diamond.png"),
    "Fruit": os.path.join(BASE_DIR, "assets", "fruit.png"),
    "A": os.path.join(BASE_DIR, "assets", "A.png"),
    "B": os.path.join(BASE_DIR, "assets", "B.png"),
    "C": os.path.join(BASE_DIR, "assets", "C.png"),
    "D": os.path.join(BASE_DIR, "assets", "D.png"),
}

# ==========================================
# CONFIGURACIÓN DE LA MÁQUINA
# ==========================================
ROWS = 4
COLS = 5
MAX_LINES = 50
MIN_BET = 1
MAX_BET = 100

CELL_WIDTH = 80
CELL_HEIGHT = 80

symbol_count = {
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

symbol_value = {
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

LINE_COLORS = ["#FF1744", "#00E676", "#2979FF", "#FFEA00", "#FF9100", "#D500F9", "#00E5FF"]

class SlotMachine(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Casino Slot")
        self.pack(padx=15, pady=10)

        self.balance = self.pedir_saldo_inicial()
        self.free_spins = 0
        self.symbol_images = {}
        self.rendered_images = []  # Evita que el Garbage Collector borre las imágenes activas

        self.cargar_imagenes()
        self.create_widgets()
        self.dibujar_tablero_inicial()

        self.master.bind("<Return>", lambda event: self.spin())

    def pedir_saldo_inicial(self):
        saldo = simpledialog.askinteger(
            "Saldo Inicial", "Ingresa tu saldo inicial:",
            parent=self.master, initialvalue=1000, minvalue=10
        )
        return saldo if saldo is not None else 1000

    def cargar_imagenes(self):
        """Carga y reescala usando Pillow para asegurar compatibilidad total."""
        for symbol, path in SYMBOL_PATHS.items():
            if path.strip() != "":
                if os.path.exists(path):
                    try:
                        pil_img = Image.open(path).convert("RGBA")
                        pil_img = pil_img.resize((CELL_WIDTH - 16, CELL_HEIGHT - 16), Image.Resampling.LANCZOS)
                        self.symbol_images[symbol] = ImageTk.PhotoImage(pil_img)
                    except Exception as e:
                        print(f"Error al procesar la imagen de {symbol} ({path}): {e}")
                else:
                    print(f"Advertencia: El archivo no existe en la ruta: {path}")

    def create_widgets(self):
        status_frame = tk.Frame(self)
        status_frame.pack(fill=tk.X, pady=5)

        self.balance_label = tk.Label(status_frame, text=f"Saldo: ${self.balance}", font=("Arial", 14, "bold"))
        self.balance_label.pack(side=tk.LEFT, padx=10)

        self.free_spins_label = tk.Label(status_frame, text="", font=("Arial", 12, "bold"), fg="#E65100")
        self.free_spins_label.pack(side=tk.LEFT, padx=10)

        control_frame = tk.Frame(self, pady=4)
        control_frame.pack()

        tk.Label(control_frame, text=f"Líneas (1-{MAX_LINES}):", font=("Arial", 10)).grid(row=0, column=0, padx=4)
        self.lines_entry = tk.Entry(control_frame, width=5, justify="center")
        self.lines_entry.insert(0, str(MAX_LINES))
        self.lines_entry.grid(row=0, column=1, padx=4)

        tk.Label(control_frame, text=f"Apuesta/línea (${MIN_BET}-${MAX_BET}):", font=("Arial", 10)).grid(row=0, column=2, padx=4)
        self.bet_entry = tk.Entry(control_frame, width=6, justify="center")
        self.bet_entry.insert(0, "1")
        self.bet_entry.grid(row=0, column=3, padx=4)

        self.spin_button = tk.Button(
            control_frame, text="GIRAR (Enter)", command=self.spin,
            font=("Arial", 11, "bold"), bg="#D32F2F", fg="white", padx=12
        )
        self.spin_button.grid(row=0, column=4, padx=10)

        canvas_w = COLS * CELL_WIDTH
        canvas_h = ROWS * CELL_HEIGHT
        self.canvas = tk.Canvas(self, width=canvas_w, height=canvas_h, bg="#1E1E1E", highlightthickness=2, highlightbackground="#444")
        self.canvas.pack(pady=8)

        self.result_label = tk.Label(self, text="Presiona GIRAR o ENTER para jugar", font=("Arial", 11, "bold"))
        self.result_label.pack(pady=2)

        tk.Label(self, text="Desglose de líneas ganadoras:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.payout_text = tk.Text(self, height=4, width=65, font=("Consolas", 9), bg="#F5F5F5", relief=tk.SOLID, bd=1)
        self.payout_text.pack(pady=4)

    def dibujar_tablero_inicial(self):
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL_WIDTH, r * CELL_HEIGHT
                x2, y2 = x1 + CELL_WIDTH, y1 + CELL_HEIGHT
                self.canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="#FFFFFF", outline="#777")
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="-", font=("Arial", 16, "bold"), fill="#999")

    def get_slot_machine_spin(self):
        all_symbols = [symbol for symbol, count in symbol_count.items() for _ in range(count)]
        return [random.sample(all_symbols, ROWS) for _ in range(COLS)]

    def check_scatters(self, columns):
        cols_with_scatter = sum(1 for col in columns if "Scatter" in col)
        scatter_awards = {3: 10, 4: 25, 5: 100}
        return scatter_awards.get(cols_with_scatter, 0), cols_with_scatter

    def check_winnings(self, columns, num_lines, bet):
        winnings = 0
        winning_details = []
        payout_multipliers = {3: 0.60, 4: 0.80, 5: 1.00}

        for i in range(num_lines):
            line_path = PAYLINES[i]
            line_symbols = [columns[col][line_path[col]] for col in range(COLS)]

            target_symbol = None
            for sym in line_symbols:
                if sym != "Wild" and sym != "Scatter":
                    target_symbol = sym
                    break
            if target_symbol is None:
                target_symbol = "Wild"

            match_count = 0
            for sym in line_symbols:
                if sym == target_symbol or sym == "Wild":
                    match_count += 1
                else:
                    break

            if match_count in payout_multipliers:
                tasa = payout_multipliers[match_count]
                pago = int(symbol_value[target_symbol] * bet * tasa)
                pago = max(pago, 1)
                winnings += pago
                winning_details.append({
                    "line_number": i + 1,
                    "symbol": target_symbol,
                    "matches": match_count,
                    "payout": pago,
                    "path": line_path
                })

        return winnings, winning_details

    def actualizar_tablero(self, slots):
        self.canvas.delete("all")
        self.rendered_images.clear()  # Reiniciar contenedor de referencias activas

        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * CELL_WIDTH, r * CELL_HEIGHT
                x2, y2 = x1 + CELL_WIDTH, y1 + CELL_HEIGHT
                sym = slots[c][r]

                # Fondo blanco para cada casilla
                self.canvas.create_rectangle(x1 + 2, y1 + 2, x2 - 2, y2 - 2, fill="#FFFFFF", outline="#CCCCCC")

                cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

                if sym in self.symbol_images:
                    img_ref = self.symbol_images[sym]
                    self.canvas.create_image(cx, cy, image=img_ref)
                    self.rendered_images.append(img_ref)  # Guardar referencia fija
                else:
                    color = "#E65100" if sym == "Scatter" else ("#7B1FA2" if sym == "Wild" else "#111111")
                    self.canvas.create_text(cx, cy, text=sym, font=("Arial", 12, "bold"), fill=color)

    def trazar_lineas_ganadoras(self, winning_details):
        for idx, win in enumerate(winning_details):
            color = LINE_COLORS[idx % len(LINE_COLORS)]
            coords = []
            for col in range(win["matches"]):
                row = win["path"][col]
                cx = (col * CELL_WIDTH) + (CELL_WIDTH / 2)
                cy = (row * CELL_HEIGHT) + (CELL_HEIGHT / 2)
                coords.extend([cx, cy])

            if len(coords) >= 4:
                self.canvas.create_line(coords, fill=color, width=4, capstyle=tk.ROUND, joinstyle=tk.ROUND)
                start_x, start_y = coords[0], coords[1]
                self.canvas.create_oval(start_x - 10, start_y - 10, start_x + 10, start_y + 10, fill=color, outline="#000")
                self.canvas.create_text(start_x, start_y, text=str(win["line_number"]), fill="white", font=("Arial", 8, "bold"))

    def spin(self):
        try:
            lines = int(self.lines_entry.get())
            bet = int(self.bet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa números válidos en las líneas y la apuesta.")
            return

        if not (1 <= lines <= MAX_LINES):
            messagebox.showerror("Error", f"El número de líneas debe estar entre 1 y {MAX_LINES}.")
            return

        if not (MIN_BET <= bet <= MAX_BET):
            messagebox.showerror("Error", f"La apuesta debe estar entre ${MIN_BET} y ${MAX_BET}.")
            return

        if self.free_spins > 0:
            self.free_spins -= 1
        else:
            total_bet = bet * lines
            if total_bet > self.balance:
                messagebox.showwarning("Fondos Insuficientes", f"Apuesta: ${total_bet}. Saldo: ${self.balance}.")
                return
            self.balance -= total_bet

        slots = self.get_slot_machine_spin()
        winnings, winning_details = self.check_winnings(slots, lines, bet)
        self.balance += winnings

        nuevos_tiros, cols_scatter = self.check_scatters(slots)
        if nuevos_tiros > 0:
            self.free_spins += nuevos_tiros

        self.actualizar_tablero(slots)
        self.trazar_lineas_ganadoras(winning_details)

        self.balance_label.config(text=f"Saldo: ${self.balance}")
        self.free_spins_label.config(text=f"🔥 TIROS GRATIS: {self.free_spins} 🔥" if self.free_spins > 0 else "")

        if winnings > 0 or nuevos_tiros > 0:
            txt = f"¡Ganancia: ${winnings}!" if winnings > 0 else ""
            if nuevos_tiros > 0:
                txt += f" | 🎉 ¡{cols_scatter} Scatters! +{nuevos_tiros} Tiros Gratis"
            self.result_label.config(text=txt, fg="#2E7D32")
        else:
            self.result_label.config(text="Sin premio en este giro.", fg="#555555")

        self.payout_text.delete("1.0", tk.END)
        if winning_details:
            for w in winning_details:
                detalle = f"• Línea {w['line_number']:02d}: {w['matches']}x {w['symbol']} -> Pagó ${w['payout']}\n"
                self.payout_text.insert(tk.END, detalle)
        else:
            self.payout_text.insert(tk.END, "No se registraron líneas premiadas.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SlotMachine(master=root)
    root.mainloop()