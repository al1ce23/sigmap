#!/usr/bin/env python3
"""
SIGMAp Data Preparation Script
Extracts GPS data from photos and creates GeoJSON files with optional thumbnails.
"""

import os
import json
import sys
import argparse
import subprocess
from pathlib import Path
from PIL import Image


def run_exiftool(photo_dir, output_json):
    """
    Execute exiftool to extract GPS and metadata from photos.

    Args:
        photo_dir: Directory containing photos
        output_json: Output JSON file path
    """
    print(f"\n=== Extracting EXIF data from photos in {photo_dir} ===")

    # Check if exiftool is available
    try:
        subprocess.run(['exiftool', '-ver'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: exiftool not found. Please install exiftool first.")
        print("Download from: https://exiftool.org/")
        sys.exit(1)

    # Build exiftool command
    cmd = [
        'exiftool',
        '-r',                    # Recursive
        '-n',                    # Numeric GPS coordinates
        '-gpslatitude',
        '-gpslongitude',
        '-datetimeoriginal',
        '-filename',
        '-SourceFile',           # Include source file path
        '-ext', 'jpg',
        '-ext', 'jpeg',
        '-charset', 'UTF8',
        '-json',
        photo_dir
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)

        # Write output to file
        with open(output_json, 'w', encoding='utf-8') as f:
            f.write(result.stdout)

        print(f"Success: Extracted EXIF data to {output_json}")

        # Count photos
        data = json.loads(result.stdout)
        total = len(data)
        with_gps = sum(1 for p in data if 'GPSLatitude' in p and 'GPSLongitude' in p)
        print(f"Total photos: {total}, Photos with GPS: {with_gps}")

    except subprocess.CalledProcessError as e:
        print(f"Error running exiftool: {e}")
        print(f"STDERR: {e.stderr}")
        sys.exit(1)


def create_thumbnails(photo_path, thumb_dir, thumb_size=(150, 150)):
    """
    Create thumbnail for a photo.

    Args:
        photo_path: Path to original photo
        thumb_dir: Directory to save thumbnails
        thumb_size: Tuple of (width, height) for thumbnail size

    Returns:
        Path to created thumbnail or None if failed
    """
    filename = os.path.basename(photo_path)
    thumb_path = os.path.join(thumb_dir, filename)

    # Skip if thumbnail already exists
    if os.path.exists(thumb_path):
        return thumb_path

    try:
        with Image.open(photo_path) as img:
            img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
            img.save(thumb_path, quality=85, optimize=True)
        return thumb_path
    except Exception as e:
        print(f"Warning: Could not create thumbnail for {photo_path}: {e}")
        return None


def json_to_geojson(input_json, output_geojson, create_thumbs=False,
                    thumb_dir='thumbnails', thumb_size=(150, 150)):
    """
    Convert ExifTool JSON to GeoJSON format.

    Args:
        input_json: Path to ExifTool JSON file
        output_geojson: Path to output GeoJSON file
        create_thumbs: Whether to create thumbnails
        thumb_dir: Directory for thumbnails
        thumb_size: Tuple of (width, height) for thumbnails
    """
    print(f"\n=== Converting {input_json} to GeoJSON ===")

    # Load JSON file
    try:
        with open(input_json, 'r', encoding='utf-8') as f:
            photos = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_json} not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_json}: {e}")
        sys.exit(1)

    # Create thumbnail directory if needed
    if create_thumbs:
        os.makedirs(thumb_dir, exist_ok=True)
        print(f"Thumbnails will be saved to: {thumb_dir}")

    features = []
    skipped = 0
    thumbs_created = 0

    for i, p in enumerate(photos):
        if "GPSLatitude" not in p or "GPSLongitude" not in p:
            skipped += 1
            continue

        try:
            lat = float(p["GPSLatitude"])
            lon = float(p["GPSLongitude"])

            # Validate GPS coordinates
            if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                print(f"Warning: Invalid coordinates for {p.get('FileName', 'unknown')}: lat={lat}, lon={lon}")
                skipped += 1
                continue

            filename = p.get("FileName", "unknown")

            # Build properties
            properties = {
                "filename": filename,
                "datetime": p.get("DateTimeOriginal", "")
            }

            # Create thumbnail if requested
            if create_thumbs and "SourceFile" in p:
                thumb_path = create_thumbnails(p["SourceFile"], thumb_dir, thumb_size)
                if thumb_path:
                    thumbs_created += 1
                    properties["thumb"] = f"{thumb_dir}/{filename}"
                    properties["original"] = f"photos/{filename}"

                    # Progress indicator
                    if thumbs_created % 100 == 0:
                        print(f"  Created {thumbs_created} thumbnails...")

            # Create GeoJSON feature
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": properties
            }
            features.append(feature)

        except (ValueError, TypeError) as e:
            print(f"Warning: Could not parse coordinates for {p.get('FileName', 'unknown')}: {e}")
            skipped += 1
            continue

    # Create GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Write GeoJSON file
    try:
        with open(output_geojson, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)

        print(f"\nSuccess: Created {output_geojson}")
        print(f"  Features: {len(features)}")
        print(f"  Skipped: {skipped}")
        if create_thumbs:
            print(f"  Thumbnails created: {thumbs_created}")

    except IOError as e:
        print(f"Error: Could not write {output_geojson}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Prepare graffiti photo data for map visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract EXIF data from photos
  python prepare_data.py --extract-exif /path/to/photos

  # Convert JSON to GeoJSON (no thumbnails)
  python prepare_data.py --convert

  # Convert with thumbnail generation
  python prepare_data.py --convert --thumbnails

  # Full pipeline: extract EXIF and create GeoJSON with thumbnails
  python prepare_data.py --extract-exif /path/to/photos --convert --thumbnails
        """
    )

    # Extract EXIF options
    parser.add_argument('--extract-exif', metavar='DIR',
                        help='Extract EXIF data from photos in specified directory')

    # Convert options
    parser.add_argument('--convert', action='store_true',
                        help='Convert ExifTool JSON to GeoJSON')

    # Thumbnail options
    parser.add_argument('--thumbnails', action='store_true',
                        help='Generate thumbnails (use with --convert)')
    parser.add_argument('--thumb-size', type=int, nargs=2, default=[150, 150],
                        metavar=('WIDTH', 'HEIGHT'),
                        help='Thumbnail size (default: 150 150)')
    parser.add_argument('--thumb-dir', default='thumbnails',
                        help='Thumbnail directory (default: thumbnails)')

    # File paths
    parser.add_argument('--input-json', default='photos.json',
                        help='Input ExifTool JSON file (default: photos.json)')
    parser.add_argument('--output-geojson', default='photos_with_thumbs.geojson',
                        help='Output GeoJSON file (default: photos_with_thumbs.geojson)')

    args = parser.parse_args()

    # Validate arguments
    if not args.extract_exif and not args.convert:
        parser.error('Must specify --extract-exif and/or --convert')

    # Step 1: Extract EXIF data
    if args.extract_exif:
        if not os.path.isdir(args.extract_exif):
            print(f"Error: Directory not found: {args.extract_exif}")
            sys.exit(1)
        run_exiftool(args.extract_exif, args.input_json)

    # Step 2: Convert to GeoJSON
    if args.convert:
        json_to_geojson(
            args.input_json,
            args.output_geojson,
            create_thumbs=args.thumbnails,
            thumb_dir=args.thumb_dir,
            thumb_size=tuple(args.thumb_size)
        )

    print("\n=== Done! ===")


if __name__ == '__main__':
    main()
