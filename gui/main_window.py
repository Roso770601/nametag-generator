import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
from gui.preview_canvas import PreviewCanvas


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Nametag Generator Pro")
        self.geometry("1200x750")
        self.minsize(1000, 650)

        # =============================
        # Data
        # =============================

        self.template_path = ""
        self.excel_path = ""
        self.font_path = ""

        self.preview_image = None
        self.original_image = None

        # Posisi sementara
        self.name_x = 500
        self.name_y = 320

        self.no_x = 500
        self.no_y = 380

        self.build_ui()

    # =========================================================

    def build_ui(self):

        toolbar = ttk.Frame(self, padding=10)
        toolbar.pack(fill="x")

        ttk.Button(
            toolbar,
            text="📷 Template",
            command=self.open_template
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="📊 Excel",
            command=self.open_excel
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="🔤 Font",
            command=self.open_font
        ).pack(side="left", padx=5)

        # =========================================

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.canvas = PreviewCanvas(
            self.preview_frame
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.status = ttk.Label(
            self,
            text="Status : Siap",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )

        
    # =========================================================

    def on_canvas_resize(self, event):

        if self.original_image is not None:
            self.draw_preview()

    # =========================================================

    def draw_preview(self):

        self.canvas.delete("all")

        if self.original_image is None:
            self.canvas.create_text(
                600,
                300,
                text="PILIH TEMPLATE",
                font=("Arial", 28, "bold"),
                fill="gray"
            )
            return

        image = self.original_image.copy()

        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()

        image.thumbnail(
            (cw - 20, ch - 20)
        )

        self.preview_image = ImageTk.PhotoImage(image)

        self.canvas.create_image(
            cw // 2,
            ch // 2,
            image=self.preview_image
        )

        # =============================
        # Hitung posisi tengah gambar
        # =============================

        img_w = image.width
        img_h = image.height

        left = (cw - img_w) // 2
        top = (ch - img_h) // 2

        # Simpan supaya nanti Sprint 4
        self.image_left = left
        self.image_top = top
        self.image_width = img_w
        self.image_height = img_h

        # =============================
        # Nama
        # =============================

        self.canvas.create_text(
            left + self.name_x,
            top + self.name_y,
            text="NAMA SISWA",
            font=("Arial", 34, "bold"),
            fill="black",
            tags="nama"
        )

        # =============================
        # No Absen
        # =============================

        self.canvas.create_text(
            left + self.no_x,
            top + self.no_y,
            text="NO. 01",
            font=("Arial", 28, "bold"),
            fill="blue",
            tags="absen"
        )

    # =========================================================

    def open_template(self):

        filename = filedialog.askopenfilename(
            title="Pilih Template",
            filetypes=[
                ("Image", "*.png *.jpg *.jpeg")
            ]
        )

        if filename:

            self.template_path = filename

            self.canvas.load_template(
                filename
            )

            self.status.config(
                text=f"Template : {filename}"
            )

            
    # =========================================================

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

    # =========================================================

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

    # =========================================================
    # Sprint 4 Preparation
    # =========================================================

    def refresh(self):
        self.canvas.draw()

    # =========================================================

    def reset_preview(self):

        self.canvas.name_x = 500
        self.canvas.name_y = 320

        self.canvas.no_x = 500
        self.canvas.no_y = 380

        self.canvas.draw()            