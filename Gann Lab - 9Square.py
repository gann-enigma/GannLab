import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
import math

class GannSquareGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Square Generator")
        self.master.geometry("600x800")
        self.master.minsize(500, 600)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ... (style configurations remain the same) ...

        self.input_frame = ttk.Frame(self.master, padding="15")
        self.input_frame.pack(pady=10, fill="x")
        self.input_frame.columnconfigure(1, weight=1)

        # ... (other input widgets remain the same) ...
        ttk.Label(self.input_frame, text="Start Number (Center):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_num_var = tk.StringVar(value="1")
        self.start_num_entry = ttk.Entry(self.input_frame, textvariable=self.start_num_var)
        self.start_num_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Number of Rotations (Layers):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rotations_var = tk.StringVar(value="1")
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

        # --- MODIFIED: Added a try-except block for robust icon loading ---
        try:
            search_icon_data = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAAAAlwSFlzAAAOwgAADsIBFShKgAAAAdpJREFUOE+N07Fr1EAUxfF3d5JSSmErDbYhYCFYCIJaRHxopZcm65eQyG61sYVf4D9YsFAQTAR7tVCwsBEhhYVgIaj+gChYSISgkp97d5k5dwf+4HDfzH3P3Lk7mSA/BEEQDBLp9L+j0VCSqEaj0eh2u+M4jlQul6mUag6HwzAMA4lEglweD15X1QZ/5+g00F/ARwA2gKVEZW7+kC0AsoBMQv5zPlmft/bL5/Nhc3MTb/f7/bFarbIsC4vFAl3XBSLh8/kQCATgpQ9W3QDg+4Pj8Xjo9/u334OrMNPpxPqdZrM5l8t13+/311ardTqd6Xa70+l0aDay2WxGo9Hor+MwjUaDfD6/bDaL5XLRbreJSqXg+36/308mkzAYDJrNJv1+n16vd3f+c2q1mkAoqpRKpbjdfkZ/fX39/f2NQqGgWq0iBUEQh72E262srCRpa0lSlkVRhB6Ph8Vi8Xq9/vL5/N5gMIj9/f2M2+1iPB6/D/fC4fAorF8uF7lcls1mYTabiLHL5UK73WZZFt1ul0wmc/j9fm+324vF4ufn50KhkM1mI7FYDCAaDAbRaLTZbLa93S6RSCL7y4ODg6/X69HI+3d4elAul+mYj1KpRFEURVH0+331er0O5I1Goy+Wyx6Ph/8pvgGnj0Yj+H4fTdOQJAmiKILv+8dxDAAqlUoymQAA6/X6TqcDlmXh+36VSoV2u/0H+Hhhr9cbjUb5fB5FUZzNZtPtdr9bX129Xl8+n5eU4D+aTqdjWZZ+v//BYBCbzQYgy7IoisqyrMFgACf/R+E/iUajkCSJ7/v5fJ4sy2JZFk3TwOPx4DgOvu+rVCqTyUQikUj9/f33B8PBAIDjOGi12tVqBSS/A0AqlUr9fj+dTgckm03TmM1mk/4m2p45ODj4fX8V4T/n8/kLNRqNgY+Pj2az2dbW1rVarXw+PzExMXl8fPy/Cg8M5vN5x3E8KBeLIsg29/f34/F4OBwOrVbr7OwsDA8PD25ubtpaVVWSpCiKQpIkDPs/ODhA9/1+v5+ORkVR1+s1n8/7N/5eWRTFkG+fz/e/f4Bfl8sFz/Mxxq6urjP5naVSCQDgB/h/kC/4/f43mUyGz+czGAzW6/XWajW73V4sFhsMBm1m8+x6fR499/T05PDwELqun5+fW5ZFIpH4+/v3+/u7ra3t+Pj4+PhYVVWSpGn6ff83f4L+B35/KRQKk8l8D4bDRkZG/wH5lMkkDEMAAO7eBQC4e/cDALi7/w/4fAAAPh8PANj1/Q8ATs4GAAzmgwDAaD4VANCMz4cBwAi/n3UAl/5lMplOp0MB+P39/f1+f3t72+v1Op1OhUIh8/Pz/5F/ALz/C/8DoL+JSA3+YxkAAAAASUVORK5CYII='
            # Keep a reference to the image to prevent it from being garbage-collected
            self.search_icon = PhotoImage(data=search_icon_data)
            self.search_button = ttk.Button(self.input_frame, image=self.search_icon, command=self.handle_highlight_click)
        except tk.TclError:
            # If the icon fails to load, create a simple text button as a fallback
            self.search_button = ttk.Button(self.input_frame, text="🔍", command=self.handle_highlight_click)
        
        self.search_button.grid(row=3, column=2, padx=(0, 10), pady=5, sticky="w")
        self.input_frame.columnconfigure(2, weight=0)

        self.generate_button = ttk.Button(self.input_frame, text="Generate / Redraw Square", command=self.display_gann_square)
        self.generate_button.grid(row=4, column=0, columnspan=3, pady=15, sticky="ew", padx=10)

        self.grid_display_frame = ttk.Frame(self.master, padding="10", relief="groove", borderwidth=2)
        self.grid_display_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        self.cell_widgets = []
        self.gann_data = []
        self.display_gann_square()

    def generate_gann_square_data(self, rotations: int, start_num: int, is_clockwise: bool):
        if rotations < 1: return None
        dim = 2 * rotations + 1
        grid = [[0] * dim for _ in range(dim)]
        x, y = rotations, rotations
        
        grid[y][x] = start_num
        current_val = start_num + 1

        if is_clockwise:
            # CORRECT: This path starts Left, then Up, ensuring 2 is left of 1 and 3 is above 2.
            # Path: Left -> Up -> Right -> Down
            path = [(-1, 0), (0, -1), (1, 0), (0, 1)] 
        else: # Counter-Clockwise
            # NEW CORRECTED PATH:
            # Starts Right (so 2 is right of 1), then Up (so 3 is above 2).
            # Path: Right -> Up -> Left -> Down
            path = [(1, 0), (0, -1), (-1, 0), (0, 1)]
            
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
            if turn_count % 2 == 0:
                steps_in_leg += 1
                
        return grid

    def handle_highlight_click(self):
        # ... (This function remains unchanged) ...
        try:
            start_num = int(self.start_num_var.get())
            highlight_text = self.highlight_var.get()
            if not highlight_text:
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
        # ... (This function remains unchanged) ...
        highlight_num = None
        try:
            highlight_text = self.highlight_var.get()
            if highlight_text: highlight_num = int(highlight_text)
        except ValueError: return

        for r, row_widgets in enumerate(self.cell_widgets):
            for c, cell_widget in enumerate(row_widgets):
                cell_value = self.gann_data[r][c]
                bg_color = "#a0c4ff" if cell_value == highlight_num else "#ffffff"
                cell_widget.config(bg=bg_color)
                
    def display_gann_square(self):
        # ... (This function remains unchanged) ...
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
        required_height = self.grid_display_frame.winfo_reqheight() + self.input_frame.winfo_reqheight() + 80
        required_width = self.grid_display_frame.winfo_reqwidth() + 60
        self.master.geometry(f"{required_width}x{required_height}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GannSquareGUI(root)
    root.mainloop()