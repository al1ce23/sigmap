# SIGMAp 

SImple-Geo-MAp is an interactive web-based map application for visualizing geotagged photos with clustering, time filtering, and thumbnail previews. Perfect for displaying large collections of geotagged photos or any location-based image collection.

## Features

- 🗺️ **Interactive Map** - Pan, zoom, and click markers to view photos
- 📸 **Photo Thumbnails** - Quick preview with lightbox for full-size images
- 🎯 **Marker Clustering** - Efficiently handles 100k+ photos
- 🕒 **Time Slider** - Filter photos by month and year
- 🌙 **Dark Mode** - Modern dark theme with warm amber accents
- 📱 **Responsive** - Works on desktop and mobile devices
- ⚡ **Performance** - Client-side filtering for instant updates

## Project Structure

```
SIGMAp/
├── map.html                    # Basic map (all photos, no time filter)
├── map_slider.html             # Map with time slider controls
├── prepare_data.py             # Unified data preparation script
├── photos.json                 # ExifTool output (generated)
├── photos_with_thumbs.geojson  # GeoJSON with thumbnails (generated)
├── thumbnails/                 # Generated thumbnail images
└── photos/                     # Original photos
```

## Requirements

### Required Software

- **Python 3.7+** - For data processing
- **ExifTool** - For extracting GPS data from photos
  - Download: https://exiftool.org/
  - Windows: Download `exiftool.exe` and add to PATH
  - Linux/Mac: `apt install libimage-exiftool-perl` or `brew install exiftool`

### Python Dependencies

```bash
pip install pillow
```

## Quick Start

### 1. Prepare Your Data

Extract GPS data from photos and create thumbnails:

```bash
python prepare_data.py --extract-exif /path/to/photos --convert --thumbnails
```

### 3. Start Web Server

```bash
python -m http.server 8000
```

## Usage

### Data Preparation Script

The `prepare_data.py` script handles all data preparation tasks:

**Extract EXIF data only:**
```bash
python prepare_data.py --extract-exif /path/to/photos
```

**Convert existing JSON to GeoJSON (no thumbnails):**
```bash
python prepare_data.py --convert
```

**Convert with thumbnail generation:**
```bash
python prepare_data.py --convert --thumbnails
```

**Custom thumbnail size:**
```bash
python prepare_data.py --convert --thumbnails --thumb-size 200 200
```

**Full pipeline (all-in-one):**
```bash
python prepare_data.py \
  --extract-exif /path/to/photos \
  --convert \
  --thumbnails \
  --thumb-size 150 150
```

**View all options:**
```bash
python prepare_data.py --help
```

### Map Versions

#### **map.html** - Basic Map
- Displays all photos on an interactive map
- Marker clustering for performance
- Click markers to view thumbnails
- Click thumbnails to view full-size images
- Best for: Simple visualization without time filtering

#### **map_slider.html** - Map with Time Filter
- All features of basic map
- Time slider to filter by month/year
- "Show all" toggle
- Clickable month markers
- Photo count statistics
- Best for: Exploring photos chronologically

## Configuration

### Customize Map Settings

Edit the HTML files to customize:

**Map Center & Zoom:**
```javascript
var map = L.map('map').setView([51.0, 13.7], 12);
//                                lat   lon   zoom
```

**Thumbnail Size in GeoJSON:**
```bash
python prepare_data.py --convert --thumbnails --thumb-size 200 200
```

**Accent Color:**
Edit CSS in `map_slider.html`:
```css
background: #f59e0b;  /* Amber - change to any color */
```

**Marker Icon:**
Edit custom icon in `map_slider.html`:
```javascript
var customIcon = L.divIcon({
  html: '<div style="background: #f59e0b; ..."></div>',
  // Customize color, size, etc.
});
```

## Troubleshooting

### No photos appear on map
- Check browser console (F12) for errors
- Verify `photos_with_thumbs.geojson` has proper UTF-8 encoding
- Ensure GeoJSON file is in the same directory as HTML files

### Lightbox shows thumbnail instead of full image
- Verify symbolic link to photos directory exists
- Check that `original` property in GeoJSON points to correct path

### ExifTool errors
- Make sure exiftool is installed and in PATH
- Try running `exiftool -ver` to verify installation

### Thumbnails not generating
- Install Pillow: `pip install pillow`
- Check write permissions for thumbnails directory
- Verify source photo paths in `photos.json` are accessible

### Encoding issues (weird characters)
- The new `prepare_data.py` always outputs UTF-8
- If using old scripts, re-run with `prepare_data.py`

## License

Copyleft.

## Credits

Built with:
- [Leaflet](https://leafletjs.com/) - Interactive maps
- [Leaflet.markercluster](https://github.com/Leaflet/Leaflet.markercluster) - Marker clustering
- [Lightbox2](https://lokeshdhakar.com/projects/lightbox2/) - Image gallery
- [ExifTool](https://exiftool.org/) - Metadata extraction
- [Pillow](https://python-pillow.org/) - Image processing
