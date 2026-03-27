import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Configuration
ANIMATIONS_DIR = r"C:\Users\chris\Downloads\game\animations"
OUTPUT_PATH = r"C:\Users\chris\Downloads\game\animations\assembly_preview.png"

# Animation metadata: name -> frame count
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

# Layout settings
LABEL_WIDTH = 120
FRAME_SPACING = 10
PADDING = 20
TEXT_HEIGHT = 30
FONT_SIZE = 14

def get_frame_number_height():
    """Calculate height needed for frame number labels"""
    return TEXT_HEIGHT

def load_animation_frames(animation_name):
    """Load all frames for an animation in order"""
    anim_dir = Path(ANIMATIONS_DIR) / animation_name
    frames = []
    
    frame_count = ANIMATIONS[animation_name]
    for i in range(1, frame_count + 1):
        frame_path = anim_dir / f"{i}.jpg"
        if frame_path.exists():
            frames.append(Image.open(frame_path).convert("RGBA"))
        else:
            raise FileNotFoundError(f"Missing frame: {frame_path}")
    
    return frames

def create_assembly_preview():
    """Create the assembled preview image"""
    
    # Load all animations
    all_animations = {}
    frame_dimensions = None
    
    for anim_name in ANIMATIONS.keys():
        frames = load_animation_frames(anim_name)
        all_animations[anim_name] = frames
        
        # Assume all frames are the same size (use first frame of first animation)
        if frame_dimensions is None:
            frame_dimensions = frames[0].size
    
    frame_width, frame_height = frame_dimensions
    
    # Calculate layout
    frame_number_height = get_frame_number_height()
    row_height = frame_height + frame_number_height + FRAME_SPACING
    
    # Calculate total width (for the widest animation)
    max_frames = max(ANIMATIONS.values())
    content_width = (frame_width + FRAME_SPACING) * max_frames - FRAME_SPACING
    total_width = LABEL_WIDTH + PADDING + content_width + PADDING
    
    # Calculate total height
    total_height = (len(ANIMATIONS) * row_height) + (PADDING * 2)
    
    # Create assembly image with white background
    assembly = Image.new("RGB", (total_width, total_height), color="white")
    draw = ImageDraw.Draw(assembly)
    
    # Try to load a nice font, fall back to default
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
        label_font = ImageFont.truetype("arial.ttf", FONT_SIZE + 2)
    except:
        font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    # Draw each animation row
    y_offset = PADDING
    
    for anim_name in ANIMATIONS.keys():
        frames = all_animations[anim_name]
        
        # Draw animation label on the left
        label_x = PADDING // 2
        label_y = y_offset + (frame_height - FONT_SIZE) // 2
        draw.text((label_x, label_y), anim_name, fill="black", font=label_font)
        
        # Draw frames
        x_offset = LABEL_WIDTH + PADDING
        
        for frame_idx, frame in enumerate(frames):
            # Draw frame number label above the frame
            frame_num = frame_idx + 1
            num_text = str(frame_num)
            num_x = x_offset + (frame_width - FONT_SIZE // 2) // 2
            num_y = y_offset
            draw.text((num_x, num_y), num_text, fill="gray", font=font)
            
            # Paste the frame image
            frame_y = y_offset + frame_number_height
            assembly.paste(frame, (x_offset, frame_y), frame)
            
            # Move to next frame position
            x_offset += frame_width + FRAME_SPACING
        
        # Move to next row
        y_offset += row_height
    
    # Save the assembly
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