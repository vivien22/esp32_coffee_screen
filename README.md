# esp32_coffee_screen: electronics design

Carrier board that moves the espresso machine (firmware: [coffee_screen](https://github.com/vivien22/coffee_screen)) from an Arduino Nano to an **ESP32-S3 Nano (N16R8)**, inside the existing plastic enclosure.

Status: **working design, nothing has been manufactured.** Placement is to scale, but track routing still has to be done in a CAD tool.

## Contents
- `docs/carrier_spec.md`: full specification (dimensions, connectors, pin assignment, circuits, bill of materials, open points).
- `images/carrier_plan.png`: to-scale top-view placement inside the enclosure (**current**).
- `images/box_iso3.png`: 3D view of the enclosure with the board (**outdated**: still shows the old 2 x 8 Dupont block, no J7/J8/J9).
- `images/carrier_schema.png`: connection schematic (**outdated**: old J2 2 x 8 layout, no J8/J9).
- `tools/`: Python (Pillow) scripts that generate the images; the measurements are at the top of each file.

## Principles
- 58 x 68 mm board in the 60 x 70 mm free area, on four 3 mm standoffs (45 x 50 mm spacing), 25 mm usable depth.
- Through-hole parts only (no SMD soldering).
- ESP32-S3 and MAX31865 module on sockets; FPC adapter board (remote display) on a 2 x 4 socket.
- SSRs are kept, driven by 2N2222A transistors from the external 5 V supply.
- Connectors: J2 2 x 4 (5 V + 3 SSRs), J7 1 x 6 (button + encoder, 5 V), J8 1 x 4 (pump dimmer, I2C), J9 1 x 3 (pressure sensor), 2 x JST XH 3-pin (flow sensors).

## To confirm before manufacturing
See the end of `docs/carrier_spec.md`.
