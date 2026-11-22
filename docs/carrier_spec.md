# ESP32-S3 carrier board: specification (working version)

All **through-hole** parts (no SMD soldering). Related files: `images/placement_plan.png` (to-scale placement), `images/enclosure_view.png` (3D view), `images/connection_schematic.png` (connection schematic).

## Dimensions and mounting
- Enclosure interior (measured): **60 mm wide x 85 mm long**. The four big posts are round, **8 mm in diameter** (8 x 8 mm footprint), in the corners. The small posts (3 mm high) are at **45 x 50 mm**, centred.
- The posts leave a plus-shaped usable area: **60 x 69 mm** between the posts along the long sides (y from 8 to 77) and **44 mm wide over the full 85 mm length** between the end posts.
- Board: **58 x 68 mm main body** (0.5 to 1 mm of margin all round) **plus a 42 x 7 mm tab on the cable (front) side**, so the board is 75 mm long at the tab; two layers, ground plane. The tab lets the Dupont housings of J2 / J7 and the JST XH plugs sit on the board up to the front wall; the back extension (same size) is not used.
- 4 mounting holes on the **3 mm** small posts, **45 x 50 mm** spacing, centred in the interior (board coordinates (6.5, 9), (51.5, 9), (6.5, 59), (51.5, 59)).
- Usable depth **25 mm**: posts 3 + board 1.6 = 4.6 mm; ESP32 on 8.5 mm sockets (USB-C at 17.9 mm); FPC adapter board on 8.5 mm sockets (17.7 mm); MAX31865 on low 3 mm sockets (22.6 mm, 2.4 mm margin).
- **ESP32-S3 rotated 90 degrees** (long side across the board, at the back, y 3 to 25 mm): **USB-C towards the left wall**, with an opening in that wall at y 9 to 19 mm (the connector is then far from the 8 mm corner posts). The antenna end is on the right (x 48.5 to 56.5 mm).
- **Under the ESP32 (between the two socket rows, 8.5 mm clearance):** vertical axial resistors R1 to R10, then Q1 to Q4 on the right; Q5 (spare output) at the left, next to the USB end. The two small standoffs at the back (6.5, 9) and (51.5, 9) are under the ESP32; the one on the right is under the antenna, so use a **non-plated hole with no copper ring** there.
- **Below the ESP32, side by side:** the FPC adapter board on the **left** (x 1.5 to 23.5 mm, connector towards the front, flow-input parts R11 to R16 and C3, C4 under it), the MAX31865 on the **right** (x 31 to 56.4 mm, rotated 180 degrees: header on its rear edge, pin 1 VIN on the right, PT100 terminal block facing the front), and a corridor between them (x 23.5 to 31 mm) holding J8, J9, C1 and C2.
- **Front connector row:** right-angle headers with their Dupont housings need about **9 mm in front of the pads** (keep-out, nothing else there); J2 and J7 are on the 42 x 7 mm tab, the vertical JST XH J3 and J4 at the front right, F1 and D1 in the front-left corner. A cable slot is needed in the front wall (housings end about 1 mm from it).
- **All cables leave through the front** (J2, J7, J3, J4, the PT100 wires and the display ribbon). Only the USB-C cable leaves through the left wall.
- **Display ribbon:** the FPC adapter board is rotated so that its connector faces the front: the flat ribbon (about 6 mm wide, at about 15.5 mm) runs **straight to the front** between x 7 and 18 mm, above J2's housings (10.5 mm) and F1; no tall part (JST XH plugs reach about 16 mm) may sit in that column. Nothing crosses the MAX31865 any more.
- **Cables:** small flat ribbons (Dupont wires side by side), about **1.5 mm per wire** (4 wires = 6 mm, 3 wires = 4.5 mm, 2 wires = 3 mm), 1.3 mm thick. In the 3D view the cables are numbered 1 to 9 (J2 x2, J7 x3, J3, J4, PT100 probe, display ribbon); J3 / J4 leave their plugs upwards at about 12 mm and the two thin PT100 wires (0.8 mm, on the two middle terminals of the MAX31865 block) at about 15 mm; all go through the front slot. **J8 (pump dimmer) and J9 (pressure sensor) are provisioned on the board but not plugged for now**: they are shown as bare headers, and their cables (4 wires = 6 mm, 3 wires = 4.5 mm) are not counted in the slot width.
- The spare-I/O resistors R17 to R21 are flat resistors under the MAX31865 (3 mm clearance, enough for axial 1/4 W parts).
- No copper and no component under the ESP32 antenna (the end of the ESP32 board opposite the USB-C).

## Connectors
| Ref | Type | Role |
|---|---|---|
| J2 | 2 x 4 right-angle male header, one 2 x 4 female Dupont housing (two ribbons of 4 wires) | 5 V supply + 3 SSRs |
| J3, J4 | JST XH 3-pin, vertical, rotated (real pitch 2.5 mm) | flow sensors In and Out |
| J5 | 2 x 4 female socket | FPC adapter board (8 pins, ribbon to the remote display) |
| J6 | 1 x 8 female socket (low, 3 mm) | MAX31865 module |
| J7 | 2 x 6 right-angle male header | button + encoder (encoder powered from 5 V) + 4 spare I/O pins (+5 V, level-adapted input, level-adapted output, GND) |
| J8 | 1 x 4 header | RobotDyn 4 A pump dimmer, **I2C** (powered from 3.3 V) |
| J9 | 1 x 3 header | pressure sensor 0.5 to 4.5 V, 0 to 12 bar (powered from 5 V) |
| ESP | 2 x 1 x 20 female sockets | ESP32-S3 board (about 22 x 54 mm from the photo; row spacing to be measured) |

### J2 (2 x 4: row A on top, row B at the bottom, pin 1 on the left)
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| A | +5 V | GND | pump + | pump − |
| B | boiler + | boiler − | valve + | valve − |

**One 2 x 4 Dupont housing**, two ribbons of 4 wires (one per row): ribbon 1 = 5 V supply and pump SSR, ribbon 2 = boiler SSR and valve SSR. Warning: an unkeyed 2 x 4 housing can be plugged 180 degrees the wrong way round (+5 V would land on the valve SSR "−" input and so on). Use a **keyed (shrouded) 2 x 4 IDC-style header** with its notch, or at least mark the housing and the header.

### J7 (2 x 6, right-angle: two stacked rows of Dupont housings)
| | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Row A (upper) | button (GPIO 6) | GND | **+5 V** | **IN (GPIO 38)** | **OUT (GPIO 39)** | **GND** |
| Row B (lower) | +5 V | GND | enc. A (GPIO 4) | enc. B (GPIO 5) | not used | not used |

Housings: row A = 2-pin (button) + 4-pin (**spare I/O: +5 V, IN, OUT, GND**); row B = 4-pin (encoder: +5 V, GND, A, B). The wire order must follow **your** encoder module (to be checked). Stacking the spare pins above the encoder, rather than extending the row to the right, keeps J7 only about 17 mm wide, so it does not run into J3 / J4.

**Spare IN (GPIO 38), 5 V to 3.3 V:** 4.7 kΩ in series (R17) to the GPIO and 10 kΩ from the GPIO to GND (R18): a 5 V signal becomes 3.4 V. Input only. For a 3.3 V source, replace R17 by a 0 Ω link and leave R18 out (the divider would give only 2.2 V, below the input-high threshold of about 2.5 V).

**Spare OUT (GPIO 39), 3.3 V to 5 V, inverting:** GPIO 39 → 1 kΩ (R19) → base of a 2N2222A (Q5); 10 kΩ from the base to GND (R21, keeps the output idle at boot); the collector is the OUT pin, pulled up to +5 V by 4.7 kΩ (R20); emitter to GND. GPIO high gives OUT low, GPIO low gives OUT at 5 V: invert the logic in the firmware. It can sink up to about 100 mA, but sources only about 1 mA (the pull-up): for a load, drive a relay or transistor from it. A non-inverting alternative is a 2N7000 / BS170 level shifter (gate on 3.3 V, 10 kΩ pull-ups on both sides), not fitted.

The two GPIO numbers (38 and 39) are provisional free GPIOs of the ESP32-S3 chip (neither strapping, PSRAM, flash nor USB); check them against the real pin table of your board, which does not necessarily expose every GPIO of the chip.

### 5 V inputs protection (encoder)
The ESP32-S3 only accepts 3.3 V. Since the encoder module is powered from 5 V, its outputs (A, B, button) can reach 5 V if the module has pull-ups to 5 V. Each signal (A, B, button and the spare GPIO 38) therefore goes through a divider: 4.7 kΩ in series to the GPIO, then 10 kΩ from the GPIO to GND (5 V becomes 3.4 V). The 10 kΩ pull-ups to 3.3 V (R9, R10) are then removed. **To check:** if your module is a bare encoder without pull-up resistors, 10 kΩ pull-ups to 5 V are needed (provide optional footprints).

### J8 (pump dimmer, 1 x 4, in the module's order)
| 1 | 2 | 3 | 4 |
|---|---|---|---|
| VCC (3.3 V) | GND | SDA | SCL |

RobotDyn "4 A Dimmer, DimmerLink UART / I2C interface" module (53 x 16 mm): no zero-cross pin and no PWM, everything goes through the bus. Reference code and documentation: https://github.com/robotdyn-dimmer/DimmerLink. Powered from 3.3 V (the module accepts 1.8 / 3.3 / 5 V and its logic follows VCC, so no level converter); 100 nF decoupling near the module. **Selected mode: I2C**, GPIO 47 = SDA, GPIO 48 = SCL (**provisional**).

**Important: the module ships in UART mode.** It must be switched to I2C once, by sending the UART frame `02 5B` (SWITCH_I2C) to it; the same two pins are then SDA / SCL. Plan a one-time switch (temporary UART sketch on GPIO 47 / 48, or a USB-serial adapter on J8) before using I2C. Going back to UART is done by writing `0x03` to the COMMAND register.

I2C summary (from the DimmerLink documentation, version 1.0):
- Address **0x50** (7-bit), changeable through register 0x30 (0x08 to 0x77, saved to EEPROM). Speed **100 kHz**.
- Pull-ups: **4.7 kΩ to 3.3 V on SDA and SCL** (the ESP32 internal ones are too weak): fit them on the board (R-SDA, R-SCL). Keep the cable under 30 cm.
- Registers: 0x00 STATUS (bit 0 ready, bit 1 error), 0x01 COMMAND (1 reset, 2 recalibrate, 3 switch to UART), 0x02 ERROR, 0x03 VERSION, **0x10 DIM0_LEVEL (0 to 100 %, read/write)**, 0x11 DIM0_CURVE (0 linear, 1 RMS, 2 log), 0x20 AC_FREQ (50 or 60), 0x21 / 0x22 AC_PERIOD (µs, half-wave), 0x23 CALIBRATION (1 = done).
- Resolution is 1 % steps, and mains frequency is detected automatically. Use the linear curve for the pump.
- Not stated in the documentation: power-on delay, EEPROM write time, maximum load, mains isolation. Wait a few hundred ms after power-up and poll STATUS bit 0 (ready) before the first write.

**Warning (from the DimmerLink FAQ):** it lists induction / asynchronous motors, "most fans, pumps", as unsuitable (they hum and overheat); it does not mention vibration pumps. The Olab pump is a vibration pump (a solenoid coil with a piston, not an induction motor), a type commonly dimmed with this kind of module, but this is not covered by the documentation: test it carefully (monitor the pump temperature and noise) and keep the pump SSR as an independent cut-off. An RC snubber on the dimmer output is suggested by the FAQ if the mains interferes.

The module stays off the board, on the mains side: only the control cable comes back, and the 230 V part keeps its own insulation and clearances.

Pump: Olab Silent Green K09541 / K09541L (datasheet): self-priming vibration pump, 35 W class F coil, available in 230 V / 50 Hz or 120 V / 60 Hz (check the label of yours), water 5 to 35 °C, brass or plastic outlet. Pressure-flow curve (±15 %): about 19 bar at zero flow, 13 bar at 100 cm³/min, 3.5 bar at 300 cm³/min, 0 bar at about 420 cm³/min. Phase-angle dimming is a common practice on this type of pump. The dimmer goes in series with the pump; keep the pump SSR in series as a hard cut-off (the dimmer alone does not guarantee a complete stop). At low power the pump may vibrate without pumping: provide a minimum setting, to be calibrated with the pressure sensor. 35 W (about 0.15 A at 230 V) is far below the 4 A rating of the dimmer.

### J9 (pressure sensor, 1 x 3)
| 1 | 2 | 3 |
|---|---|---|
| +5 V | GND | signal |

G1/4 sensor, 0 to 12 bar, 0.5 to 4.5 V output. The signal goes through a divider, 10 kΩ (series) / 20 kΩ (to GND), which brings 4.5 V down to 3.0 V, plus 100 nF on GPIO 1 (ADC1, 11 dB attenuation). Pressure in bar = (sensor voltage − 0.5) x 3. Average the readings (the ESP32 ADC is noisy and not very linear at the ends). The pump can reach about 19 bar at zero flow, above the sensor's 12 bar range: make sure the machine's pressure relief valve limits the pressure at the sensor tap (and check the sensor's overpressure rating).

### J3 / J4 (JST XH 3-pin)
1 = +5 V, 2 = signal, 3 = GND. The exact order comes from the sensor cable (often red / yellow / black).

### J5 (FPC adapter board, your numbering: top row 1 3 5 7, bottom row 2 4 6 8)
**Provisional** assignment (typical 8-pin GC9A01): 1 GND, 2 3V3, 3 SCL (GPIO 12), 4 SDA (GPIO 11), 5 DC (GPIO 9), 6 CS (GPIO 10), 7 RST (GPIO 8), 8 BL (GPIO 14 through a transistor). **To confirm with the display datasheet.** The display is powered from 3.3 V.

### J6 (MAX31865 module)
VIN (3.3 V), 3Vo (unused), GND, CLK (GPIO 12), SDO (GPIO 13), SDI (GPIO 11), CS (GPIO 7), RDY (unused). This is the Adafruit order (VIN, 3Vo, GND, CLK, SDO, SDI, CS, RDY).

## ESP32-S3 board (read on the photo)
Silkscreen read on the photo, left column from the USB-C end: GND, 5V, G48, BOOT, 48, 47, 38, 39, 40, 21, GND, 18, 17, 16, 15, 41, 42, 45, 46. Right column: GND, 3V3, PWR, RST, 14, 13, 12, 11, 10, 09, 08, 07, GND, 06, 05, 04, 03, 02, 01. Every GPIO used in this design (1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 38, 39, 47, 48) is broken out on this board, and the strapping pins to avoid (0 = BOOT, 3, 45, 46) are the ones marked. Still free: 2 (right), 40, 41, 42 (left). To confirm by you: exact board size (the photo suggests about 22 x 54 mm plus about 1.5 mm of USB-C overhang), pin count per side (about 20), and row spacing.

## ESP32-S3 pins
5V, 3V3, GND; GPIO 17 (pump SSR), 18 (boiler SSR), 21 (valve SSR); 15 (flow In), 16 (flow Out); 4 / 5 (encoder); 6 (button); 11 / 12 / 13 (SPI MOSI / SCK / MISO); 10 (display CS); 9 / 8 (display DC / RST); 14 (backlight); 7 (MAX31865 CS); 47 / 48 (dimmer, I2C SDA / SCL); 1 (pressure, ADC); 38 (spare, on J7). Avoided: 0, 3, 45, 46, 19, 20, 35 to 37 (not broken out on this board).

## Circuits
- **Power:** J2 A1 (+5 V) → 1.1 A resettable fuse → 1N5819 diode (reverse protection) → +5 V rail (470 µF + 100 nF) → ESP32 5V pin. The 3.3 V comes from the ESP32 board.
- **SSR (x3):** GPIO → 1 kΩ → 2N2222A base; 10 kΩ base → GND; SSR "+" input to the +5 V rail, "−" input to the collector; emitter to GND. The SSR input receives about 4.8 V.
- **Flow sensor (x2):** signal → 10 kΩ to +5 V; signal → 4.7 kΩ → GPIO; GPIO → 10 kΩ → GND; 1 nF GPIO → GND. Works with a 5 V output (the divider gives about 3.4 V) or with an open collector.
- **Display backlight:** GPIO 14 → 1 kΩ → 2N2222A base; the backlight current flows through the collector (adapt to the display).
- **Encoder / button:** see "5 V inputs protection"; 100 nF against bounce.

## Bill of materials (through-hole)
| Qty | Part | Indicative price |
|---|---|---|
| 1 | ESP32-S3 N16R8 board (owned) | 0 |
| 2 | 1 x 20 female sockets, 8.5 mm | 1 € |
| 1 | MAX31865 module (owned) + low 1 x 8 socket | 0.3 € |
| 1 | 8-pin FPC board (owned) + 2 x 4 male header + 2 x 4 female socket | 0.5 € |
| 1 | right-angle 2 x 4 + right-angle 2 x 6 male headers, 1 x 4 and 1 x 3 male headers | 0.8 € |
| 2 | JST XH 3-pin headers | 0.5 € |
| 5 | 2N2222A transistors (3 SSRs + backlight + spare output) | 0.7 € |
| ~20 | axial resistors (1 kΩ, 10 kΩ, 4.7 kΩ, 20 kΩ; to be recounted at routing) | 1 € |
| 1 | 1.1 A resettable fuse (radial) | 0.5 € |
| 1 | 1N5819 diode | 0.2 € |
| 1 | 470 µF 10 V radial capacitor; 4 x 100 nF; 2 x 1 nF | 1 € |
| 4 | 3 mm standoffs (existing) + M2.5 screws | 0 |
| | **Total parts** | **about 6 to 9 €** |
| 5 | bare boards, 58 x 68 mm + 42 x 7 mm tab, 2 layers (shipping included) | 10 to 20 € |

## Points to confirm before manufacturing
1. Pin order, supply and backlight of your display ribbon (J5).
2. Pin order of your encoder, and whether it has pull-up resistors.
3. Pin spacing (rows and pitch) and true width of your ESP32-S3 board.
4. Dimensions of your FPC adapter board (about 22 x 26 mm estimated) and position of its mounting holes.
5. Flow sensor output type (5 V or open collector): the planned circuit suits both.
6. MAX31865 module (Adafruit, measured from the manufacturer's drawing): 25.4 x 27.9 mm, mounting holes 0.9" apart and 0.1" from the terminal-block edge, 1 x 8 header at 0.1" pitch on the short edge.
7. Pump dimmer: one-time switch from UART to I2C (see J8); behaviour with the vibration pump to test; I2C pull-ups (4.7 kΩ) fitted on the board.
8. Pressure sensor: confirm 3 wires (+5 V, GND, signal) and the G1/4 fitting on the hydraulic circuit.
9. USB-C opening in the left wall (y 9 to 19 mm) and the USB cable bend outside the box.
10. Display ribbon: length, thickness and pin-1 orientation of your FPC adapter board; the column x 7 to 18 mm in front of it must stay free of tall parts.
