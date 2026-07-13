def show_template(self):
    from PIL import Image, ImageTk

    if not self.template_path:
        return

    image = Image.open(self.template_path)

    self.original_image = image.copy()

    # ukuran canvas
    self.update_idletasks()

    canvas_width = self.canvas.winfo_width()
    canvas_height = self.canvas.winfo_height()

    # ukuran awal jika canvas belum dihitung
    if canvas_width <= 1:
        canvas_width = 1000

    if canvas_height <= 1:
        canvas_height = 600

    image.thumbnail((canvas_width - 20, canvas_height - 20))

    self.preview_image = ImageTk.PhotoImage(image)

    self.canvas.delete("all")

    self.canvas.create_image(
        canvas_width // 2,
        canvas_height // 2,
        image=self.preview_image
    )
def __init__(self):
    super().__init__()

    self.title("Nametag Generator Pro")
    self.geometry("1200x750")
    self.minsize(1000, 650)

    self.template_path = ""
    self.excel_path = ""
    self.font_path = ""

    # Tambahan Sprint 2
    self.preview_image = None
    self.original_image = None

    self.build_ui()