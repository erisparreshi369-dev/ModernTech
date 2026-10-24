#!/usr/bin/env bash
# Build clean, upload-ready copies of the three ModernTech packages in dist/.
# The in-game Workshop uploader sends a mod's whole folder, so upload these
# copies instead of the development folder (which also holds .git, tools, extras).
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
dist="$root/dist"
python3 -I "$root/tools/check_tyd.py"

rm -rf "$dist"
mkdir -p "$dist"
rsync -a --exclude='.git*' --exclude=tools --exclude=extras --exclude=dist --exclude=README.md --exclude=LICENSE \
	"$root/" "$dist/ModernTech/"
rsync -a "$root/extras/Furniture/ModernTech PCs/" "$dist/ModernTech PCs/"
rsync -a --exclude='*.dcache' --exclude='*H.bin' "$root/extras/DLLMods/ModernTechDemand/" "$dist/ModernTechDemand/"
for pkg in "$dist"/*/; do
	cp "$root/LICENSE" "$pkg/LICENSE.txt"
done

# The uploader refuses any file whose extension isn't on the mod type's GetValidExts() list.
check() {
	bad=$(find "$dist/$1" -type f | grep -viE "\.($2)\$" || true)
	[ -z "$bad" ] || { printf 'Workshop uploader would reject:\n%s\n' "$bad"; exit 1; }
}
check ModernTech 'txt|xml|png|tyd|gltf|glb|obj'
check 'ModernTech PCs' 'xml|png|obj|txt|tyd'
check ModernTechDemand 'cs|jpg|jpeg|png|txt|tyd|ogg|mp3|wav|obj|gltf|glb'

du -sh "$dist"/*
