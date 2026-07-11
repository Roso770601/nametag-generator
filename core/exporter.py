from PIL import Image, ImageDraw, ImageFont
import os


class NameTagExporter:

    def __init__(self):
        pass

    def to_pixel(self, value, max_val):
        """
        Convert posisi:
        - kalau <= 1 → dianggap RELATIVE (%)
        - kalau > 1 → dianggap PIXEL
        """
        value = float(value)
        if value <= 1:
            return value * max_val
        return value

    def export(
        self,
        template_path,
        output_path,
        name,
        absen,
        name_x,
        name_y,
        absen_x,
        absen_y,
        font_path,
        name_font_size=72,
        absen_font_size=56,
        name_color="black",
        absen_color="black"
    ):

        # ==========================
        # Load template
        # ==========================

        image = Image.open(template_path).convert("RGBA")
        draw = ImageDraw.Draw(image)

        img_w, img_h = image.size

        # ==========================
        # Convert posisi
        # ==========================

        name_px = float(name_x)
        name_py = float(name_y)

        absen_px = float(absen_x)
        absen_py = float(absen_y)

        # ==========================
        # Font
        # ==========================

        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font tidak ditemukan: {font_path}")

        name_font = ImageFont.truetype(font_path, int(name_font_size))
        absen_font = ImageFont.truetype(font_path, int(absen_font_size))

        # ==========================
        # Debug
        # ==========================

        print("\n========== EXPORT ==========")
        print("Template :", template_path)
        print("Output   :", output_path)
        print("Ukuran   :", img_w, "x", img_h)

        print("Nama     :", name)
        print("Nama PX  :", name_px, name_py)

        print("Absen    :", absen)
        print("Absen PX :", absen_px, absen_py)

        print("============================\n")

        # ==========================
        # DRAW NAMA
        # ==========================

        draw.text(
            (name_px, name_py),
            str(name),
            fill=name_color,
            font=name_font,
            anchor="mm"
        )

        # ==========================
        # DRAW ABSEN
        # ==========================

        absen_text = f"No. {absen}" if absen else "-"

        draw.text(
            (absen_px, absen_py),
            absen_text,
            fill=absen_color,
            font=absen_font,
            anchor="mm"
        )

        # ==========================
        # SAVE
        # ==========================

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        image.save(output_path)

        print("✅ EXPORT BERHASIL :", output_path)