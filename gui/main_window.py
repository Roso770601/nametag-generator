import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Nametag Generator Pro")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        self.template_path = ""
        self.excel_path = ""
        self.font_path = ""

        self.preview_image = None
        self.original_image = None

        self.build_ui()

    # =====================================================

    def build_ui(self):

        # ---------------- Toolbar ----------------

        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar,
            text="📷 Pilih Template",
            command=self.open_template
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="📊 Pilih Excel",
            command=self.open_excel
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="🔤 Pilih Font",
            command=self.open_font
        ).pack(side="left", padx=5)

        # ---------------- Preview ----------------

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(
            self.preview_frame,
            bg="#DDDDDD",
            highlightthickness=1,
            highlightbackground="#888888"
        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            600,
            300,
            text="PILIH TEMPLATE",
            font=("Arial", 28, "bold"),
            fill="gray"
        )

        # ---------------- Status ----------------

        self.status = ttk.Label(
            self,
            text="Status : Siap",
            anchor="w"
        )

        self.status.pack(fill="x", side="bottom")

        # jika window di-resize, preview ikut menyesuaikan
        self.canvas.bind("<Configure>", self.on_canvas_resize)

    # =====================================================

    def on_canvas_resize(self, event):

        if self.original_image is not None:
            self.show_template()

    # =====================================================

    def show_template(self):

        if self.original_image is None:
            return

        image = self.original_image.copy()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 50:
            return

        if canvas_height < 50:
            return

        image.thumbnail(
            (canvas_width - 20, canvas_height - 20)
        )

        self.preview_image = ImageTk.PhotoImage(image)

        self.canvas.delete("all")

        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_image
        )

    # =====================================================

    def open_template(self):

        filename = filedialog.askopenfilename(
            title="Pilih Template",
            filetypes=[
                ("Image", "*.png *.jpg *.jpeg")
            ]
        )

        if filename:

            self.template_path = filename

            self.original_image = Image.open(filename)

            self.status.config(
                text=f"Template : {filename}"
            )

            self.show_template()

    # =====================================================

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

    # =====================================================

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