import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

TRANSPARENT_DIR = r"C:\Users\chris\Downloads\game\animations\transparent"
OUTPUT_PATH = r"C:\Users\chris\Downloads\game\animations\assembly_preview_transparent.png"

ANIMATIONS = {
    "idle": 4,
    "run": 3,
    "jump": 4,
    "stomp": 4,
    "bounce": 4,
    "dash": 1,
    "dying": 4,
    "wall grab": 1,
}

LABEL_WIDTH = 120
FRAME_SPACING = 10
PADDING = 20
TEXT_HEIGHT = 30
FONT_SIZE = 14

def load_animation_frames(animation_name):
    anim_dir = Path(TRANSPARENT_DIR) / animation_name
    frames = []
    
    frame_count = ANIMATIONS[animation_name]
    for i in range(1, frame_count + 1):
        frame_path = anim_dir / f"{i}.png"
        if frame_path.exists():
            frames.append(Image.open(frame_path).convert("RGBA"))
        else:
            raise FileNotFoundError(f"Missing frame: {frame_path}")
    
    return frames

def create_assembly_preview():
    all_animations = {}
    frame_dimensions = None
    
    for anim_name in ANIMATIONS.keys():
        frames = load_animation_frames(anim_name)
        all_animations[anim_name] = frames
        
        if frame_dimensions is None:
            frame_dimensions = frames[0].size
    
    frame_width, frame_height = frame_dimensions
    
    frame_number_height = TEXT_HEIGHT
    row_height = frame_height + frame_number_height + FRAME_SPACING
    
    max_frames = max(ANIMATIONS.values())
    content_width = (frame_width + FRAME_SPACING) * max_frames - FRAME_SPACING
    total_width = LABEL_WIDTH + PADDING + content_width + PADDING
    
    total_height = (len(ANIMATIONS) * row_height) + (PADDING * 2)
    
    assembly = Image.new("RGBA", (total_width, total_height), color=(255, 255, 255, 0))
    draw = ImageDraw.Draw(assembly)
    
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
        label_font = ImageFont.truetype("arial.ttf", FONT_SIZE + 2)
    except:
        font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    y_offset = PADDING
    
    for anim_name in ANIMATIONS.keys():
        frames = all_animations[anim_name]
        
        label_x = PADDING // 2
        label_y = y_offset + (frame_height - FONT_SIZE) // 2
        draw.text((label_x, label_y), anim_name, fill="black", font=label_font)
        
        x_offset = LABEL_WIDTH + PADDING
        
        for frame_idx, frame in enumerate(frames):
            frame_num = frame_idx + 1
            num_text = str(frame_num)
            num_x = x_offset + (frame_width - FONT_SIZE // 2) // 2
            num_y = y_offset
            draw.text((num_x, num_y), num_text, fill="gray", font=font)
            
            frame_y = y_offset + frame_number_height
            assembly.paste(frame, (x_offset, frame_y), frame)
            
            x_offset += frame_width + FRAME_SPACING
        
        y_offset += row_height
    
    assembly.save(OUTPUT_PATH, "PNG")
    print(f"Assembly preview saved to: {OUTPUT_PATH}")
    print(f"Image size: {total_width}x{total_height} pixels")

if __name__ == "__main__":
    try:
        create_assembly_preview()
        print("Success!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()