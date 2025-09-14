import tkinter as tk
from tkinter import ttk, messagebox
import math

class GannSquareGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Square Generator")
        self.master.geometry("600x950") # Increased height for the new section
        self.master.minsize(500, 700)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # Style configurations
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Tahoma", 11))
        self.style.configure("TButton", font=("Tahoma", 12, "bold"), padding=10)
        self.style.configure("TEntry", font=("Tahoma", 12), padding=5)
        self.style.configure("TMenubutton", font=("Tahoma", 11))
        self.style.configure("Result.TLabel", font=("Tahoma", 12, "bold"), foreground="darkblue")

        # --- Top Input Frame (unchanged) ---
        self.input_frame = ttk.Frame(self.master, padding="15")
        self.input_frame.pack(pady=(10,0), fill="x")
        self.input_frame.columnconfigure(1, weight=1)

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

        self.generate_button = ttk.Button(self.input_frame, text="Generate / Redraw Square", command=self.display_gann_square)
        self.generate_button.grid(row=4, column=0, columnspan=3, pady=8, sticky="ew", padx=10)

        # --- Grid Display Frame (unchanged) ---
        self.grid_display_frame = ttk.Frame(self.master, padding="10", relief="groove", borderwidth=2)
        self.grid_display_frame.pack(expand=True, fill="both", padx=15, pady=(5,10))
        
        # --- NEW: Rotation Calculator Frame ---
        self.rotation_calc_frame = ttk.LabelFrame(self.master, text="محاسبه‌گر چرخش زاویه‌ای", padding="15")
        self.rotation_calc_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.rotation_calc_frame.columnconfigure(1, weight=1)

        ttk.Label(self.rotation_calc_frame, text="عدد شروع محاسبه:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.calc_start_num_var = tk.StringVar(value="49")
        ttk.Entry(self.rotation_calc_frame, textvariable=self.calc_start_num_var).grid(row=0, column=1, sticky="ew", padx=5)

        ttk.Label(self.rotation_calc_frame, text="زاویه (درجه):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.calc_angle_var = tk.StringVar(value="180")
        ttk.Entry(self.rotation_calc_frame, textvariable=self.calc_angle_var).grid(row=1, column=1, sticky="ew", padx=5)

        ttk.Label(self.rotation_calc_frame, text="جهت حرکت:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.calc_direction_var = tk.StringVar(value="بالاتر")
        ttk.OptionMenu(self.rotation_calc_frame, self.calc_direction_var, "بالاتر", "بالاتر", "پایین‌تر").grid(row=2, column=1, sticky="ew", padx=5)

        ttk.Button(self.rotation_calc_frame, text="محاسبه کن", command=self.calculate_gann_rotation).grid(row=3, column=0, columnspan=2, pady=10, sticky="ew", padx=5)

        ttk.Label(self.rotation_calc_frame, text="عدد هدف:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.calc_result_var = tk.StringVar(value="---")
        ttk.Label(self.rotation_calc_frame, textvariable=self.calc_result_var, style="Result.TLabel").grid(row=4, column=1, sticky="w", padx=5)

        # --- Instance variables ---
        self.cell_widgets = []
        self.gann_data = []
        self.rotation_targets = set() # To store green highlighted numbers
        
        self.display_gann_square()

    # --- NEW: Method for the calculator ---
    def calculate_gann_rotation(self):
        try:
            start_num = int(self.calc_start_num_var.get())
            angle = float(self.calc_angle_var.get())
            direction = self.calc_direction_var.get()
            
            if start_num <= 0:
                messagebox.showerror("خطا", "عدد شروع باید مثبت باشد.")
                return

            sqrt_start = math.sqrt(start_num)
            angle_factor = angle / 180.0
            
            if direction == "بالاتر":
                result = (sqrt_start + angle_factor)**2
            else: # پایین‌تر
                result = (sqrt_start - angle_factor)**2
            
            target_num = int(round(result))

            # Update the result label
            self.calc_result_var.set(str(target_num))
            
            # Add to targets and check if auto-expand is needed
            self.rotation_targets.clear()
            self.rotation_targets.add(target_num)
            
            # Check if redraw is needed
            current_rotations = int(self.rotations_var.get())
            current_start = int(self.start_num_var.get())
            dim = 2 * current_rotations + 1
            max_num_in_grid = current_start + dim**2 - 1

            if target_num > max_num_in_grid or target_num < current_start:
                # Yes, we need to expand the grid
                numbers_needed = abs(target_num - current_start) + 1
                dim_required = math.ceil(math.sqrt(numbers_needed))
                if dim_required % 2 == 0: dim_required += 1
                new_rotations = (dim_required - 1) // 2
                self.rotations_var.set(str(new_rotations))
                self.display_gann_square() # This will redraw and call update_highlights
            else:
                # No need to redraw, just update colors
                self.update_highlights()

        except ValueError:
            messagebox.showerror("ورودی نامعتبر", "لطفاً برای عدد شروع و زاویه، مقادیر عددی صحیح وارد کنید.")
        except Exception as e:
            messagebox.showerror("خطا", f"یک خطای پیش‌بینی نشده رخ داد: {e}")

    # --- CORE FUNCTIONS (Unchanged logic, only highlight part is modified) ---
    
    def generate_gann_square_data(self, rotations: int, start_num: int, is_clockwise: bool):
        # This function is unchanged
        if rotations < 1: return None
        dim = 2 * rotations + 1
        grid = [[0] * dim for _ in range(dim)]
        x, y = rotations, rotations
        grid[y][x] = start_num
        current_val = start_num + 1
        if is_clockwise: path = [(-1, 0), (0, -1), (1, 0), (0, 1)] 
        else: path = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        steps_in_leg, turn_count, direction_idx = 1, 0, 0
        while current_val <= start_num + (dim**2 - 1):
            for _ in range(steps_in_leg):
                if current_val > start_num + (dim**2 - 1): break
                dx, dy = path[direction_idx]
                x, y = x + dx, y + dy
                grid[y][x] = current_val
                current_val += 1
            direction_idx = (direction_idx + 1) % 4
            turn_count += 1
            if turn_count % 2 == 0: steps_in_leg += 1
        return grid

    def handle_highlight_click(self):
        # This function is unchanged
        try:
            start_num = int(self.start_num_var.get())
            highlight_text = self.highlight_var.get()
            if not highlight_text:
                self.rotation_targets.clear() # Also clear green targets if main highlight is cleared
                self.update_highlights()
                return
            highlight_num = int(highlight_text)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers for Start Number and Highlight Number.")
            return
        dim = 2 * int(self.rotations_var.get()) + 1
        max_num_in_grid = start_num + dim**2 - 1
        if highlight_num > max_num_in_grid:
            numbers_needed = highlight_num - start_num + 1
            dim_required = math.ceil(math.sqrt(numbers_needed))
            if dim_required % 2 == 0: dim_required += 1
            new_rotations = (dim_required - 1) // 2
            self.rotations_var.set(str(new_rotations))
            self.display_gann_square()
        else:
            self.update_highlights()

    def update_highlights(self):
        """--- MODIFIED: Now handles two highlight colors ---"""
        blue_highlight_num = None
        try:
            highlight_text = self.highlight_var.get()
            if highlight_text: blue_highlight_num = int(highlight_text)
        except ValueError: pass

        for r, row_widgets in enumerate(self.cell_widgets):
            for c, cell_widget in enumerate(row_widgets):
                cell_value = self.gann_data[r][c]
                if cell_value == blue_highlight_num:
                    bg_color = "#a0c4ff" # Light Blue
                elif cell_value in self.rotation_targets:
                    bg_color = "#a7f0a7" # Light Green
                else:
                    bg_color = "#ffffff" # White
                cell_widget.config(bg=bg_color)
                
    def display_gann_square(self):
        # This function is unchanged
        try:
            start_num = int(self.start_num_var.get())
            rotations = int(self.rotations_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return
        if rotations < 1:
            messagebox.showerror("Error", "'Number of Rotations' must be 1 or greater.")
            return
        is_clockwise = self.direction_var.get() == "Clockwise"
        self.gann_data = self.generate_gann_square_data(rotations, start_num, is_clockwise)
        if not self.gann_data: return
        for row_cells in self.cell_widgets:
            for cell in row_cells: cell.destroy()
        self.cell_widgets.clear()
        dim = len(self.gann_data)
        if dim <= 3: font_size = 28
        elif dim <= 5: font_size = 20
        elif dim <= 7: font_size = 16
        else: font_size = 12
        cell_font = ("Arial", font_size, "bold")
        max_num_width = len(str(start_num + (dim**2 - 1)))
        for r in range(dim):
            row_widgets = []
            for c in range(dim):
                cell_value = self.gann_data[r][c]
                cell_text = f"{cell_value:>{max_num_width}}"
                cell = tk.Label(self.grid_display_frame, text=cell_text, font=cell_font, borderwidth=1, relief="solid", bg="#ffffff", fg="#333333")
                cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_widgets.append(cell)
                self.grid_display_frame.grid_columnconfigure(c, weight=1)
            self.cell_widgets.append(row_widgets)
            self.grid_display_frame.grid_rowconfigure(r, weight=1)
        self.update_highlights()
        self.master.update_idletasks()
        # The window resizing logic can be removed to let the user control the size
        # required_height = self.grid_display_frame.winfo_reqheight() + self.input_frame.winfo_reqheight() + 80
        # required_width = self.grid_display_frame.winfo_reqwidth() + 60
        # self.master.geometry(f"{required_width}x{required_height}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GannSquareGUI(root)
    root.mainloop()