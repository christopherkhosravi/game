import os
from PIL import Image

input_files = [
    ("new bounce 2.jpg", "1.png"),
    ("new bounce 1.jpg", "2.png"),
    ("new bounce 3.jpg", "3.png"),
]

base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "transparent", "bounce")
os.makedirs(output_dir, exist_ok=True)

try:
    from rembg import remove
    use_rembg = True
    print("Using rembg for background removal")
except ImportError:
    use_rembg = False
    print("rembg not available, using threshold-based removal (R<50 & G<50 & B<50)")

for src_name, dst_name in input_files:
    src_path = os.path.join(base_dir, src_name)
    dst_path = os.path.join(output_dir, dst_name)

    img = Image.open(src_path).convert("RGBA")

    if use_rembg:
        img = remove(img)
    else:
        pixels = img.load()
        width, height = img.size
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                if r < 50 and g < 50 and b < 50:
                    pixels[x, y] = (r, g, b, 0)

    img.save(dst_path, "PNG")
    print(dst_path)
