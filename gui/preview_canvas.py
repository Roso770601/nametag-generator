import json
import os
import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class PreviewCanvas(tk.Canvas):

    def __init__(self, master):

        super().__init__(master, bg="#DDDDDD")

        # ================= FONT =================
        self.font_path = os.path.join(BASE_DIR, "fonts", "Poppins-Bold.ttf")

        # ================= IMAGE =================
        self.original_image = None
        self.preview_image = None

        self.image_left = 0
        self.image_top = 0
        self.image_width = 0
        self.image_height = 0

        self.scale_x = 1.0
        self.scale_y = 1.0

        # ================= TEXT =================
        self.name_text = "NAMA SISWA"
        self.no_text = "NO. 01"

        # ================= POSITION =================
        self.name_x = 500
        self.name_y = 320

        self.no_x = 500
        self.no_y = 380

        # ================= FONT SIZE =================
        self.name_font_size = 72
        self.absen_font_size = 56

        # ================= STATE =================
        self.drag_target = None
        self.offset_x = 0
        self.offset_y = 0
        self.selected_object = None

        self.edit_entry = None

        # ================= EVENT =================
        self.bind("<Configure>", self.on_resize)
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind_all("<MouseWheel>", self.change_font_size)
        self.bind("<Double-Button-1>", self.on_double_click)

        self.load_layout()

    # ================= TEMPLATE =================
    def load_template(self, filename):
        self.original_image = Image.open(filename)
        self.draw()

    def on_resize(self, event):
        if self.original_image:
            self.draw()

    # ================= DRAW =================
    def draw(self):

        self.delete("all")

        if not self.original_image:
            return

        image = self.original_image.copy()
        draw = ImageDraw.Draw(image)

        name_font = ImageFont.truetype(self.font_path, int(self.name_font_size))
        absen_font = ImageFont.truetype(self.font_path, int(self.absen_font_size))

        draw.text((self.name_x, self.name_y), self.name_text, fill="black", font=name_font, anchor="mm")
        draw.text((self.no_x, self.no_y), self.no_text, fill="black", font=absen_font, anchor="mm")

        canvas_w = max(self.winfo_width(), 20)
        canvas_h = max(self.winfo_height(), 20)

        image.thumbnail((canvas_w - 20, canvas_h - 20))

        self.preview_image = ImageTk.PhotoImage(image)

        self.image_width = image.width
        self.image_height = image.height

        self.scale_x = self.image_width / self.original_image.width
        self.scale_y = self.image_height / self.original_image.height

        self.image_left = (canvas_w - self.image_width) // 2
        self.image_top = (canvas_h - self.image_height) // 2

        self.create_image(canvas_w // 2, canvas_h // 2, image=self.preview_image)

        # 🔥 highlight
        self.draw_selection_box()

    # ================= CLICK =================
    def on_click(self, event):

        if not self.original_image:
            return

        x = (event.x - self.image_left) / self.scale_x
        y = (event.y - self.image_top) / self.scale_y

        if abs(x - self.name_x) < 120 and abs(y - self.name_y) < 60:
            self.drag_target = "name"
            self.selected_object = "nama"
            self.offset_x = self.name_x - x
            self.offset_y = self.name_y - y

        elif abs(x - self.no_x) < 120 and abs(y - self.no_y) < 60:
            self.drag_target = "no"
            self.selected_object = "absen"
            self.offset_x = self.no_x - x
            self.offset_y = self.no_y - y

        else:
            self.drag_target = None
            self.selected_object = None

        self.draw()

    # ================= DRAG =================
    def on_drag(self, event):

        if self.drag_target is None:
            return

        x = (event.x - self.image_left) / self.scale_x
        y = (event.y - self.image_top) / self.scale_y

        if self.drag_target == "name":
            self.name_x = x + self.offset_x
            self.name_y = y + self.offset_y

        elif self.drag_target == "no":
            self.no_x = x + self.offset_x
            self.no_y = y + self.offset_y

        self.draw()

    # ================= SCROLL =================
    def change_font_size(self, event):

        if self.selected_object is None:
            return

        delta = 4 if event.delta > 0 else -4

        if self.selected_object == "nama":
            self.name_font_size = max(8, self.name_font_size + delta)

        elif self.selected_object == "absen":
            self.absen_font_size = max(8, self.absen_font_size + delta)

        self.save_layout()
        self.draw()

    # ================= DOUBLE CLICK EDIT =================
    def on_double_click(self, event):

        if self.selected_object is None:
            return

        if self.edit_entry:
            self.edit_entry.destroy()

        self.edit_entry = tk.Entry(self.master, font=("Arial", 18))
        self.edit_entry.place(x=event.x, y=event.y)

        if self.selected_object == "nama":
            self.edit_entry.insert(0, self.name_text)
        else:
            self.edit_entry.insert(0, self.no_text)

        self.edit_entry.focus()

        self.edit_entry.bind("<Return>", self.save_text)
        self.edit_entry.bind("<Escape>", lambda e: self.edit_entry.destroy())

    def save_text(self, event):

        value = self.edit_entry.get().strip()

        if self.selected_object == "nama":
            self.name_text = value
        else:
            self.no_text = value

        self.edit_entry.destroy()
        self.edit_entry = None

        self.draw()

    # ================= SELECTION BOX =================
    def draw_selection_box(self):

        if not self.selected_object:
            return

        if self.selected_object == "nama":
            x = self.name_x
            y = self.name_y
        else:
            x = self.no_x
            y = self.no_y

        # convert ke canvas
        cx = self.image_left + x * self.scale_x
        cy = self.image_top + y * self.scale_y

        self.create_rectangle(
            cx - 80, cy - 40,
            cx + 80, cy + 40,
            outline="red",
            width=2
        )

    # ================= RESET =================
    def reset_layout(self):

        if self.original_image:
            self.name_x = self.original_image.width // 2
            self.name_y = int(self.original_image.height * 0.6)

            self.no_x = self.original_image.width // 2
            self.no_y = int(self.original_image.height * 0.7)

        self.name_font_size = 72
        self.absen_font_size = 56

        self.save_layout()
        self.draw()

    # ================= SAVE =================
    def save_layout(self):

        os.makedirs("data", exist_ok=True)

        layout = {
            "nama": {
                "x": self.name_x,
                "y": self.name_y,
                "font_size": self.name_font_size
            },
            "absen": {
                "x": self.no_x,
                "y": self.no_y,
                "font_size": self.absen_font_size
            }
        }

        with open("data/layout.json", "w", encoding="utf-8") as f:
            json.dump(layout, f, indent=4)

    # ================= LOAD =================
    def load_layout(self):

        if not os.path.exists("data/layout.json"):
            return

        with open("data/layout.json", "r", encoding="utf-8") as f:
            layout = json.load(f)

        self.name_x = layout.get("nama", {}).get("x", 500)
        self.name_y = layout.get("nama", {}).get("y", 320)
        self.name_font_size = layout.get("nama", {}).get("font_size", 72)

        self.no_x = layout.get("absen", {}).get("x", 500)
        self.no_y = layout.get("absen", {}).get("y", 380)
        self.absen_font_size = layout.get("absen", {}).get("font_size", 56)
    def get_layout(self):
        return {
            "nama": {
                "x": self.name_x,
                "y": self.name_y,
                "font_size": self.name_font_size
            },
            "absen": {
                "x": self.no_x,
                "y": self.no_y,
                "font_size": self.absen_font_size
            },
            "font_path": self.font_path
        }