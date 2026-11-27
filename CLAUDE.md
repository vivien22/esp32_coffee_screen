# CLAUDE.md

Carrier board for an ESP32-S3 N16R8 that controls an Ascaso Steel Uno Pro espresso machine (firmware in the separate repository `vivien22/coffee_screen`). Nothing is manufactured yet: this repository holds the design documents only.

## Read first
- `docs/carrier_spec.md`: the specification (dimensions, connectors, pins, circuits, bill of materials, firmware notes, points to confirm).
- `docs/decisions.md`: why each choice was made, and what was rejected. Do not reopen a declined option without a new reason.
- `docs/order_farnell.md`: parts list with Farnell order codes.

## Files
- `tools/board_placement.py`, `tools/board_schematic.py`, `tools/enclosure_overview.py`: Python + Pillow (+ numpy) scripts that draw `images/board_placement.png`, `images/board_schematic.png` and `images/enclosure_overview.png`. Coordinates are in mm, board origin at the back-left corner of the main body, y towards the front.
- The scripts load `C:/Windows/Fonts/arial.ttf` / `arialbd.ttf`. On Linux, run a copy with the font path replaced (for example `/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf` / `-Bold.ttf`) and copy the PNG back to `images/`.

## Rules
- The user (Vivien) writes in French; the documents and scripts are in English.
- Any change must stay consistent across the spec, the three scripts and the three images: regenerate the images and look at them before committing.
- After moving pads, check pad clearances (a gap under about 0.3 mm between two pads is a defect).
- Commit locally. **Push only when Vivien writes "pousse"**; an automatic message about unpushed commits is not an approval.
