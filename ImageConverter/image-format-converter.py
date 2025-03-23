#!/usr/bin/env python3
"""
Image Format Converter - A script to convert images between different formats
Currently supports converting WebP images to JPEG
"""

import os
import argparse
from PIL import Image

def convert_webp_to_jpeg(input_path, output_path=None, quality=90):
    """
    Convert a WebP image to JPEG format
    
    Args:
        input_path (str): Path to the WebP image
        output_path (str, optional): Path where the JPEG will be saved. If None, 
                                     it will use the same filename with .jpg extension
        quality (int, optional): JPEG quality (1-100). Default is 90
    
    Returns:
        str: Path to the converted image
    """
    try:
        # Open the WebP image
        img = Image.open(input_path)
        
        # If output_path is not provided, create one based on the input
        if output_path is None:
            filename = os.path.splitext(input_path)[0]
            output_path = f"{filename}.jpg"
        
        # Convert and save as JPEG
        if img.mode in ("RGBA", "LA"):
            # WebP can have transparency, JPEG doesn't support it
            # Create a white background and paste the image on it
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if img.mode == "RGBA" else img.split()[1])
            background.save(output_path, "JPEG", quality=quality)
        else:
            img.convert("RGB").save(output_path, "JPEG", quality=quality)
        
        print(f"Converted: {input_path} -> {output_path}")
        return output_path
    except Exception as e:
        print(f"Error converting {input_path}: {e}")
        return None

def batch_convert_webp_to_jpeg(directory, quality=90, recursive=False):
    """
    Convert all WebP images in a directory to JPEG
    
    Args:
        directory (str): Directory containing WebP images
        quality (int, optional): JPEG quality. Default is 90
        recursive (bool, optional): Whether to process subdirectories. Default is False
    """
    if recursive:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.webp'):
                    convert_webp_to_jpeg(os.path.join(root, file), quality=quality)
    else:
        for file in os.listdir(directory):
            if file.lower().endswith('.webp'):
                convert_webp_to_jpeg(os.path.join(directory, file), quality=quality)

def main():
    parser = argparse.ArgumentParser(description="Convert image formats")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # WebP to JPEG converter
    webp_parser = subparsers.add_parser("webp2jpeg", help="Convert WebP to JPEG")
    webp_parser.add_argument("input", help="Input WebP file or directory")
    webp_parser.add_argument("-o", "--output", help="Output JPEG file (only used when input is a single file)")
    webp_parser.add_argument("-q", "--quality", type=int, default=90, help="JPEG quality (1-100)")
    webp_parser.add_argument("-r", "--recursive", action="store_true", help="Process directories recursively")
    
    args = parser.parse_args()
    
    if args.command == "webp2jpeg":
        if os.path.isdir(args.input):
            if args.output:
                print("Warning: Output path is ignored when processing a directory")
            batch_convert_webp_to_jpeg(args.input, args.quality, args.recursive)
        else:
            convert_webp_to_jpeg(args.input, args.output, args.quality)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
