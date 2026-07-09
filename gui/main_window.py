import customtkinter as ctk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Nametag Generator Pro")
        self.geometry("1300x750")

        self.build_ui()

    def build_ui(self):

        # ==========================
        # Toolbar
        # ==========================

        toolbar = ctk.CTkFrame(self, height=60)

        toolbar.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(
            toolbar,
            text="Template"
        ).pack(side="left", padx=10, pady=10)

        ctk.CTkButton(
            toolbar,
            text="Excel"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            toolbar,
            text="Font"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            toolbar,
            text="Generate"
        ).pack(side="right", padx=10)

        # ==========================
        # Preview
        # ==========================

        preview = ctk.CTkFrame(self)

        preview.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = ctk.CTkCanvas(
            preview,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            600,
            250,
            text="NAMETAG PREVIEW",
            font=("Arial", 30, "bold"),
            fill="gray"
        )