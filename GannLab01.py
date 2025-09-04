import tkinter as tk
from tkinter import ttk, messagebox

class GannSquareGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Gann Square Generator")
        self.master.geometry("600x750")
        self.master.minsize(500, 600)
        
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Tahoma", 11))
        self.style.configure("TButton", font=("Tahoma", 12, "bold"), padding=10)
        self.style.configure("TEntry", font=("Tahoma", 12), padding=5)
        self.style.configure("TMenubutton", font=("Tahoma", 11))

        self.input_frame = ttk.Frame(self.master, padding="15")
        self.input_frame.pack(pady=10, fill="x")
        self.input_frame.columnconfigure(1, weight=1)

        ttk.Label(self.input_frame, text="Start Number (Center):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.start_num_var = tk.StringVar(value="1")
        self.start_num_entry = ttk.Entry(self.input_frame, textvariable=self.start_num_var)
        self.start_num_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        
        ttk.Label(self.input_frame, text="Number of Rotations (Layers):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.rotations_var = tk.StringVar(value="1")
        self.rotations_entry = ttk.Entry(self.input_frame, textvariable=self.rotations_var)
        self.rotations_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        ttk.Label(self.input_frame, text="Spiral Direction:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.direction_var = tk.StringVar(value="Clockwise")
        self.direction_menu = ttk.OptionMenu(self.input_frame, self.direction_var, "Clockwise", "Clockwise", "Counter-Clockwise")
        self.direction_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.generate_button = ttk.Button(self.input_frame, text="Generate Gann Square", command=self.display_gann_square)
        self.generate_button.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew", padx=10)

        self.grid_display_frame = ttk.Frame(self.master, padding="10", relief="groove", borderwidth=2)
        self.grid_display_frame.pack(expand=True, fill="both", padx=15, pady=10)
        
        self.cells = []
        self.display_gann_square()

    def generate_gann_square_data(self, rotations: int, start_num: int, is_clockwise: bool):
        """
        COMPLETELY REWRITTEN AND ROBUST: Generates a Gann Square with fixed 1, 2, and correct spiral direction.
        This new algorithm is simpler and corrects all previous bugs.
        """
        if rotations < 1: return None
        dim = 2 * rotations + 1
        grid = [[0] * dim for _ in range(dim)]
        
        x, y = rotations, rotations
        
        # --- FIXED START ---
        grid[y][x] = start_num
        current_val = start_num + 1
        
        # --- DYNAMIC SPIRAL PART ---
        # Define direction vectors based on the chosen spiral path
        if is_clockwise:
            # Standard Gann path: L, U, R, D, L, U ...
            # The vectors correspond to a path that starts Left from the center
            path = [(-1, 0), (0, -1), (1, 0), (0, 1)] 
        else: # Counter-Clockwise
            # Mirrored path: L, D, R, U, L, D ...
            path = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        steps_in_leg = 1
        turn_count = 0
        direction_idx = 0

        while current_val <= start_num + (dim**2 - 1):
            # Take a number of steps in the current direction
            for _ in range(steps_in_leg):
                if current_val > start_num + (dim**2 - 1): break
                dx, dy = path[direction_idx]
                x, y = x + dx, y + dy
                grid[y][x] = current_val
                current_val += 1
            
            # Change direction
            direction_idx = (direction_idx + 1) % 4
            turn_count += 1
            
            # Increase the number of steps every two turns
            if turn_count % 2 == 0:
                steps_in_leg += 1
        
        return grid

    def display_gann_square(self):
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
        final_data = self.generate_gann_square_data(rotations, start_num, is_clockwise)

        if not final_data: return

        for row_cells in self.cells:
            for cell in row_cells: cell.destroy()
        self.cells.clear()

        dim = len(final_data)
        
        if dim <= 3: font_size = 28
        elif dim <= 5: font_size = 20
        elif dim <= 7: font_size = 16
        else: font_size = 12

        cell_font = ("Arial", font_size, "bold")
        max_num_width = len(str(start_num + (dim**2 - 1)))

        for r in range(dim):
            row_cells = []
            for c in range(dim):
                cell_value = final_data[r][c]
                cell_text = f"{cell_value:>{max_num_width}}"
                cell = tk.Label(self.grid_display_frame, text=cell_text, font=cell_font, borderwidth=1, relief="solid", bg="#ffffff", fg="#333333")
                cell.grid(row=r, column=c, padx=1, pady=1, sticky="nsew")
                row_cells.append(cell)
                self.grid_display_frame.grid_columnconfigure(c, weight=1)
            self.cells.append(row_cells)
            self.grid_display_frame.grid_rowconfigure(r, weight=1)
            
        self.master.update_idletasks()
        required_height = self.grid_display_frame.winfo_reqheight() + self.input_frame.winfo_reqheight() + 80
        required_width = self.grid_display_frame.winfo_reqwidth() + 60
        self.master.geometry(f"{required_width}x{required_height}")

if __name__ == "__main__":
    root = tk.Tk()
    app = GannSquareGUI(root)
    root.mainloop()