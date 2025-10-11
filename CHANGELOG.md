# Changelog - SIGMAp

## [2025-10-11] - Major UI/UX Overhaul & Performance Improvements

### 🚀 New Features

#### **Heatmap View**
- Added heatmap visualization mode for better overview of photo density
- Toggle between markers and heatmap view with dedicated button
- Custom gradient (blue → cyan → green → yellow → red) showing photo concentration
- Extremely performant even with thousands of markers
- Time filtering works in both marker and heatmap mode

#### **URL Sharing**
- Share exact map views via URL parameters
- Parameters include: location (lat/lng), zoom level, selected month, and view mode
- URLs automatically update when navigating the map
- Example: `map.html?lat=51.05&lng=13.75&zoom=14&month=2024-03&view=heatmap`

#### **Hierarchical Time Navigation**
- Year/month structure for better organization
- Click year to expand and show months
- Only one year expanded at a time
- Automatic synchronization between slider and year/month selection
- "Show all" checkbox collapses all time selections

#### **Cluster Gallery Popup**
- Replaced spiderfy with elegant horizontal gallery
- Click cluster → see all photos in scrollable gallery (220x220px thumbnails)
- Click thumbnail → open full-quality lightbox
- Arrow key navigation in lightbox (← →) through all cluster photos
- Dynamic popup width based on number of images

#### **Random Photo Navigator**
- Jump to random visible marker at full zoom
- Only considers currently visible markers (respects time filter)
- Non-intrusive: jumps to location without opening popup
- Perfect for discovery and exploration

### ⚡ Performance Improvements

#### **Canvas Rendering**
- Switched from SVG to Canvas renderer for markers
- 30-50% performance improvement with many markers
- Smoother panning and zooming

#### **Aggressive Clustering**
- Increased `maxClusterRadius` from 80 to 150 pixels
- Clustering never disabled, even at max zoom (18)
- Optimized chunk loading (150ms intervals, 30ms delay)
- `removeOutsideVisibleBounds` for better viewport performance
- Disabled animations for faster rendering

#### **Image Loading Optimization**
- Popup images: Use 500x500 thumbnails from `/thumbnails`
- Lightbox: Full quality from `/photos` folder
- Lazy loading: Images only load when popup opens
- Preview thumbnails removed (simplified structure)

### 🎨 UI/UX Improvements

#### **Improved Layout**
- Cleaner control bar with better spacing
- Stats display next to buttons instead of below
- Year buttons always on one line (no movement/expansion)
- Months appear below years when expanded
- Maximum zoom limited to 18 (prevents too-close view)

#### **Enhanced Interactions**
- Clicking year auto-selects first available month
- "Show all" checkbox collapses months and clears year highlighting
- Slider movement automatically expands relevant year
- Year selection automatically unchecks "Show all"
- Initial state: "Show all" checked, no years selected

#### **Visual Polish**
- Larger cluster gallery images (220x220px)
- Horizontal scrolling with custom orange scrollbar
- Better hover effects with shadows
- Consistent orange accent color (#f59e0b) throughout
- Dark theme optimization

### 🐛 Bug Fixes

- Fixed checkbox state on initial load (now properly checked)
- Fixed overlapping markers at max zoom with always-on clustering
- Fixed laggy map with many markers at same location
- Fixed year/month synchronization with slider
- Fixed popup frame not containing all gallery images
- Fixed month markers not updating when slider moved

### 🔧 Technical Changes

- Added `Leaflet.heat` plugin for heatmap functionality
- Refactored cluster popup to use flexbox for horizontal layout
- Separated marker and heatmap update logic
- Added URL parameter parsing and updating functions
- Improved event handling for checkbox and year/month clicks
- Added global `currentExpandedYear` tracking for better state management

### 📊 Statistics

- Maximum zoom: 18 (was 19)
- Cluster radius: 150px (was 80px)
- Gallery thumbnail size: 220x220px (was 100x100px)
- Chunk loading: 100ms interval (was 200ms)
- Improved performance with 60,000+ photos

---

## Future Considerations

- [ ] Add year range selector for multi-year filtering
- [ ] Implement search functionality for specific photos
- [ ] Add photo metadata display (EXIF data)
- [ ] Create mobile-optimized view
- [ ] Add export functionality for filtered photo lists
- [ ] Implement user-defined color schemes
- [ ] Add keyboard shortcuts documentation
