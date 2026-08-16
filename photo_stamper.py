#!/usr/bin/env python3
"""
Photo Stamper — Overlay location & date on your photos.

Reads photos from macOS Photos app or a local folder, extracts GPS + date
metadata, reverse-geocodes the location, and stamps each photo with a
nice overlay in the bottom-right corner.

Usage:
    python3 photo_stamper.py                  # Interactive mode
    python3 photo_stamper.py --help           # Show all options

Dependencies (install once):
    pip3 install Pillow osxphotos photoscript reverse_geocoder pilmoji exifread --break-system-packages
"""

import argparse
import os
import sys
import shutil
import tempfile
import struct
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Lazy imports so we can give friendly install messages
# ---------------------------------------------------------------------------
def _require(module_name, pip_name=None):
    """Import a module or tell the user how to install it."""
    import importlib
    try:
        return importlib.import_module(module_name)
    except ImportError:
        pip_name = pip_name or module_name
        print(f"\n❌  Missing dependency: {pip_name}")
        print(f"   Install it with:  pip3 install {pip_name} --break-system-packages\n")
        sys.exit(1)


# ===========================================================================
#  METADATA HELPERS
# ===========================================================================

def _dms_to_decimal(dms_values, ref):
    """Convert EXIF GPS DMS (degrees, minutes, seconds) to decimal."""
    try:
        # Handle both Ratio objects and plain floats
        def _val(v):
            if hasattr(v, 'num') and hasattr(v, 'den'):
                return float(v.num) / float(v.den) if v.den else 0.0
            return float(v)

        d = _val(dms_values[0])
        m = _val(dms_values[1])
        s = _val(dms_values[2])
        decimal = d + m / 60.0 + s / 3600.0
        if ref in ('S', 'W'):
            decimal = -decimal
        return decimal
    except Exception:
        return None


def extract_metadata_exif(filepath):
    """Extract date and GPS from a photo file using exifread."""
    exifread = _require('exifread')
    date_taken = None
    lat = None
    lon = None

    try:
        with open(filepath, 'rb') as f:
            tags = exifread.process_file(f, details=False)

        # ---- Date ----
        for tag_name in ('EXIF DateTimeOriginal', 'EXIF DateTimeDigitized', 'Image DateTime'):
            if tag_name in tags:
                try:
                    date_taken = datetime.strptime(str(tags[tag_name]), '%Y:%m:%d %H:%M:%S')
                    break
                except ValueError:
                    pass

        # ---- GPS ----
        gps_lat = tags.get('GPS GPSLatitude')
        gps_lat_ref = tags.get('GPS GPSLatitudeRef')
        gps_lon = tags.get('GPS GPSLongitude')
        gps_lon_ref = tags.get('GPS GPSLongitudeRef')

        if gps_lat and gps_lon:
            lat = _dms_to_decimal(gps_lat.values, str(gps_lat_ref))
            lon = _dms_to_decimal(gps_lon.values, str(gps_lon_ref))

    except Exception as e:
        print(f"  ⚠️  Could not read EXIF from {Path(filepath).name}: {e}")

    return date_taken, lat, lon


# ===========================================================================
#  REVERSE GEOCODING
# ===========================================================================

_geocoder = None

def reverse_geocode(lat, lon):
    """Return a human-readable place name for GPS coordinates."""
    global _geocoder
    if lat is None or lon is None:
        return None
    rg = _require('reverse_geocoder', 'reverse_geocoder')
    if _geocoder is None:
        # First call loads the K-D tree (takes ~1-2s)
        print("  📍 Loading offline geocoder (one-time)...")
    result = rg.search([(lat, lon)], verbose=False)
    if result:
        r = result[0]
        city = r.get('name', '')
        country = r.get('cc', '')
        admin1 = r.get('admin1', '')  # state / region
        # Build a nice string
        parts = [p for p in [city, admin1, country] if p]
        return ', '.join(parts)
    return None


# ===========================================================================
#  IMAGE OVERLAY
# ===========================================================================

def _get_font(size):
    """Get the best available font at the given size."""
    PIL = _require('PIL', 'Pillow')
    from PIL import ImageFont

    # Preferred macOS fonts (in order)
    font_paths = [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/HelveticaNeue.ttc',
        '/System/Library/Fonts/SFNSText.ttf',
        '/System/Library/Fonts/SFNS.ttf',
        '/Library/Fonts/Arial.ttf',
        '/System/Library/Fonts/Supplemental/Arial.ttf',
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                continue
    # Fallback
    return ImageFont.load_default()


def stamp_photo(input_path, output_path, location_text, date_text):
    """
    Overlay location & date text on the bottom-right of the photo.
    Uses a semi-transparent dark pill background with white text.
    """
    PIL = _require('PIL', 'Pillow')
    from PIL import Image, ImageDraw, ImageFont

    img = Image.open(input_path).convert('RGBA')
    w, h = img.size

    # ---- Dynamic sizing based on image dimensions ----
    short_side = min(w, h)
    font_size = max(16, int(short_side * 0.025))  # ~2.5% of short side
    padding_x = int(font_size * 1.2)
    padding_y = int(font_size * 0.7)
    margin = int(short_side * 0.025)
    line_spacing = int(font_size * 0.4)
    corner_radius = int(font_size * 0.6)

    font = _get_font(font_size)

    # Build the two lines of text
    lines = []
    if location_text:
        lines.append(f"📍  {location_text}")
    if date_text:
        lines.append(f"📅  {date_text}")

    if not lines:
        # Nothing to stamp — just copy
        if input_path != output_path:
            shutil.copy2(input_path, output_path)
        return False

    # Try pilmoji for emoji support; fall back to plain Pillow
    use_pilmoji = False
    try:
        from pilmoji import Pilmoji
        use_pilmoji = True
    except ImportError:
        # Replace emoji with text equivalents
        lines = [l.replace('📍', '[LOC]').replace('📅', '[DATE]') for l in lines]

    # ---- Measure text ----
    dummy = Image.new('RGBA', (1, 1))
    ddraw = ImageDraw.Draw(dummy)
    line_sizes = []
    for line in lines:
        bbox = ddraw.textbbox((0, 0), line, font=font)
        lw = bbox[2] - bbox[0]
        lh = bbox[3] - bbox[1]
        line_sizes.append((lw, lh))

    text_block_w = max(s[0] for s in line_sizes)
    text_block_h = sum(s[1] for s in line_sizes) + line_spacing * (len(lines) - 1)

    box_w = text_block_w + padding_x * 2
    box_h = text_block_h + padding_y * 2

    # Position: bottom-right with margin
    box_x = w - box_w - margin
    box_y = h - box_h - margin

    # ---- Draw semi-transparent rounded-rect background ----
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rounded_rectangle(
        [box_x, box_y, box_x + box_w, box_y + box_h],
        radius=corner_radius,
        fill=(0, 0, 0, 160),  # semi-transparent black
    )
    img = Image.alpha_composite(img, overlay)

    # ---- Draw text ----
    if use_pilmoji:
        with Pilmoji(img) as pmj:
            y_cursor = box_y + padding_y
            for i, line in enumerate(lines):
                lw, lh = line_sizes[i]
                x_pos = box_x + padding_x
                # Draw text shadow first
                pmj.text((x_pos + 1, y_cursor + 1), line, font=font, fill=(0, 0, 0, 200))
                # Main text
                pmj.text((x_pos, y_cursor), line, font=font, fill=(255, 255, 255, 255))
                y_cursor += lh + line_spacing
    else:
        draw = ImageDraw.Draw(img)
        y_cursor = box_y + padding_y
        for i, line in enumerate(lines):
            lw, lh = line_sizes[i]
            x_pos = box_x + padding_x
            # Outline / stroke effect
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx or dy:
                        draw.text((x_pos + dx, y_cursor + dy), line, font=font, fill=(0, 0, 0, 220))
            draw.text((x_pos, y_cursor), line, font=font, fill=(255, 255, 255, 255))
            y_cursor += lh + line_spacing

    # ---- Save as RGB JPEG (or PNG if input was PNG) ----
    ext = Path(output_path).suffix.lower()
    if ext in ('.png',):
        img.save(output_path, 'PNG')
    else:
        img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=95, exif=_copy_exif_bytes(input_path))

    return True


def _copy_exif_bytes(filepath):
    """Try to extract raw EXIF bytes to preserve in the output JPEG."""
    try:
        PIL = _require('PIL', 'Pillow')
        from PIL import Image
        src = Image.open(filepath)
        exif = src.info.get('exif', b'')
        return exif
    except Exception:
        return b''


# ===========================================================================
#  INPUT SOURCES
# ===========================================================================

PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.heic', '.tiff', '.tif', '.bmp', '.webp'}


def collect_from_folder(folder_path):
    """Return list of photo file paths from a local folder."""
    folder = Path(folder_path)
    if not folder.is_dir():
        print(f"❌  Folder not found: {folder_path}")
        sys.exit(1)
    photos = sorted([
        p for p in folder.iterdir()
        if p.suffix.lower() in PHOTO_EXTENSIONS and not p.name.startswith('.')
    ])
    return photos


def collect_from_photos_app(album_name=None, limit=None):
    """
    Export photos from the macOS Photos app and return (temp_dir, file_list).
    If album_name is given, exports only that album; otherwise shows available albums.
    """
    osxphotos = _require('osxphotos')
    import osxphotos as oxp

    print("  📸 Opening Photos library (this may take a moment)...")
    photosdb = oxp.PhotosDB()

    if album_name:
        # Find the album
        all_albums = photosdb.album_info
        match = [a for a in all_albums if a.title.lower() == album_name.lower()]
        if not match:
            print(f"❌  Album '{album_name}' not found. Available albums:")
            for a in sorted(all_albums, key=lambda x: x.title):
                print(f"     • {a.title} ({len(a.photos)} photos)")
            sys.exit(1)
        photos = match[0].photos
    else:
        # Interactive: list albums and let user pick
        all_albums = sorted(photosdb.album_info, key=lambda x: x.title)
        if not all_albums:
            print("❌  No albums found in Photos library.")
            sys.exit(1)
        print("\n  Available albums:")
        for i, a in enumerate(all_albums, 1):
            print(f"    {i:3d}. {a.title} ({len(a.photos)} photos)")
        print(f"    {'all':>3s}. All photos in library")
        choice = input("\n  Choose an album number (or 'all'): ").strip()
        if choice.lower() == 'all':
            photos = photosdb.photos()
        else:
            try:
                idx = int(choice) - 1
                photos = all_albums[idx].photos
                album_name = all_albums[idx].title
            except (ValueError, IndexError):
                print("❌  Invalid choice.")
                sys.exit(1)

    if limit:
        photos = photos[:limit]

    print(f"  Found {len(photos)} photo(s)." + (f" (album: {album_name})" if album_name else ""))

    # Export to a temp directory, collecting metadata along the way
    tmp_dir = tempfile.mkdtemp(prefix='photo_stamper_')
    results = []  # list of (exported_path, date_taken, lat, lon)

    for photo in photos:
        # Get metadata from osxphotos directly
        date_taken = photo.date
        lat = photo.latitude if photo.latitude else None
        lon = photo.longitude if photo.longitude else None

        # Export the photo
        try:
            exported = photo.export(tmp_dir, use_photos_export=True)
            if exported:
                export_path = exported[0]
                results.append((Path(export_path), date_taken, lat, lon))
        except Exception as e:
            print(f"  ⚠️  Could not export {photo.original_filename}: {e}")

    return tmp_dir, results


# ===========================================================================
#  OUTPUT
# ===========================================================================

def import_to_photos_album(file_paths, album_name="Stamped Photos"):
    """Import processed photos into a macOS Photos album."""
    photoscript = _require('photoscript')
    import photoscript as ps

    print(f"\n  📲 Importing {len(file_paths)} photos into Photos album '{album_name}'...")
    photos_app = ps.PhotosLibrary()
    photos_app.activate()

    # Create or get the album
    try:
        album = photos_app.album(album_name)
    except Exception:
        album = None
    if album is None:
        album = photos_app.create_album(album_name)

    imported = []
    for fp in file_paths:
        try:
            photo = photos_app.import_photos([str(fp)], skip_duplicate_check=True)
            if photo:
                album.add([photo[0]])
                imported.append(fp)
        except Exception as e:
            print(f"  ⚠️  Failed to import {Path(fp).name}: {e}")

    print(f"  ✅ Imported {len(imported)} photos into '{album_name}'")
    return imported


# ===========================================================================
#  MAIN PIPELINE
# ===========================================================================

def process_photos(
    source='folder',
    input_folder=None,
    album_name=None,
    output_folder=None,
    output_to_photos=False,
    output_album='Stamped Photos',
    limit=None,
):
    """Main processing pipeline."""

    tmp_dir = None
    photo_items = []  # list of (filepath, date_taken, lat, lon)

    # ── Collect photos ──
    if source == 'photos':
        tmp_dir, photo_items = collect_from_photos_app(album_name=album_name, limit=limit)
    else:
        paths = collect_from_folder(input_folder)
        for p in paths:
            date_taken, lat, lon = extract_metadata_exif(str(p))
            photo_items.append((p, date_taken, lat, lon))

    if not photo_items:
        print("❌  No photos to process.")
        return

    print(f"\n  🔄 Processing {len(photo_items)} photo(s)...\n")

    # ── Prepare output folder ──
    if output_folder:
        out_dir = Path(output_folder)
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = Path(input_folder or '.') / 'stamped_output'
        out_dir.mkdir(parents=True, exist_ok=True)

    stamped_paths = []
    for i, (filepath, date_taken, lat, lon) in enumerate(photo_items, 1):
        name = Path(filepath).stem
        ext = Path(filepath).suffix or '.jpg'
        # Convert HEIC → JPEG for output
        if ext.lower() == '.heic':
            ext = '.jpg'
        out_path = out_dir / f"{name}_stamped{ext}"

        # Reverse geocode
        location_text = reverse_geocode(lat, lon) if (lat and lon) else None

        # Format date
        date_text = None
        if date_taken:
            date_text = date_taken.strftime('%B %d, %Y  •  %I:%M %p').replace('  •  0', '  •  ')

        status_parts = []
        if location_text:
            status_parts.append(location_text)
        if date_text:
            status_parts.append(date_text)
        status = ' | '.join(status_parts) if status_parts else 'no metadata'

        print(f"  [{i}/{len(photo_items)}] {Path(filepath).name}")
        print(f"           → {status}")

        success = stamp_photo(str(filepath), str(out_path), location_text, date_text)
        if success:
            stamped_paths.append(out_path)
        else:
            print(f"           ⚠️  No location or date found — copied as-is")

    # ── Import to Photos if requested ──
    if output_to_photos and stamped_paths:
        import_to_photos_album(stamped_paths, album_name=output_album)

    # ── Cleanup temp dir ──
    if tmp_dir and os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n  ✅ Done! {len(stamped_paths)} stamped photo(s) saved to: {out_dir}")
    if output_to_photos:
        print(f"  ✅ Also imported into Photos album: '{output_album}'")
    print()


# ===========================================================================
#  CLI
# ===========================================================================

def interactive_mode():
    """Run the script interactively with prompts."""
    print("\n" + "=" * 60)
    print("  📸  Photo Stamper  —  Add location & date to your photos")
    print("=" * 60)

    # ── Input source ──
    print("\n  Where are your photos?")
    print("    1. macOS Photos app (pick an album)")
    print("    2. A local folder")
    choice = input("\n  Choose [1/2]: ").strip()

    source = 'photos' if choice == '1' else 'folder'
    input_folder = None
    album_name = None

    if source == 'folder':
        input_folder = input("  Enter folder path: ").strip()
        input_folder = os.path.expanduser(input_folder)
    # For 'photos', album selection happens inside collect_from_photos_app()

    # ── Output ──
    print("\n  Where should stamped photos go?")
    print("    1. A local folder")
    print("    2. macOS Photos album")
    print("    3. Both")
    out_choice = input("\n  Choose [1/2/3]: ").strip()

    output_folder = None
    output_to_photos = out_choice in ('2', '3')

    if out_choice in ('1', '3'):
        output_folder = input("  Enter output folder path (or press Enter for default): ").strip()
        if not output_folder:
            output_folder = None  # Will use default
        else:
            output_folder = os.path.expanduser(output_folder)
    elif out_choice == '2':
        # Still need a temp folder for processing
        output_folder = tempfile.mkdtemp(prefix='photo_stamper_out_')

    output_album = 'Stamped Photos'
    if output_to_photos:
        custom_album = input("  Photos album name [Stamped Photos]: ").strip()
        if custom_album:
            output_album = custom_album

    # ── Go! ──
    process_photos(
        source=source,
        input_folder=input_folder,
        album_name=album_name,
        output_folder=output_folder,
        output_to_photos=output_to_photos,
        output_album=output_album,
    )


def main():
    parser = argparse.ArgumentParser(
        description='📸 Photo Stamper — Overlay location & date on your photos',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (recommended for first use)
  python3 photo_stamper.py

  # Process a local folder → local output
  python3 photo_stamper.py --source folder --input ~/Photos/Vacation --output ~/Photos/Stamped

  # Process a Photos album → Photos album
  python3 photo_stamper.py --source photos --album "Summer 2024" --to-photos --output-album "Stamped Summer"

  # Process a folder → both local output AND Photos album
  python3 photo_stamper.py --source folder --input ./pics --output ./stamped --to-photos
        """,
    )
    parser.add_argument('--source', choices=['folder', 'photos'], help='Input source')
    parser.add_argument('--input', '-i', dest='input_folder', help='Input folder path')
    parser.add_argument('--album', '-a', help='Photos app album name')
    parser.add_argument('--output', '-o', dest='output_folder', help='Output folder path')
    parser.add_argument('--to-photos', action='store_true', help='Also import into Photos app')
    parser.add_argument('--output-album', default='Stamped Photos', help='Photos album for output')
    parser.add_argument('--limit', type=int, help='Max number of photos to process')

    args = parser.parse_args()

    # If no source specified, go interactive
    if not args.source:
        interactive_mode()
        return

    if args.source == 'folder' and not args.input_folder:
        parser.error("--input is required when --source is 'folder'")

    process_photos(
        source=args.source,
        input_folder=args.input_folder,
        album_name=args.album,
        output_folder=args.output_folder,
        output_to_photos=args.to_photos,
        output_album=args.output_album,
        limit=args.limit,
    )


if __name__ == '__main__':
    main()
