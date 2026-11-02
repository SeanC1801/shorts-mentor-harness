# Reusable asset library plan

Store creator-owned layered originals and derived exports by stable asset ID in `characters/`, `backgrounds/`, and `props/`. Keep source and export names predictable; never overwrite originals. Add each file to `asset-manifest.json` with type, ID, path, dimensions, layers/alpha, provenance/licence, creator approval version, and notes. Cutout characters and printed props are rasterized to transparent PNG cards (`renderer-blender/scripts/rasterize.py`) for the Blender pipeline. No art is stored yet.
