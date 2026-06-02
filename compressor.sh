#!/usr/bin/env bash
set -euo pipefail

IMGS_DIR="static/imgs"

if [ ! -d "$IMGS_DIR" ]; then
    echo "[compressor] no $IMGS_DIR directory, skipping."
    exit 0
fi

mapfile -t images < <(find "$IMGS_DIR" -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) | sort)

if [ ${#images[@]} -eq 0 ]; then
    echo "[compressor] no images found in $IMGS_DIR, skipping."
    exit 0
fi

echo "[compressor] found ${#images[@]} image(s) to process..."

converted=0
skipped=0

for img in "${images[@]}"; do
    webp="${img%.*}.webp"

    # Skip if webp already exists and is newer than source
    if [ -f "$webp" ] && [ "$webp" -nt "$img" ]; then
        echo "  [skip]    $img"
        ((skipped++)) || true
        continue
    fi

    echo "  [convert] $img -> $webp"
    cwebp -q 80 -quiet "$img" -o "$webp"
    ((converted++)) || true
done

echo "[compressor] done: $converted converted, $skipped skipped."
