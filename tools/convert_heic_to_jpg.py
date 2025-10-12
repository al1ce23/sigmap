#!/usr/bin/env python3
"""
HEIC to JPG Converter
Converts HEIC images to JPG format while preserving metadata
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener
pillow_heif.register_heif_opener()


def convert_heic_to_jpg(input_path, output_path=None, quality=100):
    """
    Convert a single HEIC file to JPG

    Args:
        input_path: Path to input HEIC file
        output_path: Path to output JPG file (optional, defaults to same name with .jpg)
        quality: JPEG quality (1-100, default 100)
    """
    input_path = Path(input_path)

    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        return False

    # Default output path
    if output_path is None:
        output_path = input_path.with_suffix('.jpg')
    else:
        output_path = Path(output_path)

    try:
        # Open HEIC image
        img = Image.open(input_path)

        # Preserve EXIF data
        exif_data = img.info.get('exif')

        # Convert and save as JPG
        if exif_data:
            img.save(output_path, "JPEG", quality=quality, exif=exif_data)
        else:
            img.save(output_path, "JPEG", quality=quality)

        print(f"✓ Converted: {input_path.name} → {output_path.name}")
        return True

    except Exception as e:
        print(f"✗ Error converting {input_path.name}: {e}")
        return False


def convert_directory(directory='.', quality=100):
    """
    Convert all HEIC files in a directory to JPG

    Args:
        directory: Directory to search for HEIC files (default: current directory)
        quality: JPEG quality (1-100, default 100)
    """
    directory = Path(directory)
    heic_files = list(directory.glob('*.heic')) + list(directory.glob('*.HEIC'))

    if not heic_files:
        print(f"No HEIC files found in {directory}")
        return

    print(f"Found {len(heic_files)} HEIC file(s)")
    print(f"Converting with quality={quality}...\n")

    success_count = 0
    for heic_file in heic_files:
        if convert_heic_to_jpg(heic_file, quality=quality):
            success_count += 1

    print(f"\nCompleted: {success_count}/{len(heic_files)} files converted successfully")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Single file or directory specified
        path = Path(sys.argv[1])
        quality = int(sys.argv[2]) if len(sys.argv) > 2 else 100

        if path.is_file():
            convert_heic_to_jpg(path, quality=quality)
        elif path.is_dir():
            convert_directory(path, quality=quality)
        else:
            print(f"Error: '{path}' is not a valid file or directory")
    else:
        # Convert all HEIC files in current directory
        convert_directory('.', quality=100)
