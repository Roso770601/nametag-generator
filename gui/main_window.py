import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image
from pymupdf import name
from gui.preview_canvas import PreviewCanvas
import openpyxl
from core.exporter import NameTagExporter
from tkinter import colorchooser

import tkinter as tk

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master.title("Nametag Generator Pro")
        self.master.geometry("1200x750")
        self.master.minsize(1000, 650)

        # =============================
        # Data
        # =============================

        self.template_path = ""
        self.excel_path = ""
        self.font_path = ""
        
        self.students = []
        
        self.selected_index = None
        
        self.exporter = NameTagExporter()

        self.preview_image = None
        self.original_image = None

        self.build_ui()
        self.preview_index = 0
        
    def show_preview(self):

        if not self.students:
            return

        student = self.students[self.preview_index]

        name = student["nama"]
        absen = str(student["absen"])

        print("PREVIEW:", name, absen)

        # pakai fungsi export tapi simpan ke sementara
        temp_path = "temp_preview.png"

        layout = self.canvas.get_layout()

        self.exporter.export(
            template_path=self.template_path,
            output_path=temp_path,

            name=name,
            absen=absen,

            name_x=layout["nama"]["x"],
            name_y=layout["nama"]["y"],

            absen_x=layout["absen"]["x"],
            absen_y=layout["absen"]["y"],

            font_path=self.font_path,

            name_font_size=self.canvas.name_font_size,
            absen_font_size=self.canvas.absen_font_size,
            name_color=self.canvas.name_color,
            absen_color=self.canvas.absen_color,
        )

        # tampilkan ke canvas
        self.canvas.load_image(temp_path)
        
    def choose_color(self):
        from tkinter import colorchooser

        color = colorchooser.askcolor()[1]

        if not color:
            return

        print("WARNA DIPILIH:", color)

        if self.canvas.selected_object == "nama":
            self.canvas.name_color = color

        elif self.canvas.selected_object == "absen":
            self.canvas.absen_color = color

        else:
            print("Pilih teks dulu (klik nama / absen)")
            return
        
        # self.canvas.selected_object = None

        self.canvas.draw()

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
        
        ttk.Button(
            toolbar,
            text="🧪 Test Export",
            command=self.test_export
        ).pack(side="left", padx=5)
        
        ttk.Button(
            toolbar,
            text="Warna",
            command=self.choose_color
        ).pack(side="left", padx=5)
        
               
        ttk.Button(
            toolbar,
            text="⬅ Prev",
            command=self.prev_preview
        ).pack(side="left", padx=5)

        ttk.Button(
            toolbar,
            text="Next ➡",
            command=self.next_preview
        ).pack(side="left", padx=5)
        
       
               
        # =========================================

        self.preview_frame = ttk.Frame(self)
        self.preview_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # WRAPPER (INI KUNCI)
        wrapper = ttk.Frame(self.preview_frame)
        wrapper.pack(fill="both", expand=True)

        # Scrollbar
        self.v_scroll = ttk.Scrollbar(wrapper, orient="vertical")
        self.v_scroll.pack(side="right", fill="y")

        self.h_scroll = ttk.Scrollbar(wrapper, orient="horizontal")
        self.h_scroll.pack(side="bottom", fill="x")

        # Canvas
        self.canvas = PreviewCanvas(
            wrapper,
            yscrollcommand=self.v_scroll.set,
            xscrollcommand=self.h_scroll.set
        )

        self.canvas.pack(fill="both", expand=True)

        # Connect
        self.v_scroll.config(command=self.canvas.yview)
        self.h_scroll.config(command=self.canvas.xview)

        # Scroll area
        self.canvas.config(scrollregion=(0, 0, 2000, 2000))

        self.canvas.pack(
            fill="both",
            expand=True
        )
        
        ttk.Button(
            toolbar,
            text="💾 Simpan Layout",
            command=self.canvas.save_layout
        ).pack(side="left", padx=5)
        
        ttk.Button(
            toolbar,
            text="🔄 Reset Layout",
            command=self.canvas.reset_layout
        ).pack(side="left", padx=5)
        
        ttk.Button(
            toolbar,
            text="🚀 Generate Semua",
            command=self.generate_all
        ).pack(side="left", padx=5)

        self.status = ttk.Label(
            self,
            text="Status : Siap",
            anchor="w"
        )

        self.status.pack(
            fill="x",
            side="bottom"
        )
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
            
    def next_preview(self):

        if not self.students:
            return

        self.preview_index += 1

        if self.preview_index >= len(self.students):
            self.preview_index = 0

        self.show_preview()


    def prev_preview(self):

        if not self.students:
            return

        self.preview_index -= 1

        if self.preview_index < 0:
            self.preview_index = len(self.students) - 1

        self.show_preview()

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
            self.load_excel(filename)
            
            self.update_student_preview()

            self.status.config(
                text=f"Siswa : {len(self.students)} data"
            )

    # =========================================================
    def load_excel(self, filename):
        self.students = []
        workbook = openpyxl.load_workbook(
            filename
        )


        sheet = workbook.active


        for row in sheet.iter_rows(
            min_row=2,
            values_only=True
        ):

            nama = row[0]
            absen = row[1]


            if nama:

                self.students.append(
                    {
                        "nama": str(nama),
                        "absen": str(absen)
                    }
                )


        print(
            "DATA SISWA:",
            self.students
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
            self.test_export()

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

        self.canvas.reset_layout()
        
    # =========================================================
    # UPDATE DATA SISWA KE CANVAS
    # =========================================================

    def update_student_preview(self):

        if not self.students:
            return


        student = self.students[0]


        self.canvas.name_text = student["nama"]
        self.canvas.no_text = student["absen"]

        self.canvas.draw()


        print(
            "PREVIEW UPDATE:",
            self.canvas.name_text,
            self.canvas.no_text
        )
        
        print("CANVAS COLOR:", self.canvas.name_color, self.canvas.absen_color)
    def test_export(self):

        print(">>> TEST EXPORT DIKLIK <<<")

        if not self.template_path:
            print("Template belum dipilih")
            return

        if not self.font_path:
            print("Font belum dipilih")
            self.status.config(
                text="Pilih font dahulu."
            )
            return
        print("=== TEST EXPORT ===")
        print("CANVAS NAME :", self.canvas.name_text)
        print("CANVAS ABSEN :", self.canvas.no_text)
        print("STUDENTS :", len(self.students))
        layout = self.canvas.get_layout()
        
        self.exporter.export(
            template_path=self.template_path,
            output_path="Output/test.png",

            name=self.canvas.name_text,
            absen=self.canvas.no_text,

            name_x=layout["nama"]["x"],
            name_y=layout["nama"]["y"],

            absen_x=layout["absen"]["x"],
            absen_y=layout["absen"]["y"],

            font_path=self.font_path,

            name_font_size=self.canvas.name_font_size,
            absen_font_size=self.canvas.absen_font_size,
            
            name_color=self.canvas.name_color,   # ✅ penting
            absen_color=self.canvas.absen_color, # ✅ penting
        )

        self.status.config(
            text="Export selesai."
        )
        print("=== EXPORT SELESAI ===")
        
    def update_name_live(self, event):

        # kalau belum pilih siswa → stop
        if self.selected_index is None:
            return

        edited_name = self.name_entry.get()

        # 🔥 UPDATE DATA UTAMA
        self.students[self.selected_index]["nama"] = edited_name

        # 🔥 UPDATE PREVIEW
        self.canvas.name_text = edited_name
        self.canvas.draw()

        print("UPDATE:", self.students[self.selected_index])
        
    def generate_all(self):

        if not self.template_path:
            print("Template belum dipilih")
            return

        if not self.font_path:
            print("Font belum dipilih")
            self.status.config(
                text="Pilih font dahulu."
            )
            return

        if not self.students:
            print("Data siswa kosong")
            self.status.config(
                text="Data siswa kosong."
            )
            return

        layout = self.canvas.get_layout()
        print("WARNA CANVAS (SEBELUM LOOP):", self.canvas.name_color, self.canvas.absen_color)

        for student in self.students:

            name = student["nama"] 
            absen = str(student["absen"])
            
            print("LOOP WARNA:", self.canvas.name_color, self.canvas.absen_color)
            print("EXPORT DATA:", name, absen)

            output_path = f"Output/{name}_{absen}.png"

            self.exporter.export(
                template_path=self.template_path,
                output_path=output_path,

                name=name,
                absen=absen,

                name_x=layout["nama"]["x"],
                name_y=layout["nama"]["y"],

                absen_x=layout["absen"]["x"],
                absen_y=layout["absen"]["y"],

                font_path=self.font_path,

                name_font_size=self.canvas.name_font_size,
                absen_font_size=self.canvas.absen_font_size,
                name_color=self.canvas.name_color,
                absen_color=self.canvas.absen_color,
            )

        self.status.config(
            text=f"Export selesai untuk {len(self.students)} siswa."
        )
        
        print("===== GENERATE SELESAI =====")