#!/usr/bin/env python3
"""
Compress GeoJSON file to reduce file size and improve loading performance.
Removes whitespace and rounds coordinates to reduce precision.
"""

import json
import sys
import os
import gzip
import argparse


def compress_geojson(input_file, output_file, decimals=6, create_gzip=True):
    """
    Compress GeoJSON by removing whitespace and rounding coordinates.

    Args:
        input_file: Input GeoJSON file
        output_file: Output compressed GeoJSON file
        decimals: Number of decimal places for coordinates (6 = ~0.1m precision)
        create_gzip: Also create a .gz version for HTTP compression
    """
    print(f"Loading {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    original_size = os.path.getsize(input_file)
    num_features = len(data.get('features', []))

    print(f"  Features: {num_features:,}")
    print(f"  Original size: {original_size:,} bytes ({original_size/1024/1024:.1f} MB)")

    # Round coordinates to reduce file size
    print(f"Rounding coordinates to {decimals} decimal places...")
    for feature in data.get('features', []):
        if 'geometry' in feature and 'coordinates' in feature['geometry']:
            coords = feature['geometry']['coordinates']
            if isinstance(coords, list) and len(coords) == 2:
                # Round lon, lat
                feature['geometry']['coordinates'] = [
                    round(coords[0], decimals),
                    round(coords[1], decimals)
                ]

    # Write compressed JSON (no whitespace)
    print(f"Writing compressed file to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    compressed_size = os.path.getsize(output_file)
    reduction = (1 - compressed_size / original_size) * 100

    print(f"  Compressed size: {compressed_size:,} bytes ({compressed_size/1024/1024:.1f} MB)")
    print(f"  Reduction: {reduction:.1f}%")

    # Create gzipped version for HTTP serving
    if create_gzip:
        gzip_file = output_file + '.gz'
        print(f"\nCreating gzipped version: {gzip_file}...")
        with open(output_file, 'rb') as f_in:
            with gzip.open(gzip_file, 'wb', compresslevel=9) as f_out:
                f_out.writelines(f_in)

        gzip_size = os.path.getsize(gzip_file)
        gzip_reduction = (1 - gzip_size / original_size) * 100

        print(f"  Gzipped size: {gzip_size:,} bytes ({gzip_size/1024/1024:.1f} MB)")
        print(f"  Total reduction: {gzip_reduction:.1f}%")
        print(f"\n  💡 Tip: Serve {os.path.basename(gzip_file)} with your web server for best performance!")


def main():
    parser = argparse.ArgumentParser(
        description='Compress GeoJSON file for better web performance',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
  # Compress photos.geojson
  python compress_geojson.py photos.geojson

  # Custom output file and precision
  python compress_geojson.py photos.geojson -o photos.min.geojson --decimals 5

This will:
  1. Remove all whitespace from JSON
  2. Round coordinates to reduce precision (default 6 decimals = ~0.1m accuracy)
  3. Create a .gz version for HTTP serving (80-90% smaller!)

To use the .gz file:
  - Rename photos.geojson.gz to photos.geojson.gz
  - Configure your web server to serve .gz files with Content-Encoding: gzip
  - Or simply use the minified .geojson file (already 30-40% smaller)
        """
    )

    parser.add_argument('input', help='Input GeoJSON file')
    parser.add_argument('-o', '--output', help='Output file (default: input.min.geojson)')
    parser.add_argument('-d', '--decimals', type=int, default=6,
                       help='Coordinate precision (default: 6 = ~0.1m accuracy)')
    parser.add_argument('--no-gzip', action='store_true',
                       help='Skip creating .gz file')

    args = parser.parse_args()

    # Determine output file
    if args.output:
        output = args.output
    else:
        base, ext = os.path.splitext(args.input)
        output = f"{base}.min{ext}"

    # Check input exists
    if not os.path.exists(args.input):
        print(f"Error: {args.input} not found")
        sys.exit(1)

    # Compress
    compress_geojson(
        args.input,
        output,
        decimals=args.decimals,
        create_gzip=not args.no_gzip
    )

    print("\n✅ Done!")
    print(f"\nNext steps:")
    print(f"  1. Update map.html to load '{os.path.basename(output)}' instead")
    print(f"  2. Or configure your web server to serve the .gz file automatically")


if __name__ == '__main__':
    main()
