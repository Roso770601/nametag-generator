import tkinter as tk
from tkinter import ttk, filedialog


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Nametag Generator Pro")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.template_path = ""
        self.excel_path = ""
        self.font_path = ""

        self.build_ui()

    def build_ui(self):

        # ==========================
        # Toolbar
        # ==========================

        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar,
            text="Pilih Template",
            command=self.open_template
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Pilih Excel",
            command=self.open_excel
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Pilih Font",
            command=self.open_font
        ).pack(side="left", padx=5)

        # ==========================
        # Preview Area
        # ==========================

        preview_frame = ttk.Frame(self, padding=10)
        preview_frame.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(
            preview_frame,
            bg="#e8e8e8",
            highlightthickness=1,
            highlightbackground="#999999"
        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            600,
            300,
            text="PREVIEW TEMPLATE",
            font=("Arial", 28, "bold"),
            fill="gray"
        )

        # ==========================
        # Status Bar
        # ==========================

        self.status = ttk.Label(
            self,
            text="Status : Siap",
            anchor="w"
        )

        self.status.pack(fill="x", side="bottom")

    # ==========================
    # Event
    # ==========================

    def open_template(self):

        filename = filedialog.askopenfilename(
            title="Pilih Template",
            filetypes=[
                ("Image", "*.png *.jpg *.jpeg")
            ]
        )

        if filename:
            self.template_path = filename
            self.status.config(
                text=f"Template : {filename}"
            )

    def open_excel(self):

        filename = filedialog.askopenfilename(
            title="Pilih Excel",
            filetypes=[
                ("Excel", "*.xlsx")
            ]
        )

        if filename:
            self.excel_path = filename
            self.status.config(
                text=f"Excel : {filename}"
            )

    def open_font(self):

        filename = filedialog.askopenfilename(
            title="Pilih Font",
            filetypes=[
                ("Font", "*.ttf")
            ]
        )

        if filename:
            self.font_path = filename
            self.status.config(
                text=f"Font : {filename}"
            )