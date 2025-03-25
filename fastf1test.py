import os
from PIL import Image

def resize_images(source_folder):
    dpis = {
        'mdpi':   1.0,
        'hdpi':   1.5,
        'xhdpi':  2.0,
        'xxhdpi': 3.0,
        'xxxhdpi':4.0
    }

    if not os.path.isdir(source_folder):
        print(f"The folder '{source_folder}' does not exist.")
        return

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(source_folder, filename)
            name, ext = os.path.splitext(filename)

            with Image.open(input_path) as img:
                # STEP 1: Make base version height=500
                orig_w, orig_h = img.size
                base_height = 500
                aspect_ratio = orig_w / orig_h
                base_width = int(aspect_ratio * base_height)

                base_img = img.resize(
                    (base_width, base_height),
                    Image.Resampling.LANCZOS
                )

                # Optional: Save the 500px base image
                base_filename = f"{name}_base{ext}"
                base_img.save(os.path.join(source_folder, base_filename))

                # STEP 2: Make scaled versions for each dpi
                for dpi_label, scale in dpis.items():
                    new_w = int(base_width * scale)
                    new_h = int(base_height * scale)

                    resized = base_img.resize(
                        (new_w, new_h),
                        Image.Resampling.LANCZOS
                    )

                    dpi_folder = os.path.join(source_folder, dpi_label)
                    os.makedirs(dpi_folder, exist_ok=True)

                    output_filename = f"{name}_{dpi_label}{ext}"
                    output_path = os.path.join(dpi_folder, output_filename)

                    resized.save(output_path)
                    print(f"Saved: {output_path}")


if __name__ == "__main__":
    folder_to_resize = r"C:\Users\Antoan\Desktop\Team Logos"
    resize_images(folder_to_resize)
