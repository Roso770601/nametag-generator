import json
import os
import tkinter as tk

from PIL import Image
from PIL import ImageTk


class PreviewCanvas(tk.Canvas):

    """
    Preview Canvas
    -----------------------
    Menampilkan template
    Drag object
    Resize font
    Edit text
    Simpan layout
    """

    def __init__(self, master, **kwargs):

        super().__init__(
            master,
            bg="#DDDDDD",
            highlightthickness=1,
            highlightbackground="#999999",
            **kwargs  # 🔥 INI KUNCINYA
        )
        self.scale_factor = 1.0
        self.bind("<MouseWheel>", self.on_mousewheel)

        # ==================================================
        # TEMPLATE
        # ==================================================

        self.original_image = None
        self.preview_image = None

        self.image_left = 0
        self.image_top = 0

        self.image_width = 0
        self.image_height = 0

        self.scale_x = 1.0
        self.scale_y = 1.0

        # ==================================================
        # TEXT
        # ==================================================

        self.name_text = "NAMA SISWA"
        self.no_text = "01"
        self.name_color = "black"
        self.absen_color = "blue"

        # ==================================================
        # POSISI
        # (koordinat gambar ASLI)
        # ==================================================

        self.name_x = 500
        self.name_y = 320

        self.no_x = 500
        self.no_y = 380

        # ==================================================
        # FONT
        # ==================================================

        self.name_font_size = 72
        self.absen_font_size = 56

        # ==================================================
        # ITEM
        # ==================================================

        self.name_item = None
        self.no_item = None

        # ==================================================
        # SELECT
        # ==================================================

        self.selected_object = None

        # ==================================================
        # DRAG
        # ==================================================

        self.drag_item = None

        self.start_x = 0
        self.start_y = 0

        # ==================================================
        # EDIT
        # ==================================================

        self.edit_entry = None

        # ==================================================
        # EVENT
        # ==================================================

        self.bind(
            "<Configure>",
            self.on_resize
        )

        self.bind_all(
            "<MouseWheel>",
            self.change_font_size
        )

        self.load_layout()

        self.enable_drag()
        self.enable_edit()
        
    from PIL import Image, ImageTk
    
    def on_mousewheel(self, event):
        # ZOOM kalau CTRL ditekan
        if event.state & 0x0004:
            if event.delta > 0:
                self.zoom(1.1, event)
            else:
                self.zoom(0.9, event)
        else:
            # SCROLL NORMAL
            self.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
    def zoom(self, factor, event):
        self.scale_factor *= factor

        # zoom ke arah cursor
        self.draw()

    def load_image(self, path):

        image = Image.open(path)

        # 🔥 ambil ukuran canvas
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        # kalau canvas belum ready → skip resize
        if canvas_width < 10 or canvas_height < 10:
            canvas_width = 800
            canvas_height = 500

        # 🔥 RESIZE PROPORSIONAL
        new_w = int(self.original_image.width * self.scale_factor)
        new_h = int(self.original_image.height * self.scale_factor)
        image = image.resize((new_w, new_h))

        self.preview_image = ImageTk.PhotoImage(image)

        self.delete("all")

        self.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_image,
            anchor="center"
        )

    # ==================================================
    # TEMPLATE
    # ==================================================

    def load_template(self, filename):

        self.original_image = Image.open(filename)

        self.draw()

    # ==================================================

    def on_resize(self, event):

        if self.original_image:
            self.draw()
       # ==================================================
    # DRAW
    # ==================================================

    def draw(self):

        self.delete("all")

        if self.original_image is None:

            self.create_text(
                self.winfo_width() // 2,
                self.winfo_height() // 2,
                text="PILIH TEMPLATE",
                font=("Arial", 28, "bold"),
                fill="gray"
            )

            return

        image = self.original_image.copy()

        canvas_width = max(self.winfo_width(), 20)
        canvas_height = max(self.winfo_height(), 20)

        new_w = int(self.original_image.width * self.scale_factor)
        new_h = int(self.original_image.height * self.scale_factor)
        image = image.resize((new_w, new_h))

        self.preview_image = ImageTk.PhotoImage(image)

        self.image_width = image.width
        self.image_height = image.height

        self.scale_x = (
            self.image_width /
            self.original_image.width
        )

        self.scale_y = (
            self.image_height /
            self.original_image.height
        )

        self.image_left = (
            canvas_width - self.image_width
        ) // 2

        self.image_top = (
            canvas_height - self.image_height
        ) // 2

        self.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_image
        )

        self.draw_name()
        self.draw_absen()
        
        self.enable_drag()

    # ==================================================
    # DRAW NAME
    # ==================================================

    def draw_name(self):

        x = self.image_left + (self.name_x * self.scale_x)
        y = self.image_top + (self.name_y * self.scale_y)

        preview_size = max(
            int(self.name_font_size * self.scale_y),
            8
        )

        color = self.name_color

        self.name_item = self.create_text(
            x,
            y,
            text=self.name_text,
            font=(
                "Arial",
                preview_size,
                "bold"
            ),
            fill=color,
            tags=("nama",)
        )

    # ==================================================
    # DRAW ABSEN
    # ==================================================

    def draw_absen(self):

        x = self.image_left + (self.no_x * self.scale_x)
        y = self.image_top + (self.no_y * self.scale_y)

        preview_size = max(
            int(self.absen_font_size * self.scale_y),
            8
        )

        color = self.absen_color

        self.no_item = self.create_text(
            x,
            y,
            text=self.no_text,
            font=(
                "Arial",
                preview_size,
                "bold"
            ),
            fill=color,
            tags=("absen",)
        )
        # ==================================================
    # DRAG SYSTEM
    # ==================================================

    def enable_drag(self):

        for tag in ("nama", "absen"):

            self.tag_bind(
                tag,
                "<ButtonPress-1>",
                self.start_drag
            )

            self.tag_bind(
                tag,
                "<B1-Motion>",
                self.drag
            )

            self.tag_bind(
                tag,
                "<ButtonRelease-1>",
                self.stop_drag
            )

    # ==================================================

    def start_drag(self, event):

       print("START DRAG")

       item = self.find_withtag("current")

       print(item)

       if not item:
        return

       self.drag_item = item[0]

       tags = self.gettags(self.drag_item)

       print(tags)

       if "nama" in tags:
        self.selected_object = "nama"

       elif "absen" in tags:
        self.selected_object = "absen"

       self.start_x = event.x
       self.start_y = event.y



    # ==================================================

    def drag(self, event):

        if self.drag_item is None:
            return

        dx = event.x - self.start_x
        dy = event.y - self.start_y

        self.move(
            self.drag_item,
            dx,
            dy
        )

        self.start_x = event.x
        self.start_y = event.y

    # ==================================================

    def stop_drag(self, event):

        if self.drag_item is None:
            return

        coords = self.coords(self.drag_item)

        preview_x = coords[0] - self.image_left
        preview_y = coords[1] - self.image_top

        original_x = preview_x / self.scale_x
        original_y = preview_y / self.scale_y

        tags = self.gettags(self.drag_item)

        if "nama" in tags:

            self.name_x = original_x
            self.name_y = original_y

        elif "absen" in tags:

            self.no_x = original_x
            self.no_y = original_y

        self.drag_item = None

        self.save_layout()

        self.draw()
        
    # ==================================================
    # FONT SIZE
    # ==================================================

    def change_font_size(self, event):

        if self.selected_object is None:
            return

        delta = 2 if event.delta > 0 else -2

        if self.selected_object == "nama":

            self.name_font_size = max(
                8,
                self.name_font_size + delta
            )

        elif self.selected_object == "absen":

            self.absen_font_size = max(
                8,
                self.absen_font_size + delta
            )

        self.save_layout()
        self.draw()

    # ==================================================
    # SAVE LAYOUT
    # ==================================================

    def save_layout(self):

        layout = {

            "nama":{

                "x":self.name_x,
                "y":self.name_y,
                "font_size":self.name_font_size

            },

            "absen":{

                "x":self.no_x,
                "y":self.no_y,
                "font_size":self.absen_font_size

            }

        }

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            "data/layout.json",
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                layout,
                file,
                indent=4
            )

    # ==================================================
    # LOAD LAYOUT
    # ==================================================

    def load_layout(self):

        filename = "data/layout.json"

        if not os.path.exists(filename):
            return

        with open(
            filename,
            "r",
            encoding="utf-8"
        ) as file:

            layout = json.load(file)

        if "nama" in layout:

            self.name_x = layout["nama"].get("x",500)
            self.name_y = layout["nama"].get("y",320)
            self.name_font_size = layout["nama"].get(
                "font_size",
                72
            )

        if "absen" in layout:

            self.no_x = layout["absen"].get("x",500)
            self.no_y = layout["absen"].get("y",380)
            self.absen_font_size = layout["absen"].get(
                "font_size",
                56
            )

    # ==================================================
    # RESET
    # ==================================================

    def reset_layout(self):

        self.name_x = 500
        self.name_y = 320

        self.no_x = 500
        self.no_y = 380

        self.name_font_size = 72
        self.absen_font_size = 56

        self.save_layout()
        self.draw()

    # ==================================================
    # DUMMY EDIT
    # (sementara agar MainWindow tidak error)
    # ==================================================

    def enable_edit(self):
        pass

    # ==================================================

    def get_layout(self):

        return {

            "nama":{

                "x":self.name_x,
                "y":self.name_y,
                "font_size":self.name_font_size

            },

            "absen":{

                "x":self.no_x,
                "y":self.no_y,
                "font_size":self.absen_font_size

            }

        }
        # ======================================================
    # TEXT EDITOR
    # ======================================================

    def enable_edit(self):

        self.tag_bind(
            "nama",
            "<Double-Button-1>",
            self.edit_name
        )

        self.tag_bind(
            "absen",
            "<Double-Button-1>",
            self.edit_absen
        )

    # ======================================================

    def create_editor(self, x, y, value, target):

        if self.edit_entry:
            self.edit_entry.destroy()

        self.edit_entry = tk.Entry(
            self.master,
            font=("Arial", 20)
        )

        self.edit_entry.insert(
            0,
            value
        )

        self.edit_entry.place(
            x=x,
            y=y
        )

        self.edit_entry.focus()

        self.edit_entry.bind(
            "<Return>",
            lambda e: self.save_text(target)
        )

        self.edit_entry.bind(
            "<Escape>",
            lambda e: self.cancel_edit()
        )

    # ======================================================

    def edit_name(self, event):

        self.create_editor(
            event.x,
            event.y,
            self.name_text,
            "nama"
        )

    # ======================================================

    def edit_absen(self, event):

        self.create_editor(
            event.x,
            event.y,
            self.no_text,
            "absen"
        )

    # ======================================================

    def save_text(self, target):

        if self.edit_entry is None:
            return

        value = self.edit_entry.get().strip()

        if target == "nama":
            self.name_text = value

        elif target == "absen":
            self.no_text = value

        self.edit_entry.destroy()
        self.edit_entry = None

        self.draw()

    # ======================================================

    def cancel_edit(self):

        if self.edit_entry:

            self.edit_entry.destroy()
            self.edit_entry = None
            
    def get_layout(self):

        return {

        "nama":{

            "x":self.name_x,
            "y":self.name_y

        },

        "absen":{

            "x":self.no_x,
            "y":self.no_y

        }

    }