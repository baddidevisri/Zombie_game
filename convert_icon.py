"""Convert game_icon.png into a Windows .ico file.

Usage:
    python convert_icon.py

Install Pillow first if needed:
    python -m pip install Pillow
"""
from pathlib import Path
from PIL import Image

HERE = Path(__file__).resolve().parent
PNG_PATH = HERE / "game_icon.png"
ICO_PATH = HERE / "game_icon.ico"


def main():
    if not PNG_PATH.is_file():
        raise FileNotFoundError(
            f"Could not find {PNG_PATH.name}. Put game_icon.png in the same folder as this script."
        )

    with Image.open(PNG_PATH) as source:
        image = source.convert("RGBA")
        image.save(
            ICO_PATH,
            format="ICO",
            sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
        )

    print(f"Created: {ICO_PATH}")


if __name__ == "__main__":
    main()