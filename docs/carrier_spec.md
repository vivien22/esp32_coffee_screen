# ESP32-S3 carrier board: specification (working version)

All **through-hole** parts (no SMD soldering). Related files: `images/carrier_plan.png` (to-scale placement), `images/box_iso3.png` (3D view, outdated), `images/carrier_schema.png` (connection schematic, outdated: to be regenerated for J2 / J7 / J8 / J9).

## Dimensions and mounting
- Board: **58 x 68 mm**, two layers, ground plane. Free area in the enclosure: 60 x 70 mm between the large posts.
- 4 mounting holes on the **3 mm** small posts, **45 x 50 mm** spacing.
- Usable depth **25 mm**: posts 3 + board 1.6 = 4.6 mm; ESP32 on 8.5 mm sockets (USB-C at 17.9 mm); FPC adapter board on 8.5 mm sockets (17.7 mm); MAX31865 on low 3 mm sockets (22.6 mm, 2.4 mm margin).
- No copper and no component under the ESP32 antenna (the end of the ESP32 board opposite the USB-C).

## Connectors
| Ref | Type | Role |
|---|---|---|
| J2 | 2 x 4 right-angle male header, female Dupont housings | 5 V supply + 3 SSRs |
| J3, J4 | JST XH 3-pin (real pitch 2.5 mm) | flow sensors In and Out |
| J5 | 2 x 4 female socket | FPC adapter board (8 pins, ribbon to the remote display) |
| J6 | 1 x 8 female socket (low, 3 mm) | MAX31865 module |
| J7 | 1 x 6 right-angle male header | button + encoder (encoder powered from 5 V) |
| J8 | 1 x 4 header | RobotDyn 4 A pump dimmer, **I2C** (powered from 3.3 V) |
| J9 | 1 x 3 header | pressure sensor 0.5 to 4.5 V, 0 to 12 bar (powered from 5 V) |
| ESP | 2 x 1 x 20 female sockets | ESP32-S3 board (row spacing to be measured) |

### J2 (2 x 4: row A on top, row B at the bottom, pin 1 on the left)
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| A | +5 V | pump + | boiler + | valve + |
| B | GND | pump − | boiler − | valve − |

Four 2-pin Dupont housings (one per column). Warning: a 2 x 4 header is not keyed and a 2-pin housing can be plugged the wrong way round; mark the wires (red on row A) or add a key / use a keyed housing.

### J7 (1 x 6)
| 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| button (GPIO 6) | GND | **+5 V** | GND | enc. A (GPIO 4) | enc. B (GPIO 5) |

Housings: 2-pin (button) and 4-pin (encoder: +5 V, GND, A, B). The wire order must follow **your** encoder module (to be checked).

### 5 V inputs protection (encoder)
The ESP32-S3 only accepts 3.3 V. Since the encoder module is powered from 5 V, its outputs (A, B, button) can reach 5 V if the module has pull-ups to 5 V. Each signal therefore goes through a divider: 4.7 kΩ in series to the GPIO, then 10 kΩ from the GPIO to GND (5 V becomes 3.4 V). The 10 kΩ pull-ups to 3.3 V (R9, R10) are then removed. **To check:** if your module is a bare encoder without pull-up resistors, 10 kΩ pull-ups to 5 V are needed (provide optional footprints).

### J8 (pump dimmer, 1 x 4, in the module's order)
| 1 | 2 | 3 | 4 |
|---|---|---|---|
| VCC (3.3 V) | GND | SDA | SCL |

RobotDyn "4 A Dimmer, DimmerLink UART / I2C interface" module (53 x 16 mm): no zero-cross pin and no PWM, everything goes through the bus. **Selected mode: I2C**, GPIO 47 = SDA, GPIO 48 = SCL (**provisional**). Provide two 4.7 kΩ pull-ups to 3.3 V on SDA and SCL (fitted only if the module has none). The module stays off the board, on the mains side: only the control cable comes back, and the 230 V part keeps its own insulation and clearances. Powered from 3.3 V so the logic level matches the ESP32.

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

## ESP32-S3 pins
5V, 3V3, GND; GPIO 17 (pump SSR), 18 (boiler SSR), 21 (valve SSR); 15 (flow In), 16 (flow Out); 4 / 5 (encoder); 6 (button); 11 / 12 / 13 (SPI MOSI / SCK / MISO); 10 (display CS); 9 / 8 (display DC / RST); 14 (backlight); 7 (MAX31865 CS); 47 / 48 (dimmer, I2C SDA / SCL); 1 (pressure, ADC); 38 (spare). Avoided: 0, 3, 45, 46, 19, 20, 35 to 37.

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
| 1 | right-angle 2 x 4 male header + right-angle 1 x 6 + 1 x 4 + 1 x 3 | 0.7 € |
| 2 | JST XH 3-pin headers | 0.5 € |
| 4 | 2N2222A transistors (3 SSRs + backlight) | 0.6 € |
| ~20 | axial resistors (1 kΩ, 10 kΩ, 4.7 kΩ, 20 kΩ; to be recounted at routing) | 1 € |
| 1 | 1.1 A resettable fuse (radial) | 0.5 € |
| 1 | 1N5819 diode | 0.2 € |
| 1 | 470 µF 10 V radial capacitor; 4 x 100 nF; 2 x 1 nF | 1 € |
| 4 | 3 mm standoffs (existing) + M2.5 screws | 0 |
| | **Total parts** | **about 6 to 9 €** |
| 5 | bare boards, 58 x 68 mm, 2 layers (shipping included) | 10 to 20 € |

## Points to confirm before manufacturing
1. Pin order, supply and backlight of your display ribbon (J5).
2. Pin order of your encoder, and whether it has pull-up resistors.
3. Pin spacing (rows and pitch) and true width of your ESP32-S3 board.
4. Dimensions of your FPC adapter board (about 22 x 26 mm estimated) and position of its mounting holes.
5. Flow sensor output type (5 V or open collector): the planned circuit suits both.
6. MAX31865 module (Adafruit, measured from the manufacturer's drawing): 25.4 x 27.9 mm, mounting holes 0.9" apart and 0.1" from the terminal-block edge, 1 x 8 header at 0.1" pitch on the short edge.
7. Pump dimmer: I2C address, registers and timing from the DimmerLink datasheet; I2C pull-ups present or not on the module.
8. Pressure sensor: confirm 3 wires (+5 V, GND, signal) and the G1/4 fitting on the hydraulic circuit.
9. One mounting hole (top right) passes under the MAX31865: flat-head screw, 1.5 mm high at most, under the module's 3 mm.
