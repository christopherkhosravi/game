import os
from PIL import Image
from pathlib import Path
from collections import defaultdict

ANIMATIONS_DIR = r"C:\Users\chris\Downloads\game\animations"
OUTPUT_BASE_DIR = r"C:\Users\chris\Downloads\game\animations\transparent"
TOLERANCE = 30

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

def sample_corner_colors(image):
    width, height = image.size
    corner_size = 5
    
    corners = {
        "top_left": image.crop((0, 0, corner_size, corner_size)),
        "top_right": image.crop((width - corner_size, 0, width, corner_size)),
        "bottom_left": image.crop((0, height - corner_size, corner_size, height)),
        "bottom_right": image.crop((width - corner_size, height - corner_size, width, height)),
    }
    
    colors = {}
    for corner_name, corner_img in corners.items():
        pixels = list(corner_img.getdata())
        if pixels:
            avg_r = sum(p[0] if isinstance(p, tuple) else p for p in pixels) // len(pixels)
            avg_g = sum(p[1] if isinstance(p, tuple) else p for p in pixels) // len(pixels)
            avg_b = sum(p[2] if isinstance(p, tuple) else p for p in pixels) // len(pixels)
            colors[corner_name] = (avg_r, avg_g, avg_b)
    
    return colors

def colors_match(color1, color2, tolerance):
    if len(color1) < 3 or len(color2) < 3:
        return False
    
    r_diff = abs(color1[0] - color2[0])
    g_diff = abs(color1[1] - color2[1])
    b_diff = abs(color1[2] - color2[2])
    
    return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance

def remove_background(image_path, output_path, tolerance):
    try:
        img = Image.open(image_path)
        
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        corner_colors = sample_corner_colors(img)
        
        avg_r = sum(c[0] for c in corner_colors.values()) // len(corner_colors)
        avg_g = sum(c[1] for c in corner_colors.values()) // len(corner_colors)
        avg_b = sum(c[2] for c in corner_colors.values()) // len(corner_colors)
        target_color = (avg_r, avg_g, avg_b)
        
        img = img.convert('RGBA')
        data = img.getdata()
        
        new_data = []
        for pixel in data:
            rgb = pixel[:3]
            if colors_match(rgb, target_color, tolerance):
                new_data.append((rgb[0], rgb[1], rgb[2], 0))
            else:
                new_data.append(pixel)
        
        img.putdata(new_data)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        img.save(output_path, 'PNG')
        return True, target_color
    
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 70)
    print("SPRITE BACKGROUND REMOVER")
    print("=" * 70)
    print(f"Source: {ANIMATIONS_DIR}")
    print(f"Output: {OUTPUT_BASE_DIR}")
    print(f"Tolerance: {TOLERANCE}")
    print("=" * 70)
    print()
    
    results = defaultdict(list)
    total_processed = 0
    total_success = 0
    
    for anim_name in ANIMATIONS.keys():
        anim_dir = Path(ANIMATIONS_DIR) / anim_name
        frame_count = ANIMATIONS[anim_name]
        
        print(f"\n[{anim_name.upper()}] Processing {frame_count} frames...")
        print("-" * 70)
        
        for frame_num in range(1, frame_count + 1):
            input_path = anim_dir / f"{frame_num}.jpg"
            output_dir = Path(OUTPUT_BASE_DIR) / anim_name
            output_path = output_dir / f"{frame_num}.png"
            
            total_processed += 1
            
            if not input_path.exists():
                status = "FAILED - File not found"
                results[anim_name].append((frame_num, status))
                print(f"  Frame {frame_num}: {status}")
                continue
            
            success, color_info = remove_background(str(input_path), str(output_path), TOLERANCE)
            
            if success:
                total_success += 1
                if isinstance(color_info, tuple):
                    color_rgb = f"RGB({color_info[0]}, {color_info[1]}, {color_info[2]})"
                    status = f"SUCCESS - Removed {color_rgb}"
                else:
                    status = "SUCCESS"
                results[anim_name].append((frame_num, status))
                print(f"  Frame {frame_num}: {status}")
            else:
                status = f"FAILED - {color_info}"
                results[anim_name].append((frame_num, status))
                print(f"  Frame {frame_num}: {status}")
    
    print()
    print("=" * 70)
    print("SUMMARY REPORT")
    print("=" * 70)
    print(f"Total files processed: {total_processed}")
    print(f"Successful: {total_success}")
    print(f"Failed: {total_processed - total_success}")
    print()
    print("DETAILED RESULTS:")
    print("-" * 70)
    
    for anim_name in ANIMATIONS.keys():
        print(f"\n{anim_name.upper()}:")
        for frame_num, status in results[anim_name]:
            print(f"  {frame_num}.jpg -> {frame_num}.png: {status}")
    
    print()
    print("=" * 70)
    print(f"Output directory: {OUTPUT_BASE_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()