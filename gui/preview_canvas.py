import tkinter as tk
import json
import os

from PIL import Image, ImageTk


class PreviewCanvas(tk.Canvas):

    def __init__(self, master):

        super().__init__(
            master,
            bg="#DDDDDD",
            highlightthickness=1,
            highlightbackground="#999999"
        )

        # ==========================
        # Template
        # ==========================

        self.original_image = None
        self.preview_image = None

        self.image_left = 0
        self.image_top = 0

        self.image_width = 0
        self.image_height = 0


        # ==========================
        # Posisi Nama
        # ==========================

        self.name_x = 500
        self.name_y = 320

        self.name_item = None


        # ==========================
        # Posisi No Absen
        # ==========================

        self.no_x = 500
        self.no_y = 380

        self.no_item = None


        # ==========================
        # Drag
        # ==========================

        self.drag_item = None

        self.start_x = 0
        self.start_y = 0

        # ==========================
        # Text Editor
        # ==========================

        self.name_text = "NAMA SISWA"
        self.no_text = "NO. 01"

        self.edit_entry = None


        # ==========================
        # Event Resize
        # ==========================

        self.bind(
            "<Configure>",
            self.on_resize
        )


        # ==========================
        # Aktifkan Drag
        # ==========================

        self.enable_drag()
        self.enable_edit()
        
        self.load_layout()


    # ======================================================

    def load_template(self, filename):

        self.original_image = Image.open(filename)

        self.draw()


    # ======================================================

    def on_resize(self, event):

        if self.original_image:

            self.draw()


    # ======================================================

    def draw(self):

        self.delete("all")


        if self.original_image is None:

            self.create_text(
                self.winfo_width() // 2,
                self.winfo_height() // 2,
                text="PILIH TEMPLATE",
                font=("Arial",28,"bold"),
                fill="gray"
            )

            return


        image = self.original_image.copy()


        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()


        image.thumbnail(
            (
                canvas_width - 20,
                canvas_height - 20
            )
        )


        self.preview_image = ImageTk.PhotoImage(
            image
        )


        self.image_width = image.width
        self.image_height = image.height


        self.image_left = (
            canvas_width - self.image_width
        ) // 2


        self.image_top = (
            canvas_height - self.image_height
        ) // 2



        self.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.preview_image,
            anchor="center"
        )


        self.draw_name()
        self.draw_absen()



    # ======================================================

    def draw_name(self):

        self.name_item = self.create_text(

        self.image_left + self.name_x,
        self.image_top + self.name_y,

        text=self.name_text,

            font=(
                "Arial",
                34,
                "bold"
            ),

            fill="black",

            tags=("nama",)

        )



        # ======================================================

    def draw_name(self):

        self.name_item = self.create_text(

            self.image_left + self.name_x,
            self.image_top + self.name_y,

            text=self.name_text,

            font=(
                "Arial",
                34,
                "bold"
            ),

            fill="black",

            tags=("nama",)

        )


    # ======================================================

    def draw_absen(self):

        self.no_item = self.create_text(

            self.image_left + self.no_x,
            self.image_top + self.no_y,

            text=self.no_text,

            font=(
                "Arial",
                28,
                "bold"
            ),

            fill="blue",

            tags=("absen",)

        )


    # ======================================================
    # DRAG SYSTEM
    # ======================================================


    def enable_drag(self):

        for tag in ("nama","absen"):

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



    # ======================================================


    def start_drag(self,event):

        self.drag_item = self.find_closest(
            event.x,
            event.y
        )


        self.start_x = event.x
        self.start_y = event.y


        print(
            "DRAG:",
            self.drag_item
        )



    # ======================================================


    def drag(self,event):

        if not self.drag_item:

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



    # ======================================================


    def stop_drag(self, event):

        if self.drag_item:

            coords = self.coords(self.drag_item)

            x = coords[0] - self.image_left
            y = coords[1] - self.image_top

            tags = self.gettags(self.drag_item)

            if "nama" in tags:

                self.name_x = x
                self.name_y = y

                print(
                    "POSISI NAMA:",
                    self.name_x,
                    self.name_y
                )

            elif "absen" in tags:

                self.no_x = x
                self.no_y = y

                print(
                    "POSISI ABSEN:",
                    self.no_x,
                    self.no_y
                )
                self.save_layout()
            self.drag_item = None
    # ======================================================
    # SAVE LAYOUT
    # ======================================================

    def save_layout(self):

        layout = {

            "nama": {
                "x": self.name_x,
                "y": self.name_y
            },

            "absen": {
                "x": self.no_x,
                "y": self.no_y
            }

        }


        os.makedirs(
            "data",
            exist_ok=True
        )


        with open(
            "data/layout.json",
            "w"
        ) as file:

            json.dump(
                layout,
                file,
                indent=4
            )


        print(
            "LAYOUT TERSIMPAN"
        )
        
        
    # ======================================================
    # LOAD LAYOUT
    # ======================================================

    def load_layout(self):

        filename = "data/layout.json"


        if not os.path.exists(filename):

            return


        with open(
            filename,
            "r"
        ) as file:

            layout = json.load(file)


        if "nama" in layout:

            self.name_x = layout["nama"]["x"]
            self.name_y = layout["nama"]["y"]


        if "absen" in layout:

            self.no_x = layout["absen"]["x"]
            self.no_y = layout["absen"]["y"]


        print(
            "LAYOUT DIMUAT"
        )
        
    # ======================================================
    # RESET LAYOUT
    # ======================================================

    def reset_layout(self):

        self.name_x = 500
        self.name_y = 320

        self.no_x = 500
        self.no_y = 380


        self.save_layout()

        self.draw()


        print(
            "LAYOUT RESET"
        )
        
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
            font=("Arial",20)
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


    # ======================================================

    def edit_name(self,event):

        self.create_editor(
            event.x,
            event.y,
            self.name_text,
            "nama"
        )


    # ======================================================

    def edit_absen(self,event):

        self.create_editor(
            event.x,
            event.y,
            self.no_text,
            "absen"
        )


    # ======================================================

    def save_text(self,target):

        value = self.edit_entry.get()


        if target == "nama":

            self.name_text = value


        if target == "absen":

            self.no_text = value


        self.edit_entry.destroy()

        self.edit_entry = None


        self.draw()