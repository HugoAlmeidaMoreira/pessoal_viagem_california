import os
from PIL import Image
import argparse

def resize_and_compress_image(input_path, output_path=None, width=1280, height=720, quality=85):
    """
    Resize and compress an image to make it suitable for YouTube thumbnails.
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Get original size
        original_size = os.path.getsize(input_path) / 1024  # KB
        
        # Resize image to YouTube recommended size
        img.thumbnail((width, height), Image.LANCZOS)
        
        # Generate output path if not provided
        if output_path is None:
            file_name, file_ext = os.path.splitext(input_path)
            output_path = f"{file_name}_thumbnail{file_ext}"
        
        # Convert RGBA to RGB for JPG if needed
        if img.mode in ('RGBA', 'LA') and output_path.lower().endswith(('.jpg', '.jpeg')):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
            img = background
        
        # Save the image with compression
        img.save(output_path, quality=quality, optimize=True)
        
        # Get new size
        new_size = os.path.getsize(output_path) / 1024  # KB
        
        print(f"Original size: {original_size:.2f} KB")
        print(f"New size: {new_size:.2f} KB")
        print(f"Reduction: {(1 - new_size/original_size) * 100:.2f}%")
        print(f"Image saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description='Create a smaller image for YouTube thumbnails')
    parser.add_argument('input_image', help='Path to the input image file')
    parser.add_argument('-o', '--output', help='Path to save the output image')
    parser.add_argument('-q', '--quality', type=int, default=85, 
                        help='JPEG compression quality 1-100 (default: 85)')
    
    args = parser.parse_args()
    
    resize_and_compress_image(
        args.input_image,
        args.output,
        quality=args.quality
    )

if __name__ == "__main__":
    main()