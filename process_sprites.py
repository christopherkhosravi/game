from pathlib import Path
from PIL import Image

tasks = [
    (r"C:\Users\chris\Downloads\game\animations\run\new 1.jpg",
     r"C:\Users\chris\Downloads\game\animations\transparent\run\1.png"),
    (r"C:\Users\chris\Downloads\game\animations\run\new 2.jpg",
     r"C:\Users\chris\Downloads\game\animations\transparent\run\2.png"),
    (r"C:\Users\chris\Downloads\game\animations\run\new 3.jpg",
     r"C:\Users\chris\Downloads\game\animations\transparent\run\3.png"),
    (r"C:\Users\chris\Downloads\game\animations\dead hang.jpg",
     r"C:\Users\chris\Downloads\game\animations\transparent\dead hang\1.png"),
]

THRESHOLD = 60

FLIP_HORIZONTAL = {
    r"C:\Users\chris\Downloads\game\animations\run\new 2.jpg",
}

for src, dst in tasks:
    img = Image.open(src).convert("RGBA")
    pixels = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            if r < THRESHOLD and g < THRESHOLD and b < THRESHOLD:
                pixels[x, y] = (0, 0, 0, 0)
    if src in FLIP_HORIZONTAL:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    img.save(dst)
    print(f"Saved: {dst}")

print("Done.")
