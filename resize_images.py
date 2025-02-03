import os
import shutil

# 🔹 Change these paths as needed
RES_FOLDER = "C:/Users/Antoan/PycharmProjects/F1AppBackend/app/static/images/res"  # Path to the Android res folder (contains mipmap-* directories)
OUTPUT_FOLDER = "C:/Users/Antoan/PycharmProjects/F1AppBackend/app/static/images"  # Path where renamed images will be stored

# Mapping Android's mipmap folders to DPI labels
DPI_MAPPING = {
    "mipmap-ldpi": "ldpi",
    "mipmap-mdpi": "mdpi",
    "mipmap-hdpi": "hdpi",
    "mipmap-xhdpi": "xhdpi",
    "mipmap-xxhdpi": "xxhdpi",
    "mipmap-xxxhdpi": "xxxhdpi"
}


def rename_and_move_images(res_folder, output_folder):
    """
    Rename images from res/mipmap-* and move them to a new location.

    Args:
        res_folder (str): Path to the res folder containing mipmap directories.
        output_folder (str): Path to the output folder where renamed images will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create output directory if it doesn't exist

    for mipmap_folder, dpi in DPI_MAPPING.items():
        source_path = os.path.join(res_folder, mipmap_folder)

        if not os.path.exists(source_path):
            print(f"Skipping {mipmap_folder} (not found)")
            continue

        for file in os.listdir(source_path):
            if file.endswith((".png", ".jpg", ".webp")):  # Process only image files
                old_file_path = os.path.join(source_path, file)
                file_name, ext = os.path.splitext(file)

                # New file name with DPI suffix
                new_file_name = f"{file_name}_{dpi}{ext}"
                new_file_path = os.path.join(output_folder, new_file_name)

                # Move and rename the file
                shutil.copy2(old_file_path, new_file_path)
                print(f"Moved: {old_file_path} → {new_file_path}")


if __name__ == "__main__":
    rename_and_move_images(RES_FOLDER, OUTPUT_FOLDER)
