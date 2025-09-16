import tkinter as tk
from tkinter import ttk, messagebox
import math

class GannSquareGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Square Generator - Interactive")
        self.master.geometry("600x1050") # Increased height for the new section
        self.master.minsize(500, 800)
        
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
        
        ttk.Label(self.input_frame, text="Increment:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.increment_var = tk.StringVar(value="1")
        self.increment_entry = ttk.Entry(self.input_frame, textvariable=self.increment_var)
        self.increment_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky="ew")

        ttk.Label(self.input_frame, text="Number of Rotations (Layers):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.rotations_var = tk.StringVar(value="4")
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

        # --- Grid Display Frame (unchanged) ---
        self.grid_display_frame = ttk.Frame(self.master, padding="10", relief="groove", borderwidth=2)
        self.grid_display_frame.pack(expand=True, fill="both", padx=15, pady=(5,10))
        
        # --- Rotation Calculator Frame (MODIFIED) ---
        self.rotation_calc_frame = ttk.LabelFrame(self.master, text="Angular Rotation Calculator", padding="15")
        self.rotation_calc_frame.pack(fill="x", padx=15, pady=(0, 15))
        self.rotation_calc_frame.columnconfigure(1, weight=1)

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

        # --- Instance variables ---
        self.cell_widgets = []
        self.gann_data = []
        self.rotation_targets = set()
        
        self.display_gann_square()

    def on_cell_click(self, number):
        """--- MODIFIED: Handles clicks to update both calculator and highlight ---"""
        self.calc_start_num_var.set(str(int(number))) # Set number for calculator
        self.highlight_var.set(str(int(number)))     # Set number for blue highlight
        self.rotation_targets.clear()                # Clear any green targets
        self.calc_result_text.config(state="normal")
        self.calc_result_text.delete("1.0", "end")
        self.calc_result_text.insert("1.0", "---")
        self.calc_result_text.config(state="disabled")
        self.update_highlights()                     # Apply the blue highlight immediately

    def calculate_gann_rotation(self):
        """--- DEFINITIVE VERSION: Calculates the first target with the user's angle,
        and subsequent targets by adding/subtracting 360 degrees from the previous target. ---"""
        try:
            # Read all necessary values from the GUI
            start_num_for_calc = float(self.calc_start_num_var.get())
            initial_angle = float(self.calc_angle_var.get())
            repeats = int(self.calc_repeats_var.get())
            direction = self.calc_direction_var.get()
            
            increment = float(self.increment_var.get())
            grid_start_num = float(self.start_num_var.get())

            # --- Validation ---
            if start_num_for_calc < grid_start_num or (start_num_for_calc - grid_start_num) % increment != 0:
                messagebox.showerror("Error", "The 'Start Number' for calculation must be a valid number within the grid's sequence.")
                return
            
            # --- Core Chained Calculation Logic ---
            targets = []
            # This variable will hold the number we're currently calculating FROM.
            # It starts as the user's initial number.
            current_start_num = start_num_for_calc
            
            for i in range(repeats):
                # The angle is the user's angle for the first target (i=0), and 360 for all others.
                current_angle = initial_angle if i == 0 else 360.0

                # 1. Convert the current number to its "step" index
                current_step = round((current_start_num - grid_start_num) / increment)
                sqrt_of_current_step = math.sqrt(current_step + 1)
                
                # 2. Calculate the angle factor
                angle_factor = current_angle / 180.0
                
                if direction == "Higher":
                    result_step = (sqrt_of_current_step + angle_factor)**2
                else: # Lower
                    result_step = (sqrt_of_current_step - angle_factor)**2
                
                if result_step < 0: continue
                
                # 3. Convert the calculated step back to a real number
                target_step = int(round(result_step)) - 1
                target_num = grid_start_num + (target_step * increment)
                targets.append(target_num)
                
                # 4. The new start number for the next iteration is the target we just found
                current_start_num = target_num

            # Update the result text box
            self.calc_result_text.config(state="normal")
            self.calc_result_text.delete("1.0", "end")
            self.calc_result_text.insert("1.0", ", ".join(map(str, targets)))
            self.calc_result_text.config(state="disabled")
            
            self.rotation_targets = set(targets)
            
            # --- Auto-expand logic (unchanged) ---
            if not targets:
                self.update_highlights()
                return

            max_target = max(targets)
            current_rotations = int(self.rotations_var.get())
            dim = 2 * current_rotations + 1
            max_num_in_grid = grid_start_num + ((dim**2 - 1) * increment)

            if max_target > max_num_in_grid or max_target < grid_start_num:
                if max_target < grid_start_num and direction == "Higher":
                    pass
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
    
    # --- CORE FUNCTIONS (Unchanged logic, except for adding click binding) ---
    def generate_gann_square_data(self, rotations, start_num, is_clockwise, increment):
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
        for row_cells in self.cell_widgets:
            for cell in row_cells: cell.destroy()
        self.cell_widgets.clear()
        dim = len(self.gann_data)
        font_size = 28
        if dim > 3: font_size = 20
        if dim > 5: font_size = 16
        if dim > 9: font_size = 12
        cell_font = ("Arial", font_size, "bold")
        max_num = start_num + ((dim**2 - 1) * increment)
        max_num_width = len(str(int(max_num)))
        for r in range(dim):
            row_widgets = []
            for c in range(dim):
                cell_value = self.gann_data[r][c]
                cell_text = f"{int(cell_value):>{max_num_width}}"
                cell = tk.Label(self.grid_display_frame, text=cell_text, font=cell_font, borderwidth=1, relief="solid", bg="#ffffff", fg="#333333")
                cell.bind("<Button-1>", lambda event, num=cell_value: self.on_cell_click(num))
                cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_widgets.append(cell)
                self.grid_display_frame.grid_columnconfigure(c, weight=1)
            self.cell_widgets.append(row_widgets)
            self.grid_display_frame.grid_rowconfigure(r, weight=1)
        self.update_highlights()

    # --- Other functions (handle_highlight_click, update_highlights) remain the same ---
    def handle_highlight_click(self):
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

    def update_highlights(self):
        blue_highlight_num = None
        try:
            highlight_text = self.highlight_var.get()
            if highlight_text: blue_highlight_num = float(highlight_text)
        except (ValueError, TypeError): pass
        for r, row_widgets in enumerate(self.cell_widgets):
            for c, cell_widget in enumerate(row_widgets):
                cell_value = self.gann_data[r][c]
                if cell_value == blue_highlight_num:
                    bg_color = "#a0c4ff"
                elif cell_value in self.rotation_targets:
                    bg_color = "#a7f0a7"
                else:
                    bg_color = "#ffffff"
                cell_widget.config(bg=bg_color)


if __name__ == "__main__":
    root = tk.Tk()
    app = GannSquareGUI(root)
    root.mainloop()