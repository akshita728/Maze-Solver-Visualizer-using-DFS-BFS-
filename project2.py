import tkinter as tk
from tkinter import messagebox
import random
import time
from collections import deque

class MazeSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")

        # Maze settings
        self.rows = 15
        self.cols = 20
        self.cell_size = 30
        self.maze = []
        self.visited = set()
        self.path = []
        self.is_running = False

        # Colors
        self.colors = {
            "wall": "#000000",
            "empty": "#ffffff",
            "start": "#00ff00",
            "end": "#ff0000",
            "visited": "#64b5f6",
            "path": "#ffd700"
        }

        self.setup_ui()
        self.generate_maze()

    # ---------------- UI ----------------
    def setup_ui(self):
        title = tk.Label(
            self.root, text="🧩 Maze Solver Visualizer",
            font=("Arial", 22, "bold"),
            fg="#00d4ff", bg="#1a1a2e"
        )
        title.pack(pady=10)

        control = tk.Frame(self.root, bg="#1a1a2e")
        control.pack(pady=5)

        tk.Label(control, text="Rows", fg="white", bg="#1a1a2e").grid(row=0, column=0)
        self.rows_scale = tk.Scale(control, from_=10, to=25, orient="horizontal",
                                   command=self.on_size_change)
        self.rows_scale.set(self.rows)
        self.rows_scale.grid(row=0, column=1)

        tk.Label(control, text="Cols", fg="white", bg="#1a1a2e").grid(row=1, column=0)
        self.cols_scale = tk.Scale(control, from_=10, to=30, orient="horizontal",
                                   command=self.on_size_change)
        self.cols_scale.set(self.cols)
        self.cols_scale.grid(row=1, column=1)

        self.algorithm = tk.StringVar(value="dfs")
        tk.Radiobutton(control, text="DFS", variable=self.algorithm,
                       value="dfs", bg="#1a1a2e", fg="white").grid(row=0, column=2, padx=10)
        tk.Radiobutton(control, text="BFS", variable=self.algorithm,
                       value="bfs", bg="#1a1a2e", fg="white").grid(row=1, column=2, padx=10)

        tk.Button(control, text="▶ Solve", command=self.solve_maze,
                  bg="#00c853", fg="white", width=10).grid(row=0, column=3, padx=10)
        tk.Button(control, text="🔄 Reset", command=self.generate_maze,
                  bg="#7c4dff", fg="white", width=10).grid(row=1, column=3, padx=10)

        self.canvas = tk.Canvas(self.root, bg="#16213e")
        self.canvas.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

    # ---------------- Maze ----------------
    def on_size_change(self, event=None):
        if not self.is_running:
            self.rows = self.rows_scale.get()
            self.cols = self.cols_scale.get()
            self.generate_maze()

    def generate_maze(self):
        self.maze = []
        self.visited.clear()
        self.path.clear()

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if (i, j) in [(0, 0), (self.rows - 1, self.cols - 1)]:
                    row.append(0)
                else:
                    row.append(1 if random.random() < 0.25 else 0)
            self.maze.append(row)

        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.get_cell_color(i, j),
                    outline="#333",
                    tags=f"cell_{i}_{j}"
                )

    def get_cell_color(self, r, c):
        if (r, c) == (0, 0):
            return self.colors["start"]
        if (r, c) == (self.rows - 1, self.cols - 1):
            return self.colors["end"]
        if (r, c) in self.path:
            return self.colors["path"]
        if (r, c) in self.visited:
            return self.colors["visited"]
        if self.maze[r][c] == 1:
            return self.colors["wall"]
        return self.colors["empty"]

    def update_cell(self, r, c):
        self.canvas.itemconfig(f"cell_{r}_{c}", fill=self.get_cell_color(r, c))
        self.canvas.update()

    # ---------------- Solver ----------------
    def solve_maze(self):
        if self.is_running:
            return

        self.is_running = True
        self.visited.clear()
        self.path.clear()

        if self.algorithm.get() == "dfs":
            self.solve_dfs()
        else:
            self.solve_bfs()

        if self.path:
            self.draw_final_path()
        else:
            messagebox.showinfo("No Solution", "No path found!")

        self.is_running = False

    def solve_dfs(self):
        found = False

        def dfs(r, c, cur_path):
            nonlocal found
            if found:
                return
            if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
                return
            if self.maze[r][c] == 1 or (r, c) in self.visited:
                return

            self.visited.add((r, c))
            cur_path.append((r, c))
            self.update_cell(r, c)
            time.sleep(0.03)

            if (r, c) == (self.rows - 1, self.cols - 1):
                self.path = cur_path.copy()
                found = True
                return

            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                dfs(r + dr, c + dc, cur_path)

            cur_path.pop()

        dfs(0, 0, [])

    def solve_bfs(self):
        q = deque([(0, 0, [(0, 0)])])
        self.visited.add((0, 0))

        while q:
            r, c, cur_path = q.popleft()
            self.update_cell(r, c)
            time.sleep(0.03)

            if (r, c) == (self.rows - 1, self.cols - 1):
                self.path = cur_path
                return

            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.maze[nr][nc] == 0 and (nr, nc) not in self.visited:
                        self.visited.add((nr, nc))
                        q.append((nr, nc, cur_path + [(nr, nc)]))

    def draw_final_path(self):
        for r, c in self.path:
            if (r, c) not in [(0,0),(self.rows-1,self.cols-1)]:
                self.canvas.itemconfig(f"cell_{r}_{c}", fill=self.colors["path"])
                self.canvas.update()
                time.sleep(0.04)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    MazeSolver(root)
    root.mainloop()
