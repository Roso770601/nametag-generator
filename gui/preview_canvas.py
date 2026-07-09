import tkinter as tk
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

            text="NAMA SISWA",

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

            text="NO. 01",

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


    def stop_drag(self,event):

        self.drag_item = None