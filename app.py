import tkinter as tk
from gui.main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    root.title("App")

    app = MainWindow(root)
    app.pack(fill="both", expand=True)

    root.mainloop()