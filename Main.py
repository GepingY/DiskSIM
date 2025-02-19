import tkinter as tk
from tkinter import ttk

class HardDriveSimulator:
    def __init__(self, master):
        self.master = master
        master.title("Hard Drive Simulator")
        
        # Define the grid layout for blocks
        self.grid_size = 50  # Even wider with more blocks
        self.block_size = 20  # Even smaller blocks
        self.padding = 3      # Even less padding for closer packing
        self.blocks = []
        
        # Create canvas
        self.canvas = tk.Canvas(master, width=self.grid_size * (self.block_size + self.padding), 
                                height=self.block_size + 2 * self.padding)
        self.canvas.pack()
        
        # Create the fixed positions for blocks (still only one row)
        for j in range(self.grid_size):
            x1 = j * (self.block_size + self.padding)
            y1 = self.padding
            x2 = x1 + self.block_size
            y2 = y1 + self.block_size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", tags=f"spot_{j}")

        # Add draggable blocks
        colors = ["red", "blue", "green", "yellow", "purple", "orange", "cyan", "magenta", "pink", "lime"]
        for i in range(30):  # 30 movable blocks with more variety in colors
            self.create_block(i % self.grid_size, colors[i % len(colors)])  # Place initial blocks spread out

    def create_block(self, grid_x, color):
        x1 = grid_x * (self.block_size + self.padding)
        y1 = self.padding
        x2 = x1 + self.block_size
        y2 = y1 + self.block_size
        
        block = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=("block", f"block_{len(self.blocks)}"))
        self.blocks.append(block)
        
        self.canvas.tag_bind(block, "<ButtonPress-1>", self.on_drag_start)
        self.canvas.tag_bind(block, "<ButtonRelease-1>", self.on_drag_stop)
        self.canvas.tag_bind(block, "<B1-Motion>", self.on_dragging)

    def on_drag_start(self, event):
        self._drag_data = {"item": self.canvas.find_closest(event.x, event.y)[0],
                           "x": event.x, "y": event.y}

    def on_drag_stop(self, event):
        # Snap block to grid
        block = self._drag_data["item"]
        block_x = event.x
        
        closest_spot = None
        min_distance = float('inf')
        
        for j in range(self.grid_size):
            spot = self.canvas.find_withtag(f"spot_{j}")[0]
            x1, y1, x2, y2 = self.canvas.coords(spot)
            center_x = (x1 + x2) / 2
            distance = abs(center_x - block_x)
            if distance < min_distance:
                min_distance = distance
                closest_spot = spot

        if closest_spot:
            x1, y1, _, _ = self.canvas.coords(closest_spot)
            self.canvas.coords(block, x1, y1, x1 + self.block_size, y1 + self.block_size)
        
        self._drag_data = None

    def on_dragging(self, event):
        delta_x = event.x - self._drag_data["x"]
        self.canvas.move(self._drag_data["item"], delta_x, 0)
        self._drag_data["x"] = event.x

if __name__ == "__main__":
    root = tk.Tk()
    app = HardDriveSimulator(root)
    root.mainloop()
