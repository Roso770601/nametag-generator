from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os


class NameTagExporter:

    def __init__(self):
        pass

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

        # ==========================
        # Font
        # ==========================

        name_font = ImageFont.truetype(
            font_path,
            name_font_size
        )

        absen_font = ImageFont.truetype(
            font_path,
            absen_font_size
        )

        # ==========================
        # Debug
        # ==========================

        print("\n========== EXPORT ==========")
        print("Template :", template_path)
        print("Output   :", output_path)
        print("Nama     :", name)
        print("Absen    :", absen)
        print("Nama XY  :", name_x, name_y)
        print("Absen XY :", absen_x, absen_y)
        print("============================\n")

        # ==========================
        # Nama
        # ==========================

        draw.text(
            (float(name_x), float(name_y)),
            str(name),
            fill=name_color,
            font=name_font,
            anchor="mm"
        )

        # ==========================
        # No Absen
        # ==========================

        draw.text(
            (float(absen_x), float(absen_y)),
            str(absen),
            fill=absen_color,
            font=absen_font,
            anchor="mm"
        )

        # ==========================
        # Save
        # ==========================

        os.makedirs(
            os.path.dirname(output_path),
            exist_ok=True
        )

        image.save(output_path)

        print("EXPORT BERHASIL :", output_path)