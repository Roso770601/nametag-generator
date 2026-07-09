import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

# ==========================
# Konfigurasi Tampilan
# ==========================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class NametagGenerator(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Nametag Generator Pro")
        self.geometry("1200x700")
        self.resizable(False, False)

        self.template_path = ""
        self.excel_path = ""
        self.font_path = ""

        self.create_widgets()

    def create_widgets(self):

        # =============================
        # PANEL KIRI
        # =============================

        left = ctk.CTkFrame(self, width=300)
        left.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(
            left,
            text="NAMETAG GENERATOR",
            font=("Arial",20,"bold")
        ).pack(pady=20)

        # TEMPLATE

        ctk.CTkButton(
            left,
            text="Pilih Template",
            command=self.open_template
        ).pack(fill="x", padx=20, pady=10)

        self.template_label = ctk.CTkLabel(
            left,
            text="Belum dipilih"
        )

        self.template_label.pack()

        # EXCEL

        ctk.CTkButton(
            left,
            text="Pilih Excel",
            command=self.open_excel
        ).pack(fill="x", padx=20, pady=10)

        self.excel_label = ctk.CTkLabel(
            left,
            text="Belum dipilih"
        )

        self.excel_label.pack()

        # FONT

        ctk.CTkButton(
            left,
            text="Pilih Font",
            command=self.open_font
        ).pack(fill="x", padx=20, pady=10)

        self.font_label = ctk.CTkLabel(
            left,
            text="Belum dipilih"
        )

        self.font_label.pack()

        # GENERATE

        ctk.CTkButton(
            left,
            text="Generate",
            height=45,
            command=self.generate
        ).pack(fill="x", padx=20, pady=40)

        # =============================
        # PANEL KANAN
        # =============================

        right = ctk.CTkFrame(self)
        right.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            right,
            text="PREVIEW",
            font=("Arial",18,"bold")
        ).pack(pady=10)

        self.canvas = ctk.CTkCanvas(
            right,
            width=800,
            height=600,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack()

    # =================================

    def open_template(self):

        path = filedialog.askopenfilename(
            filetypes=[("PNG","*.png"),("JPG","*.jpg")]
        )

        if path:

            self.template_path = path

            self.template_label.configure(text=path.split("/")[-1])

            self.show_preview()

    # =================================

    def open_excel(self):

        path = filedialog.askopenfilename(
            filetypes=[("Excel","*.xlsx")]
        )

        if path:

            self.excel_path = path

            self.excel_label.configure(text=path.split("/")[-1])

    # =================================

    def open_font(self):

        path = filedialog.askopenfilename(
            filetypes=[("Font","*.ttf")]
        )

        if path:

            self.font_path = path

            self.font_label.configure(text=path.split("/")[-1])

    # =================================

    def show_preview(self):

        img = Image.open(self.template_path)

        img.thumbnail((800,600))

        self.preview = ImageTk.PhotoImage(img)

        self.canvas.delete("all")

        self.canvas.create_image(
            400,
            300,
            image=self.preview
        )

        self.canvas.create_text(
            420,
            360,
            text="AHMAD FAUZI",
            font=("Arial",24,"bold"),
            fill="navy",
            tags="nama"
        )

        self.canvas.create_text(
            420,
            430,
            text="12",
            font=("Arial",24,"bold"),
            fill="navy",
            tags="absen"
        )

    # =================================

    def generate(self):

        print("Generate nanti kita sambungkan ke generator.py")


app = NametagGenerator()

app.mainloop()