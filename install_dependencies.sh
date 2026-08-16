#!/bin/bash
# ─────────────────────────────────────────────────
#  Photo Stamper — Dependency Installer
# ─────────────────────────────────────────────────
set -e

echo ""
echo "📸  Photo Stamper — Installing dependencies..."
echo "─────────────────────────────────────────────"

# Check Python 3
if ! command -v python3 &>/dev/null; then
    echo "❌  Python 3 is required. Install it from https://python.org or via Homebrew:"
    echo "    brew install python"
    exit 1
fi

echo "✅  Python 3 found: $(python3 --version)"

# Install packages
echo ""
echo "📦  Installing Python packages..."
pip3 install \
    Pillow \
    osxphotos \
    photoscript \
    reverse_geocoder \
    pilmoji \
    exifread \
    --break-system-packages 2>/dev/null || \
pip3 install \
    Pillow \
    osxphotos \
    photoscript \
    reverse_geocoder \
    pilmoji \
    exifread

echo ""
echo "✅  All dependencies installed!"
echo ""
echo "Run the stamper with:"
echo "    python3 photo_stamper.py"
echo ""
