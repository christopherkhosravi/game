from PIL import Image, ImageDraw, ImageFont
import os

ANIMATIONS_DIR = os.path.dirname(os.path.abspath(__file__))

ANIMATIONS = [
    ("idle",      4),
    ("run",       3),
    ("jump",      4),
    ("stomp",     4),
    ("bounce",    4),
    ("dash",      1),
    ("dying",     4),
    ("wall grab", 1),
]

LABEL_WIDTH   = 120   # pixels reserved for the animation name on the left
FRAME_PADDING = 8     # gap between frames
ROW_PADDING   = 16    # gap between rows
HEADER_HEIGHT = 24    # height for the frame-number header row
FONT_SIZE     = 14

# Load all frames first so we can determine a consistent frame size
def load_frames(name, count):
    frames = []
    folder = os.path.join(ANIMATIONS_DIR, name)
    for i in range(1, count + 1):
        path = os.path.join(folder, f"{i}.jpg")
        frames.append(Image.open(path).convert("RGBA"))
    return frames

all_frames = {name: load_frames(name, count) for name, count in ANIMATIONS}

# Determine the largest frame dimensions to use as the uniform cell size
max_w = max(f.width  for frames in all_frames.values() for f in frames)
max_h = max(f.height for frames in all_frames.values() for f in frames)
CELL_W, CELL_H = max_w, max_h

# Calculate canvas size
max_frames = max(count for _, count in ANIMATIONS)
canvas_w = LABEL_WIDTH + (CELL_W + FRAME_PADDING) * max_frames
row_h    = HEADER_HEIGHT + CELL_H + ROW_PADDING
canvas_h = row_h * len(ANIMATIONS) + ROW_PADDING

canvas = Image.new("RGBA", (canvas_w, canvas_h), (30, 30, 30, 255))
draw   = ImageDraw.Draw(canvas)

# Try to load a nicer font; fall back to default if unavailable
try:
    font       = ImageFont.truetype("arial.ttf", FONT_SIZE)
    font_small = ImageFont.truetype("arial.ttf", FONT_SIZE - 2)
except OSError:
    font       = ImageFont.load_default()
    font_small = font

TEXT_COLOR  = (220, 220, 220, 255)
NUM_COLOR   = (160, 200, 255, 255)
LABEL_COLOR = (255, 220, 100, 255)

for row_idx, (name, count) in enumerate(ANIMATIONS):
    y_top = ROW_PADDING + row_idx * row_h

    # Draw animation label (vertically centred in the row)
    label_y = y_top + HEADER_HEIGHT + CELL_H // 2
    draw.text((4, label_y - FONT_SIZE // 2), name, font=font, fill=LABEL_COLOR)

    frames = all_frames[name]
    for col_idx, frame in enumerate(frames):
        x_left = LABEL_WIDTH + col_idx * (CELL_W + FRAME_PADDING)

        # Frame number above the cell
        num_text = str(col_idx + 1)
        bbox = draw.textbbox((0, 0), num_text, font=font_small)
        text_w = bbox[2] - bbox[0]
        draw.text(
            (x_left + (CELL_W - text_w) // 2, y_top + 4),
            num_text, font=font_small, fill=NUM_COLOR
        )

        # Paste frame centred in its cell
        paste_x = x_left + (CELL_W - frame.width) // 2
        paste_y = y_top + HEADER_HEIGHT + (CELL_H - frame.height) // 2
        canvas.paste(frame, (paste_x, paste_y), frame)

out_path = os.path.join(ANIMATIONS_DIR, "assembly_preview.png")
canvas.convert("RGB").save(out_path, "PNG")
print(f"Saved: {out_path}  ({canvas_w}x{canvas_h}px)")
