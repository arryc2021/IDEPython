import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

class PythonIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Python IDE")

        self.text_area = tk.Text(root, font=("Consolas", 12), wrap=tk.NONE, undo=True)
        self.text_area.pack(fill=tk.BOTH, expand=1)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        run_menu = tk.Menu(self.menu, tearoff=0)
        run_menu.add_command(label="Run", command=self.run_code)
        self.menu.add_cascade(label="Run", menu=run_menu)

        self.output_window = tk.Text(root, height=10, bg="#f0f0f0", font=("Consolas", 10))
        self.output_window.pack(fill=tk.X)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "r") as f:
                code = f.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, code)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".py",
                                                 filetypes=[("Python Files", "*.py")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))

    def run_code(self):
        code = self.text_area.get(1.0, tk.END)
        with open("temp_run.py", "w") as f:
            f.write(code)

        result = subprocess.run(["python", "temp_run.py"], capture_output=True, text=True)
        self.output_window.delete(1.0, tk.END)
        if result.stderr:
            self.output_window.insert(tk.END, "❌ Error:\n" + result.stderr)
        else:
            self.output_window.insert(tk.END, "✅ Output:\n" + result.stdout)

if __name__ == "__main__":
    root = tk.Tk()
    ide = PythonIDE(root)
    root.mainloop()
