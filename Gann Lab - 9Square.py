import tkinter as tk
from tkinter import ttk, messagebox
import math

class GannSquareGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Square Generator - Optimized")
        self.master.geometry("700x900") # یک اندازه شروع پیش‌فرض مناسب
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ... (تنظیمات استایل بدون تغییر) ...
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Tahoma", 11))
        self.style.configure("TButton", font=("Tahoma", 12, "bold"), padding=10)
        self.style.configure("TEntry", font=("Tahoma", 12), padding=5)
        self.style.configure("TMenubutton", font=("Tahoma", 11))
        self.style.configure("Result.TLabel", font=("Tahoma", 12, "bold"), foreground="darkblue")

        # --- جدید: تنظیم فریم اصلی قابل اسکرول ---
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill="both", expand=True)

        self.scrollable_canvas = tk.Canvas(main_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.scrollable_canvas.yview)
        self.scrollable_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.scrollable_canvas.pack(side="left", fill="both", expand=True)

        # --- اتصال اسکرول ماوس برای ویندوز، مک و لینوکس ---
        self.scrollable_canvas.bind_all("<MouseWheel>", self._on_mousewheel) # Windows
        self.scrollable_canvas.bind_all("<Button-4>", self._on_mousewheel)   # Linux (Scroll Up)
        self.scrollable_canvas.bind_all("<Button-5>", self._on_mousewheel)   # Linux (Scroll Down)

        self.content_frame = ttk.Frame(self.scrollable_canvas)
        self.scrollable_canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        self.content_frame.bind("<Configure>", lambda e: self.scrollable_canvas.configure(scrollregion=self.scrollable_canvas.bbox("all")))
        
        # --- تمام ویجت‌ها اکنون داخل self.content_frame قرار می‌گیرند ---
        self.input_frame = ttk.Frame(self.content_frame, padding="15")
        self.input_frame.pack(pady=(10,0), fill="x", anchor="n")
        self.input_frame.columnconfigure(1, weight=1)

        # ... (تمام ویجت‌های ورودی شما بدون تغییر اینجا قرار می‌گیرند) ...
        ttk.Label(self.input_frame, text="Start Number (Center):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_num_var = tk.StringVar(value="1")
        self.start_num_entry = ttk.Entry(self.input_frame, textvariable=self.start_num_var)
        self.start_num_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ttk.Label(self.input_frame, text="Increment:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.increment_var = tk.StringVar(value="1")
        self.increment_entry = ttk.Entry(self.input_frame, textvariable=self.increment_var)
        self.increment_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ttk.Label(self.input_frame, text="Number of Rotations (Layers):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.rotations_var = tk.StringVar(value="8")
        self.rotations_entry = ttk.Entry(self.input_frame, textvariable=self.rotations_var)
        self.rotations_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ttk.Label(self.input_frame, text="Spiral Direction:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.direction_var = tk.StringVar(value="Clockwise")
        self.direction_menu = ttk.OptionMenu(self.input_frame, self.direction_var, "Clockwise", "Clockwise", "Counter-Clockwise")
        self.direction_menu.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        ttk.Label(self.input_frame, text="Highlight Number:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.highlight_var = tk.StringVar(value="")
        self.highlight_entry = ttk.Entry(self.input_frame, textvariable=self.highlight_var)
        self.highlight_entry.grid(row=4, column=1, padx=(10, 2), pady=5, sticky="ew")
        self.search_button = ttk.Button(self.input_frame, text="🔍", command=self.handle_highlight_click)
        self.search_button.grid(row=4, column=2, padx=(0, 10), pady=5, sticky="w")
        self.input_frame.columnconfigure(2, weight=0)
        self.generate_button = ttk.Button(self.input_frame, text="Generate / Redraw Square", command=self.display_gann_square)
        self.generate_button.grid(row=5, column=0, columnspan=3, pady=8, sticky="ew", padx=10)

        # --- جدید: گرید اکنون یک ویجت Canvas است ---
        self.grid_canvas = tk.Canvas(self.content_frame, bg="white", highlightthickness=1, highlightbackground="grey")
        self.grid_canvas.pack(expand=True, fill="both", padx=15, pady=(5,10), anchor="n")
        self.grid_canvas.bind("<Button-1>", self.on_canvas_click)

        # --- محاسبه‌گر چرخش ---
        self.rotation_calc_frame = ttk.LabelFrame(self.content_frame, text="Angular Rotation Calculator", padding="15")
        self.rotation_calc_frame.pack(fill="x", padx=15, pady=(0, 15), anchor="n")
        self.rotation_calc_frame.columnconfigure(1, weight=1)
        # ... (ویجت‌های محاسبه‌گر بدون تغییر اینجا قرار می‌گیرند) ...
        ttk.Label(self.rotation_calc_frame, text="Start Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.calc_start_num_var = tk.StringVar(value="49")
        ttk.Entry(self.rotation_calc_frame, textvariable=self.calc_start_num_var).grid(row=0, column=1, sticky="ew", padx=5)
        ttk.Label(self.rotation_calc_frame, text="Angle (degrees):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.calc_angle_var = tk.StringVar(value="180")
        ttk.Entry(self.rotation_calc_frame, textvariable=self.calc_angle_var).grid(row=1, column=1, sticky="ew", padx=5)
        ttk.Label(self.rotation_calc_frame, text="Number of Targets:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.calc_repeats_var = tk.StringVar(value="3")
        ttk.Entry(self.rotation_calc_frame, textvariable=self.calc_repeats_var).grid(row=2, column=1, sticky="ew", padx=5)
        ttk.Label(self.rotation_calc_frame, text="Direction:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.calc_direction_var = tk.StringVar(value="Higher")
        ttk.OptionMenu(self.rotation_calc_frame, self.calc_direction_var, "Higher", "Higher", "Lower").grid(row=3, column=1, sticky="ew", padx=5)
        ttk.Button(self.rotation_calc_frame, text="Calculate", command=self.calculate_gann_rotation).grid(row=4, column=0, columnspan=2, pady=10, sticky="ew", padx=5)
        ttk.Label(self.rotation_calc_frame, text="Target(s):").grid(row=5, column=0, padx=5, pady=5, sticky="nw")
        self.calc_result_text = tk.Text(self.rotation_calc_frame, height=3, font=("Tahoma", 11), relief="sunken", borderwidth=1)
        self.calc_result_text.grid(row=5, column=1, sticky="ew", padx=5)
        self.calc_result_text.insert("1.0", "---")
        self.calc_result_text.config(state="disabled")

        self.gann_data = []
        self.rotation_targets = set()
        self.cell_size = 0
        
        self.display_gann_square()

    def _on_mousewheel(self, event):
        # ... (کد این تابع در بالا آمده است) ...
        if event.num == 4 or event.delta > 0:
            self.scrollable_canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.scrollable_canvas.yview_scroll(1, "units")

    # ... (بقیه توابع شما بدون تغییر در اینجا قرار می‌گیرند) ...
    def on_canvas_click(self, event):
        if not self.gann_data or self.cell_size == 0: return
        canvas_width = self.grid_canvas.winfo_width()
        dim = len(self.gann_data)
        grid_size = dim * self.cell_size
        offset_x = (canvas_width - grid_size) / 2
        if event.x < offset_x or event.x > offset_x + grid_size: return
        col = int((event.x - offset_x) / self.cell_size)
        row = int(event.y / self.cell_size)
        if 0 <= row < dim and 0 <= col < dim:
            number = self.gann_data[row][col]
            self.calc_start_num_var.set(str(int(number)))
            self.highlight_var.set(str(int(number)))
            self.rotation_targets.clear()
            self.calc_result_text.config(state="normal")
            self.calc_result_text.delete("1.0", "end")
            self.calc_result_text.insert("1.0", "---")
            self.calc_result_text.config(state="disabled")
            self.update_highlights()

    def calculate_gann_rotation(self):
        # ... (این تابع بدون تغییر است) ...
        try:
            start_num_for_calc = float(self.calc_start_num_var.get())
            initial_angle = float(self.calc_angle_var.get())
            repeats = int(self.calc_repeats_var.get())
            direction = self.calc_direction_var.get()
            increment = float(self.increment_var.get())
            grid_start_num = float(self.start_num_var.get())
            if start_num_for_calc < grid_start_num or (start_num_for_calc - grid_start_num) % increment != 0:
                messagebox.showerror("Error", "The 'Start Number' for calculation must be a valid number within the grid's sequence.")
                return
            targets = []
            current_start_num = start_num_for_calc
            for i in range(repeats):
                current_angle = initial_angle if i == 0 else 360.0
                current_step = round((current_start_num - grid_start_num) / increment)
                sqrt_of_current_step = math.sqrt(current_step + 1)
                angle_factor = current_angle / 180.0
                if direction == "Higher":
                    result_step = (sqrt_of_current_step + angle_factor)**2
                else:
                    result_step = (sqrt_of_current_step - angle_factor)**2
                if result_step < 0: continue
                target_step = int(round(result_step)) - 1
                target_num = grid_start_num + (target_step * increment)
                targets.append(target_num)
                current_start_num = target_num
            self.calc_result_text.config(state="normal")
            self.calc_result_text.delete("1.0", "end")
            self.calc_result_text.insert("1.0", ", ".join(map(str, targets)))
            self.calc_result_text.config(state="disabled")
            self.rotation_targets = set(targets)
            if not targets:
                self.update_highlights()
                return
            max_target = max(targets)
            current_rotations = int(self.rotations_var.get())
            dim = 2 * current_rotations + 1
            max_num_in_grid = grid_start_num + ((dim**2 - 1) * increment)
            if max_target > max_num_in_grid or max_target < grid_start_num:
                if max_target < grid_start_num and direction == "Higher": pass
                else:
                    numbers_needed = abs(max_target - grid_start_num) / increment
                    dim_required = math.ceil(math.sqrt(numbers_needed + 1))
                    if dim_required % 2 == 0: dim_required += 1
                    new_rotations = (dim_required - 1) // 2
                    self.rotations_var.set(str(new_rotations))
                    self.display_gann_square()
            else:
                self.update_highlights()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def generate_gann_square_data(self, rotations, start_num, is_clockwise, increment):
        # ... (این تابع بدون تغییر است) ...
        if rotations < 1: return None
        dim = 2 * rotations + 1
        grid = [[0] * dim for _ in range(dim)]
        path_logic_positions = [[0] * dim for _ in range(dim)]
        pos_x, pos_y = rotations, rotations
        path_logic_positions[pos_y][pos_x] = 0
        current_step = 1
        if is_clockwise: path = [(-1, 0), (0, -1), (1, 0), (0, 1)] 
        else: path = [(1, 0), (0, -1), (-1, 0), (0, 1)]
        steps_in_leg, turn_count, direction_idx = 1, 0, 0
        while current_step < dim**2:
            for _ in range(steps_in_leg):
                if current_step >= dim**2: break
                dx, dy = path[direction_idx]
                pos_x, pos_y = pos_x + dx, pos_y + dy
                path_logic_positions[pos_y][pos_x] = current_step
                current_step += 1
            direction_idx = (direction_idx + 1) % 4
            turn_count += 1
            if turn_count % 2 == 0: steps_in_leg += 1
        for r in range(dim):
            for c in range(dim):
                step = path_logic_positions[r][c]
                grid[r][c] = start_num + (step * increment)
        return grid

    def update_highlights(self):
        self.grid_canvas.delete("highlights")
        blue_highlight_num = None
        try:
            highlight_text = self.highlight_var.get()
            if highlight_text: blue_highlight_num = float(highlight_text)
        except (ValueError, TypeError): pass
        if not self.gann_data or self.cell_size == 0: return
        canvas_width = self.grid_canvas.winfo_width()
        dim = len(self.gann_data)
        grid_size = dim * self.cell_size
        offset_x = (canvas_width - grid_size) / 2
        for r, row_data in enumerate(self.gann_data):
            for c, cell_value in enumerate(row_data):
                bg_color = None
                if cell_value == blue_highlight_num:
                    bg_color = "#a0c4ff"
                elif cell_value in self.rotation_targets:
                    bg_color = "#a7f0a7"
                if bg_color:
                    x1 = c * self.cell_size + offset_x
                    y1 = r * self.cell_size
                    x2 = x1 + self.cell_size
                    y2 = y1 + self.cell_size
                    self.grid_canvas.create_rectangle(x1, y1, x2, y2, fill=bg_color, outline="", tags="highlights")
        self.grid_canvas.tag_raise("numbers")

    def display_gann_square(self):
        try:
            start_num = int(self.start_num_var.get())
            rotations = int(self.rotations_var.get())
            increment = int(self.increment_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return
        is_clockwise = self.direction_var.get() == "Clockwise"
        self.gann_data = self.generate_gann_square_data(rotations, start_num, is_clockwise, increment)
        if not self.gann_data: return
        self.grid_canvas.delete("all")
        dim = len(self.gann_data)
        parent_width = self.content_frame.winfo_width()
        if parent_width <= 1: parent_width = self.master.winfo_width()
        parent_width = parent_width - 30 # Account for padding
        self.cell_size = parent_width / dim
        required_size = dim * self.cell_size
        self.grid_canvas.config(width=required_size, height=required_size)
        font_size = max(6, int(self.cell_size * 0.4))
        cell_font = ("Arial", font_size)
        
        # This offset ensures the grid is centered within the canvas
        offset_x = (required_size - (dim * self.cell_size)) / 2
        
        for r in range(dim):
            for c in range(dim):
                cell_value = self.gann_data[r][c]
                x1 = c * self.cell_size + offset_x
                y1 = r * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.grid_canvas.create_rectangle(x1, y1, x2, y2, outline="#ccc", fill="white")
                self.grid_canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(int(cell_value)), font=cell_font, fill="black", tags="numbers")
        self.update_highlights()

    def handle_highlight_click(self):
        # ... (این تابع بدون تغییر است) ...
        try:
            start_num = int(self.start_num_var.get())
            increment = int(self.increment_var.get())
            highlight_text = self.highlight_var.get()
            if not highlight_text:
                self.rotation_targets.clear()
                self.update_highlights()
                return
            highlight_num = int(highlight_text)
            if (highlight_num - start_num) % increment != 0:
                messagebox.showwarning("Not Found", f"The number {highlight_num} does not exist in the sequence.")
                self.highlight_var.set("")
                self.update_highlights()
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integers.")
            return
        current_rotations = int(self.rotations_var.get())
        dim = 2 * current_rotations + 1
        max_num_in_grid = start_num + ((dim**2 - 1) * increment)
        if highlight_num > max_num_in_grid:
            steps_needed = (highlight_num - start_num) / increment
            dim_required = math.ceil(math.sqrt(steps_needed + 1))
            if dim_required % 2 == 0: dim_required += 1
            new_rotations = (dim_required - 1) // 2
            self.rotations_var.set(str(new_rotations))
            self.display_gann_square()
        else:
            self.update_highlights()


if __name__ == "__main__":
    root = tk.Tk()
    app = GannSquareGUI(root)
    root.mainloop()