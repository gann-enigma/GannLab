import tkinter as tk
from tkinter import ttk, messagebox
import math

class GannHexagonGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Concentric Hexagon - Full Version")
        self.master.geometry("800x950")
        self.master.minsize(600, 700)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ... (Style configurations remain the same) ...
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Tahoma", 11))
        self.style.configure("TButton", font=("Tahoma", 12, "bold"), padding=10)
        self.style.configure("TEntry", font=("Tahoma", 12), padding=5)
        self.style.configure("TMenubutton", font=("Tahoma", 11))

        self.input_frame = ttk.Frame(self.master, padding="15")
        self.input_frame.pack(pady=10, fill="x")
        self.input_frame.columnconfigure(1, weight=1)

        # --- Input Widgets ---
        ttk.Label(self.input_frame, text="Start Number (Center):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_num_var = tk.StringVar(value="1")
        self.start_num_entry = ttk.Entry(self.input_frame, textvariable=self.start_num_var)
        self.start_num_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Number of Rotations (Layers):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rotations_var = tk.StringVar(value="4")
        self.rotations_entry = ttk.Entry(self.input_frame, textvariable=self.rotations_var)
        self.rotations_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.input_frame, text="Spiral Direction:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.direction_var = tk.StringVar(value="Clockwise")
        self.direction_menu = ttk.OptionMenu(self.input_frame, self.direction_var, "Clockwise", "Clockwise", "Counter-Clockwise")
        self.direction_menu.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.input_frame, text="Highlight Number:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.highlight_var = tk.StringVar(value="")
        self.highlight_entry = ttk.Entry(self.input_frame, textvariable=self.highlight_var)
        self.highlight_entry.grid(row=3, column=1, padx=(10, 2), pady=5, sticky="ew")

        self.search_button = ttk.Button(self.input_frame, text="🔍", command=self.handle_highlight_click)
        self.search_button.grid(row=3, column=2, padx=(0, 10), pady=5, sticky="w")
        self.input_frame.columnconfigure(2, weight=0)

        self.generate_button = ttk.Button(self.input_frame, text="Generate / Redraw Hexagon", command=self.display_chart)
        self.generate_button.grid(row=4, column=0, columnspan=3, pady=15, sticky="ew", padx=10)

        self.canvas = tk.Canvas(self.master, bg="#2c2c2c", highlightthickness=0)
        self.canvas.pack(expand=True, fill="both", padx=15, pady=10)
        
        self.gann_data = {}
        self.text_ids = {}
        self.canvas.bind("<Configure>", self.display_chart)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        
        self._after_id = None
        self.master.after(100, self.display_chart)

    def _get_hex_points(self, center_x, center_y, radius):
        points = []
        for i in range(6):
            angle_deg = 60 * i
            angle_rad = math.pi / 180 * angle_deg
            points.append((center_x + radius * math.cos(angle_rad), center_y - radius * math.sin(angle_rad)))
        return points

    def display_chart(self, event=None):
        if self._after_id:
            self.master.after_cancel(self._after_id)
        self._after_id = self.master.after(50, self._generate_and_draw)

    def _generate_and_draw(self):
        self.canvas.delete("all")
        self.gann_data.clear()
        self.text_ids.clear()

        try:
            rotations = int(self.rotations_var.get())
            start_num = int(self.start_num_var.get())
            is_clockwise = self.direction_var.get() == "Clockwise"
        except (ValueError, tk.TclError):
            return 

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 : return

        center_x, center_y = canvas_width / 2, canvas_height / 2
        max_radius = min(canvas_width, canvas_height) / 2 * 0.9
        base_radius = max_radius / (rotations + 0.5)

        font_size = max(8, int(base_radius / 2.5))
        number_font = ("Arial", font_size, "bold")
        
        self.gann_data[start_num] = (center_x, center_y)
        self.canvas.create_text(center_x, center_y, text=str(start_num), font=number_font, fill="white", tags=f"num_{start_num}")

        current_val = start_num + 1

        for layer in range(1, rotations + 1):
            layer_radius = layer * base_radius
            outline_points = self._get_hex_points(center_x, center_y, layer_radius)
            self.canvas.create_polygon(outline_points, outline="#D2B48C", fill="", width=2)
            
            perimeter_points = []
            if is_clockwise:
                vertex_angles = [120, 60, 0, -60, -120, -180]
            else: 
                vertex_angles = [60, 120, 180, 240, 300, 360]

            vertices = []
            for angle_deg in vertex_angles:
                angle_rad = math.pi / 180 * angle_deg
                vertices.append((center_x + layer_radius * math.cos(angle_rad), 
                                 center_y - layer_radius * math.sin(angle_rad)))

            for side in range(6):
                start_vertex = vertices[side]
                end_vertex = vertices[(side + 1) % 6]
                for i in range(layer):
                    ratio = i / float(layer)
                    px = start_vertex[0] * (1 - ratio) + end_vertex[0] * ratio
                    py = start_vertex[1] * (1 - ratio) + end_vertex[1] * ratio
                    perimeter_points.append((px, py))
            
            # --- FINAL CORRECTION BASED ON DIRECT INSTRUCTION ---
            shift_amount = layer - 1
            if shift_amount > 0:
                if is_clockwise:
                    # This logic is correct and confirmed.
                    perimeter_points = perimeter_points[-shift_amount:] + perimeter_points[:-shift_amount]
                else: # Counter-Clockwise
                    # As per your final instruction, this mode also uses a counter-clockwise shift.
                    perimeter_points = perimeter_points[-shift_amount:] + perimeter_points[:-shift_amount]
            
            for px, py in perimeter_points:
                self.gann_data[current_val] = (px, py)
                self.canvas.create_text(px, py, text=str(current_val), font=number_font, fill="white", tags=f"num_{current_val}")
                current_val += 1
        
        self.update_highlights()

    def on_canvas_click(self, event):
        item_found = self.canvas.find_closest(event.x, event.y)
        if not item_found: return
        item = item_found[0]
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("num_"):
                try:
                    number = int(tag.split("_")[1])
                    self.highlight_var.set(str(number))
                    self.update_highlights()
                except (ValueError, IndexError): pass
                return

    def handle_highlight_click(self):
        try:
            start_num = int(self.start_num_var.get())
            highlight_text = self.highlight_var.get()
            if not highlight_text:
                self.update_highlights()
                return
            highlight_num = int(highlight_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return

        rotations = int(self.rotations_var.get())
        max_num_in_grid = start_num + (3 * rotations * (rotations + 1))

        if highlight_num > max_num_in_grid:
            new_rotations = 0
            while True:
                new_rotations += 1
                if (start_num + (3 * new_rotations * (new_rotations + 1))) >= highlight_num:
                    break
            self.rotations_var.set(str(new_rotations))
            self.display_chart()
        else:
            self.update_highlights()

    def update_highlights(self):
        highlight_num = None
        try:
            highlight_text = self.highlight_var.get()
            if highlight_text: highlight_num = int(highlight_text)
        except ValueError: return

        for number in self.gann_data.keys():
            color = "#34a853" if number == highlight_num else "white"
            self.canvas.itemconfig(f"num_{number}", fill=color)


if __name__ == "__main__":
    root = tk.Tk()
    app = GannHexagonGUI(root)
    root.mainloop()