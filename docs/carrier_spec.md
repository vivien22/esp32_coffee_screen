# ESP32-S3 carrier board: specification (working version)

All **through-hole** parts (no SMD soldering). Related files: `images/board_placement.png` (to-scale placement), `images/enclosure_overview.png` (3D view), `images/board_schematic.png` (connection schematic).

## Dimensions and mounting
- Enclosure interior (measured): **60 mm wide x 85 mm long**. The four big posts are round, **8 mm in diameter** (8 x 8 mm footprint), in the corners. The small posts (3 mm high) are at **45 x 50 mm**, centred.
- The posts leave a plus-shaped usable area: **60 x 69 mm** between the posts along the long sides (y from 8 to 77) and **44 mm wide over the full 85 mm length** between the end posts.
- Board: **58 x 68 mm main body** (0.5 to 1 mm of margin all round) **plus a 42 x 7 mm tab on the cable (front) side and a 42 x 7 mm tab at the back, behind the ESP32** (x 8 to 50), so the board is 82 mm long at the tabs; two layers, ground plane. The tab lets the Dupont housings of J2 / J7 and the JST XH plugs sit on the board up to the front wall; the back tab holds C1 (470 µF, x 22, y −3.5), C2 (100 nF, x 31, y −3.5), the two 4.7 kΩ I2C pull-ups to 3.3 V R24 / R25 (left of C1) and the two 10 kΩ button pull-ups to 3.3 V R30 / R31 (right of C2), which frees the central corridor; keep it clear of the antenna zone (x 48.5 and beyond).
- 4 mounting holes on the **3 mm** small posts, **45 x 50 mm** spacing, centred in the interior (board coordinates (6.5, 9), (51.5, 9), (6.5, 59), (51.5, 59)).
- Usable depth **25 mm**: posts 3 + board 1.6 = 4.6 mm; ESP32 on 8.5 mm sockets (USB-C at 17.9 mm); FPC adapter board on 8.5 mm sockets (17.7 mm); MAX31865 on low 3 mm sockets (22.6 mm, 2.4 mm margin).
- **ESP32-S3 rotated 90 degrees** (long side across the board, at the back, y 3.5 to 24.5 mm): **USB-C towards the left wall**, with an opening in that wall at y 9 to 19 mm (the connector is then far from the 8 mm corner posts). The antenna end is on the right (x 48.5 to 56.5 mm).
- **Under the ESP32 (between the two socket rows, 8.5 mm clearance):** vertical axial resistors R1 to R10, then Q1 to Q4 on the right, in two rows of two (TO-92 bodies are 4.8 mm wide); every TO-92 (Q1 to Q5) uses a **triangular footprint**: outer legs 2.54 mm apart, middle leg bent 2.54 mm back, 1.6 mm pads (three round pads in line at 1.27 mm would overlap and short the legs); Q5 (spare output) at the left, next to the USB end. C5 and C6 (100 nF, filters of the ADC inputs GPIO 1 and GPIO 2) stand right of Q2 / Q4, at x 46.4, close to the GPIO 1 / 2 pins and just outside the antenna keep-out. The two small standoffs at the back (6.5, 9) and (51.5, 9) are under the ESP32 (screw them before plugging the ESP32 in); the copper ring of the hole at (6.5, 9) is reduced to 4.6 mm, because a 5.6 mm ring comes within 0.26 mm of a pad of the back socket row; the one on the right is under the antenna, so use a **non-plated hole with no copper ring** there, and a **nylon M2.5 screw** (a metal screw right under the antenna detunes it).
- **Connector rows:** J8 is the lowest row of the J2 header; J7 is also a 3 x 4 right-angle strip (row A: start and steam buttons, row B: encoder, row C: spare I/O); each row has its own Dupont housing, rows are 2.54 mm apart vertically, the housings are not keyed: mind the order. J8 and J9 both have their plug and cable. The corridor between the FPC board and the MAX31865 holds D2 (ESP32 supply diode), R28 / R29 (33 Ω, display SPI) and the test points TP1 to TP3.
- **Below the ESP32, side by side:** the FPC adapter board on the **left** (x 1.5 to 23.5 mm, connector towards the front, flow-input parts R11 to R16 and C3, C4 under it), the MAX31865 on the **right** (x 31 to 56.4 mm, rotated 180 degrees: header on its rear edge, pin 1 VIN on the right, PT100 terminal block facing the front), and a corridor between them (x 23.5 to 31 mm) holding D2, R28, R29 and TP1 to TP3.
- **Front connector row:** right-angle headers with their Dupont housings need about **9 mm in front of the pads** (keep-out, nothing else there); J2 and J7 are on the 42 x 7 mm tab, the vertical JST XH J3 and J4 at the front right, F1 in the front-left corner, and the **PWR pads** (5 V supply wires, see Circuits) at the left end of the tab (x 9.4, y 70.6 and 73.1), left of the J2 housings. A cable slot is needed in the front wall (housings end about 1 mm from it).
- **All cables leave through the front** (the 5 V supply wires, J2, J7, J8, J3, J4, J9, the PT100 wires and the display ribbon). Only the USB-C cable leaves through the left wall.
- **Display ribbon:** the FPC adapter board is rotated so that its connector faces the front: the flat ribbon (about 6 mm wide, at about 15.5 mm) runs **straight to the front** between x 7 and 18 mm, above J2's housings (10.5 mm) and F1; no tall part (JST XH plugs reach about 16 mm) may sit in that column. Nothing crosses the MAX31865 any more.
- **Cables:** small flat ribbons (Dupont wires side by side), about **1.5 mm per wire** (4 wires = 6 mm, 3 wires = 4.5 mm, 2 wires = 3 mm), 1.3 mm thick. In the 3D view the cables are numbered 1 to 13 (5 V supply, J2 x2, J7 x4, J8, J3, J4, J9, PT100 probe, display ribbon); J3 / J4 leave their plugs upwards at about 12 mm and the two thin PT100 wires (0.8 mm, on the two middle terminals of the MAX31865 block) at about 15 mm; all go through the front slot. J9 (pressure sensor, 3 wires = 4.5 mm) leaves its plug upwards at about 14 mm, like J3 / J4. J8 (pump dimmer, 4 wires = 6 mm) comes out of the lowest housing of the J2 header, under the two J2 ribbons.
- The spare-I/O resistors R17 to R21, then R22 / R23 (pressure) and R26 / R27 (rail measure) are flat resistors under the MAX31865 (3 mm clearance, enough for axial 1/4 W parts, about 2.5 mm thick). **Check under the PT100 terminal block** (front edge of the module, above R22 to R26): its through-hole leads stick out under the module, often by 1 to 1.5 mm; trim them flush with the solder joints, or put a piece of Kapton tape under the module, or use 1/8 W resistors (about 1.8 mm) there.
- No copper and no component under the ESP32 antenna (the end of the ESP32 board opposite the USB-C). The last socket pads at that end (GPIO 01 / 02 on one row, 45 / 46 on the other) fall in or next to the keep-out: route their traces (GPIO 1 pressure, GPIO 2 rail measure) straight away from the antenna, towards the USB end, and stop the ground plane at x 48.5.

## Connectors
| Ref | Type | Role |
|---|---|---|
| J2 | rows A and B of a **3 x 4 right-angle male header** (one 2 x 4 female Dupont housing; A1 and A2 not connected) | 3 SSRs (pump on row A; boiler, valve on row B) |
| J3, J4 | JST XH 3-pin, vertical, rotated (real pitch 2.5 mm) | flow sensors In (USN-HS06PD) and Out (Digmesa Nano) |
| J5 | 2 x 4 female socket | FPC adapter board (8 pins, ribbon to the remote display) |
| J6 | 1 x 8 female socket (low, 3 mm) | MAX31865 module |
| J7 | a **3 x 4 right-angle male header** | row A: start button + steam-mode button; row B: encoder (powered from **3.3 V**); row C: 4 spare I/O pins (+5 V, level-adapted input, level-adapted output, GND) |
| J8 | row C (the lowest) of the J2 header, 4 pins | RobotDyn 4 A pump dimmer, **I2C** (powered from **3.3 V**, no level shifter) |
| J9 | JST XH 3-pin, vertical, on the tab right under J3 (centre x 38.5, y 71.5) | pressure sensor 0.5 to 4.5 V, 0 to 12 bar (powered from 5 V) |
| PWR | 2 solder pads (+5 V square, GND), 1.0 mm holes (for 0.34 mm² / AWG 22 wire), at the left end of the tab | 5 V supply: two wires soldered to the board, ending in a JST SM 2-pin plug towards the supply |
| D2 | 1N5819 Schottky diode, standing, in the former JP1 pads (square pad = cathode = band, on the ESP32 side) | +5 V board to the 5V pin of the ESP32 (see Circuits) |
| ESP | 2 x 1 x 20 female sockets | ESP32-S3 board (21 mm wide, measured; about 54 mm long; 2 x 20 pins, rows 17.78 mm apart, confirmed) |

### J2 (rows A and B of the 3 x 4 header: row A at the back, row B below it, row C = J8 at the bottom; pin 1 on the left)
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| A | not connected | not connected | pump + | pump − |
| B | boiler + | boiler − | valve + | valve − |

**One 2 x 4 Dupont housing**: ribbon 1 (row A) = pump SSR, 2 wires on A3 / A4 (A1 and A2 stay empty, not connected); ribbon 2 (row B) = boiler SSR and valve SSR. **The 5 V supply no longer goes through J2** (it comes on the PWR pads), so a housing plugged 180 degrees the wrong way only puts the SSR inputs in reverse: nothing switches on, and no supply voltage can reach the ESP32 pins. The remaining risk is a housing pushed **one row too low** (on rows B and C): ribbon 2 would then land on J8 (+3.3 V, GND) and could switch the boiler SSR on. A shrouded (keyed) header is not possible on a 3-row strip: **mark the housing and the header** (a paint dot on A1 on both, and the arrow on the silkscreen).

### J7 (3 x 4 right-angle header: three stacked rows of Dupont housings)
| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Row A (upper) | start button (GPIO 6) | GND | steam button (GPIO 41) | GND |
| Row B (middle) | GA (GPIO 4) | GB (GPIO 5) | **+3.3 V** | GND |
| Row C (lower) | **+5 V** | **IN (GPIO 38)** | **OUT (GPIO 39)** | **GND** |

Housings: row A = two 2-pin (start button, steam-mode button: dry contacts to GND, 10 kΩ pull-ups to 3.3 V on the board, R30 and R31, debounce in firmware); row B = 4-pin (CJMCU-111 encoder, in the module's own order: GA, GB, VCC = **+3.3 V**, GND). The CJMCU-111 module has only these four pins (photo): GA, GB, VCC, GND; its push button is carried by the GA line, so there is no separate push wire (the firmware's encoder library recognises the push from the GA edges, with the 0 Ω hack on the module's push resistor). Row C = 4-pin (**spare I/O: +5 V, IN, OUT, GND**). Three stacked rows keep J7 only about 10 mm wide, so it stays well clear of J3 / J4.

**Spare IN (GPIO 38), 5 V to 3.3 V:** 4.7 kΩ in series (R17) to the GPIO and 10 kΩ from the GPIO to GND (R18): a 5 V signal becomes 3.4 V. Input only. For a 3.3 V source, replace R17 by a 0 Ω link and leave R18 out (the divider would give only 2.2 V, below the input-high threshold of about 2.5 V).

**Spare OUT (GPIO 39), 3.3 V to 5 V, inverting:** GPIO 39 → 1 kΩ (R19) → base of a 2N2222A (Q5); 10 kΩ from the base to GND (R21, keeps the transistor off at boot); the collector is the OUT pin, pulled up to +5 V by 4.7 kΩ (R20); emitter to GND. GPIO high gives OUT low, GPIO low gives OUT at 5 V: invert the logic in the firmware. **At power-up and during a reset, OUT is high (5 V)** until the firmware drives GPIO 39 high: connect only a load that is safe when OUT is high, or that is active-low. It can sink up to about 100 mA, but sources only about 1 mA (the pull-up): for a load, drive a relay or transistor from it. A non-inverting alternative is a 2N7000 / BS170 level shifter (gate on 3.3 V, 10 kΩ pull-ups on both sides), not fitted.

GPIO 38 and 39 are broken out on your board (silkscreen) and are neither strapping, PSRAM, flash nor USB pins.

### Encoder and 5 V input protection
The ESP32-S3 only accepts 3.3 V. **The CJMCU-111 encoder is powered from 3.3 V** (J7 row B, VCC = 3V3). Measured on the module: **6.6 kΩ between GA (or GB) and VCC**, made of 3.3 kΩ resistors (marked on the module): pull-up plus series resistor; the module is passive (mechanical contacts and resistors), so it works at 3.3 V even though its data sheet gives 5 V (4.5 to 5.5 V). With a 5 V supply, these 6.6 kΩ in series with a 4.7 kΩ / 10 kΩ divider would only give about 2.3 V at the GPIO, below the ESP32 input-high threshold (about 2.5 V): that is why the encoder is not powered from 5 V. GA and GB go to GPIO 4 / 5 through **1 kΩ series resistors** (R9, R10, protection only, no divider). The spare GPIO 38 keeps its divider (a real 5 V input): 4.7 kΩ in series to the GPIO, then 10 kΩ from the GPIO to GND (5 V becomes 3.4 V), R17 / R18. **Push button of the knob:** with the 3.3 kΩ pull-up and the module's 3 kΩ push resistor, a push only brings GA down to about 1.6 V, which is not a low level: the **0 Ω hack** (bridge the push resistor, pins 4 and 1 of the encoder) is required for the push to be seen. The start and steam buttons (J7 row A) are dry contacts to GND: no divider, but a **10 kΩ pull-up to 3.3 V** on the board (R30 on GPIO 6, R31 on GPIO 41, on the back tab), because the ESP32 internal pull-up (about 45 kΩ) is too weak for wires running near the pump's 230 V wiring; bounce is handled in the firmware (no capacitor). 

### J8 (pump dimmer, row C of the J2 header, 4 pins in the module's order)
| 1 | 2 | 3 | 4 |
|---|---|---|---|
| VCC (**+3.3 V**) | GND | SDA | SCL |

RobotDyn "4 A Dimmer, DimmerLink UART / I2C interface" module (53 x 16 mm): no zero-cross pin and no PWM, everything goes through the bus. Reference code and documentation: https://github.com/robotdyn-dimmer/DimmerLink. Powered from **+3.3 V** (the 3V3 pin of the ESP32 board). The module accepts 1.8 / 3.3 / 5 V and its logic levels follow VCC, so at 3.3 V it talks directly to the ESP32-S3: **no level shifter**. SDA and SCL each have a **4.7 kΩ pull-up to +3.3 V** on the board (R24, R25, on the back tab). 100 nF decoupling near the module. The module's own consumption on 3.3 V is that of its logic only (the triac side is on the mains); check it once with a multimeter (the ESP32 board regulator, about 500 mA, has enough margin for it). **Selected mode: I2C**, GPIO 47 = SDA, **GPIO 42 = SCL**. GPIO 47 belongs to the VDD_SPI power domain of the ESP32-S3 (data sheet): 3.3 V on your N16R8 (3.3 V flash and PSRAM); it would be 1.8 V on a 1.8 V-flash variant, so keep an N16R8 if the board is ever replaced. GPIO 48 is not used: on this ESP32-S3 board it drives the small LED marked **G48** (next to the USB-C, through a 180 Ω resistor), which would pull SCL down to about 2 to 2.5 V when high, below the input-high threshold (check: blink GPIO 48 in a sketch, the LED next to G48 lights).

**Important: the module ships in UART mode.** It must be switched to I2C once, by sending the UART frame `02 5B` (SWITCH_I2C) to it; the same two pins are then SDA / SCL. Plan a one-time switch (temporary UART sketch on GPIO 47 / 42, or a USB-serial adapter on J8) before using I2C. Going back to UART is done by writing `0x03` to the COMMAND register.

I2C summary (from the DimmerLink documentation, version 1.0):
- Address **0x50** (7-bit), changeable through register 0x30 (0x08 to 0x77, saved to EEPROM). Speed **100 kHz**.
- Pull-ups: 4.7 kΩ to +3.3 V on SDA and SCL (R24, R25); the ESP32 internal ones are too weak. If the module has its own pull-ups, they are now to 3.3 V as well (in parallel, still fine). Keep the cable under 30 cm.
- Registers: 0x00 STATUS (bit 0 ready, bit 1 error), 0x01 COMMAND (1 reset, 2 recalibrate, 3 switch to UART), 0x02 ERROR, 0x03 VERSION, **0x10 DIM0_LEVEL (0 to 100 %, read/write)**, 0x11 DIM0_CURVE (0 linear, 1 RMS, 2 log), 0x20 AC_FREQ (50 or 60), 0x21 / 0x22 AC_PERIOD (µs, half-wave), 0x23 CALIBRATION (1 = done).
- Resolution is 1 % steps, and mains frequency is detected automatically. Use the linear curve for the pump.
- Not stated in the documentation: power-on delay, EEPROM write time, maximum load, mains isolation. Wait a few hundred ms after power-up and poll STATUS bit 0 (ready) before the first write.

**Warning (from the DimmerLink FAQ):** it lists induction / asynchronous motors, "most fans, pumps", as unsuitable (they hum and overheat); it does not mention vibration pumps. The Olab pump is a vibration pump (a solenoid coil with a piston, not an induction motor), a type commonly dimmed with this kind of module, but this is not covered by the documentation: test it carefully (monitor the pump temperature and noise) and keep the pump SSR as an independent cut-off. An RC snubber on the dimmer output is suggested by the FAQ if the mains interferes.

The module stays off the board, on the mains side: only the control cable comes back, and the 230 V part keeps its own insulation and clearances.

Pump: Olab Silent Green K09541 / K09541L (datasheet): self-priming vibration pump, 35 W class F coil, available in 230 V / 50 Hz or 120 V / 60 Hz (check the label of yours), water 5 to 35 °C, brass or plastic outlet. Pressure-flow curve (±15 %): about 19 bar at zero flow, 13 bar at 100 cm³/min, 3.5 bar at 300 cm³/min, 0 bar at about 420 cm³/min. Phase-angle dimming is a common practice on this type of pump. The dimmer goes in series with the pump; keep the pump SSR in series as a hard cut-off (the dimmer alone does not guarantee a complete stop). At low power the pump may vibrate without pumping: provide a minimum setting, to be calibrated with the pressure sensor. 35 W (about 0.15 A at 230 V) is far below the 4 A rating of the dimmer.

### J9 (pressure sensor, JST XH 3-pin, on the tab under J3)
Same order as J3 / J4:

| 1 | 2 | 3 |
|---|---|---|
| +5 V | signal | GND |

The footprint (9.9 x 5.8 mm, pins along x, plug upwards, real pitch 2.5 mm) is centred at x 38.5, y 71.5 mm (J3 at x 38.5 and J4 at x 49, both at y 64.5), inside the 42 x 7 mm tab (y 68 to 75): **only 1.2 mm to J3 and 0.6 mm to the tab edge**, and 1.5 mm from the front wall. Check the plug heights against the cable of J3 (about 12 mm); one more 3-wire cable (4.5 mm) goes through the front slot.

G1/4 sensor, 0 to 12 bar, 0.5 to 4.5 V output. The signal goes through a divider, 10 kΩ (series) / **12 kΩ** (to GND), which brings 4.5 V down to 2.45 V (margin below the top of the ADC range, about 3.1 V, where it is least linear), plus 100 nF on GPIO 1 (ADC1, 12 dB attenuation); on the board: R22 (10 kΩ) and R23 (12 kΩ) flat under the MAX31865 below R21, and C5 (100 nF) under the ESP32, right next to the GPIO 1 pin (x 46.4).

**The sensor is ratiometric** (0.5 to 4.5 V = 10 to 90 % of its supply), and its supply is the board's +5 V rail, which sits at about 5.0 V after F1 (no diode) and moves with the load. The rail is therefore measured on **GPIO 2** through the same 10 kΩ / 12 kΩ ratio (5.0 V gives 2.7 V) (R26, R27, below R23) and the same 100 nF filter (C6, next to C5, by the GPIO 2 pin), and the firmware uses the ratio of the two readings: ratio = ADC(GPIO 1) / ADC(GPIO 2); pressure in bar = (ratio − 0.1) / 0.8 x 12. This cancels the rail variations. Average the readings (the ESP32 ADC is noisy and not very linear at the ends). The pump can reach about 19 bar at zero flow, above the sensor's 12 bar range: make sure the machine's pressure relief valve limits the pressure at the sensor tap (and check the sensor's overpressure rating).

### J3 / J4 (JST XH 3-pin)
1 = +5 V, 2 = signal, 3 = GND. The exact order comes from the sensor cable (often red / yellow / black). J3, J4 and J9 have the same pinout: plugging a sensor into the wrong one of the three is harmless (only the firmware reading is wrong).

### J5 (FPC adapter board, your numbering: top row 1 3 5 7, bottom row 2 4 6 8)
Read on the photo of the display module (1.28" round TFT V1.0, GC9A01, 240 x 240, active diameter 32.4 mm): its 8-pin FPC connector J1 is silkscreened, from left to right, **BLK, CS, DC, RES, SDA, SCL, VCC, GND**. Assuming a straight ribbon and an adapter that maps FPC pin n to header pin n:

| | 1 | 3 | 5 | 7 |
|---|---|---|---|---|
| top row | BLK (GPIO 14) | DC (GPIO 9) | SDA = MOSI (GPIO 11) | VCC (+3.3 V) |

| | 2 | 4 | 6 | 8 |
|---|---|---|---|---|
| bottom row | CS (GPIO 10) | RES (GPIO 8) | SCL = SCK (GPIO 12) | GND |

SDA and SCL are the SPI data and clock (write-only, the display has no MISO); the display shares the SPI bus with the MAX31865 (own chip select). Firmware: the MAX31865 uses SPI mode 1 (or 3) and the GC9A01 mode 0, so each access must use its own SPI transaction settings, and no MAX31865 read may happen during a DMA transfer to the display. The module carries its own backlight transistor and resistors (Q2, R1 to R3 on the photo), so **BLK is driven directly from GPIO 14**: the 2N2222A stage Q4 and its two resistors become **optional**, to be fitted only if the module's schematic shows that BLK drives the LED directly. **The ribbon is 20 cm long**, so SCL (SCK, GPIO 12) and SDA (MOSI, GPIO 11) go to J5 through **33 Ω series resistors (R28, R29)**, on the J5 branch only (the MAX31865 stays directly on the bus), as close to the ESP32 pins as routing allows: they soften the clock edges that would otherwise ring along the ribbon (general design practice, not from a data sheet; replace them by 0 Ω links if the display works without). Firmware: start the display SPI at about 20 to 27 MHz and raise it only if the image stays clean (40 MHz or more over 20 cm of flat ribbon may give corrupted pixels); on the ribbon, SCL sits between SDA and VCC with GND at the end, which is not ideal for a fast clock. The display is powered from 3.3 V.

### J6 (MAX31865 module)
VIN (**+3.3 V**, from the 3V3 of the ESP32 board; the Adafruit board accepts 3 to 5 V), 3Vo (unused), GND, CLK (GPIO 12), SDO (GPIO 13), SDI (GPIO 11), CS (GPIO 7), RDY (unused). This is the Adafruit order (VIN, 3Vo, GND, CLK, SDO, SDI, CS, RDY). Powered from 3.3 V, all its logic levels are 3.3 V: SDO goes straight to GPIO 13, no divider and nothing to measure. It draws a few mA from the ESP32 board regulator.

## ESP32-S3 board (read on the photo)
Silkscreen read on the photo, left column from the USB-C end: GND, 5V, G48, BOOT, 48, 47, 38, 39, 40, 21, GND, 18, 17, 16, 15, 41, 42, 45, 46. Right column: GND, 3V3, PWR, RST, 14, 13, 12, 11, 10, 09, 08, 07, GND, 06, 05, 04, 03, 02, 01. Every GPIO used in this design (1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 21, 38, 39, 41, 42, 47) is broken out on this board, and the strapping pins to avoid (0 = BOOT, 3, 45, 46) are the ones marked. Still free: 40 (left). GPIO 48 is broken out but drives the board's LED marked G48 (180 Ω, read on a close-up photo); next to the USB-C, the LED marked PWR is the power indicator. The 3.3 V regulator is the small 5-pin SOT-23-5 part under the USB-C (not an AMS1117; probably an ME6211-class, about 500 mA, marking not readable on the photo). Measured by you: 21 mm wide, 2 x 20 pins, rows 17.78 mm apart (about 54 mm long, plus about 1.5 mm of USB-C overhang).

## ESP32-S3 pins
5V, 3V3, GND; GPIO 17 (pump SSR), 18 (boiler SSR), 21 (valve SSR); 15 (flow In), 16 (flow Out); 4 / 5 (encoder); 6 (start button); 41 (steam button); 11 / 12 / 13 (SPI MOSI / SCK / MISO); 10 (display CS); 9 / 8 (display DC / RST); 14 (backlight); 7 (MAX31865 CS); 47 / 42 (dimmer, I2C SDA / SCL); 1 (pressure, ADC); 2 (5 V rail measure, ADC); 38 / 39 (spare IN / OUT, on J7). Avoided: 0, 3, 45, 46, 19, 20, 35 to 37 (not broken out on this board), 48 (board LED G48).

## Circuits
- **Power:** supply **5.1 V, 2 A** (measured by you), brought by **two wires soldered to the PWR pads** (+5 V on the square pad, GND), ending in a **JST SM 2-pin** plug towards the supply (polarised and latching); hold the wires with a dab of hot glue or silicone next to the pads (pump vibrations). PWR + → 1.1 A resettable fuse → +5 V rail (about 5.0 V; 470 µF + 100 nF) → **D2 (1N5819)** → 5V pin of the ESP32. The 3.3 V comes from the ESP32 board. **D2 replaces the former jumper JP1** (same two pads, diode standing, cathode on the ESP32 side): the ESP32 takes its power from the board or from its USB port, and the diode keeps the two 5 V sources apart, so the **USB cable can be plugged with the machine on** (flashing, logs) without back-feeding the computer. The ESP32 5V pin then sees about 4.6 V from the board, enough for its 3.3 V regulator. **There is no reverse-protection diode** (the former D1 is removed): the latching JST SM plug is polarised, so the supply cannot be reversed once the plug is wired right, and a diode would bring the rail down to about 4.6 V, below the 5 V minimum of the USN-HS06PD. **Check the polarity of the JST SM plug once, with a multimeter, when you crimp it** (+5 V on the square PWR pad): nothing on the board survives a reversed supply. With the USB cable alone, the ESP32, the display, the MAX31865, the encoder and the dimmer logic run; the 5 V side (SSRs, sensors) stays off.
- **Safety:** an SSR usually fails **closed** (stuck on). Keep the machine's original safety thermostat / thermal fuse in series with the boiler heater, whatever the firmware does; the board alone cannot guarantee that the boiler stops.
- **SSR (x3):** GPIO → 1 kΩ → 2N2222A base; 10 kΩ base → GND; SSR "+" input to the +5 V rail, "−" input to the collector; emitter to GND. The SSR input receives about 4.8 V (rail about 5.0 V minus about 0.2 V across the transistor), well above the usual 3 V minimum of a DC-input SSR.
- **Flow sensor (x2):** signal → **4.7 kΩ to +5 V**; signal → **10 kΩ** → GPIO; GPIO → **22 kΩ** → GND; 1 nF GPIO → GND. With a 5 V push-pull output the GPIO sees 5 x 22 / 32 = 3.4 V; with an open collector the pull-up is loaded by the divider and the GPIO sees 5 x 22 / (4.7 + 10 + 22) = 3.0 V; with a sensor that has its own internal pull-up, between the two. (The former values, 10 kΩ pull-up and 4.7 kΩ / 10 kΩ divider, gave only 2.0 V with an open collector, below the ESP32 input-high threshold of about 2.5 V.) The low level (0.5 V max at the sensor) gives under 0.35 V.
- **Flow In sensor (J3): USN-HS06PD** (Hall sensor, 6 mm tube, 0.1 to 1.5 l/min, F (Hz) = 200 x Q (l/min), i.e. 12,000 pulses per litre, 300 Hz max; supply 5 to 24 V, under 10 mA; output high at least 4.5 V and low at most 0.5 V at 5 V; duty cycle 50 ± 10 %; -20 to 60 °C; **working pressure under 0.8 MPa (8 bar)**, so it must stay on the low-pressure side, between the tank and the pump; XH 2.54 plug, wire order varies by batch: check it). Its lower limit, 0.1 l/min = 1.7 ml/s, is below the pump flow during an extraction (about 4 ml/s measured at the inlet), so it works in range.
- **Flow Out sensor (J4): Digmesa Nano** (brass, 1.2 mm nozzle; 31,100 pulses per litre, linear 0.83 to 8.3 ml/s, so 258 Hz max; ±2 %; 0 to 100 °C; 20 bar), on the boiler side. Its turbine counts in both flow directions: the firmware ignores its pulses while the pump is stopped. Its output type does not matter, the input circuit above suits it.
- **Display backlight:** BLK ← GPIO 14 directly (the display module has its own transistor). Optional stage Q4: GPIO 14 → 1 kΩ → 2N2222A base, not fitted by default.
- **Test points:** TP1 +5 V, TP2 3.3 V, TP3 GND, bare pads (1 mm holes) in the corridor below R28 / R29, for a multimeter probe or a wire loop; SDA / SCL can be probed on the pads of R24 / R25 (back tab).
- **Encoder / buttons:** see "Encoder and 5 V input protection". **No RC filter on GA / GB:** the encoder library's interrupt routine expects every rising and falling edge, bounces included, and debounces in software; the two buttons are debounced in the firmware too.

## Firmware notes
- **Flow sensors: use the ESP32-S3 hardware pulse counter (PCNT)**, not GPIO interrupts. The S3 has 4 PCNT units (2 channels each), any GPIO can be routed to them. One unit per sensor: flow In on GPIO 15, flow Out on GPIO 16, counting rising edges only (falling edge: hold), with the hardware glitch filter at about 10 µs (`max_glitch_ns = 10000`; the filter goes up to about 12 µs). No pulse is lost while the display (SPI / DMA) or the Bluetooth keep the CPU busy. The counter is 16-bit (±32,767): enable `accum_count` with a watch point at the limit, or read and accumulate it regularly (32,767 pulses = about 2.7 l on the USN-HS06PD at 12,000 pulses per litre, about 1.05 l on the Digmesa at 31,100 pulses per litre). The PCNT does not see the direction of the Digmesa turbine: keep the "pump stopped" filter in software (store the count when the pump stops, ignore what comes after). ESP-IDF 5 driver `driver/pulse_cnt.h` (`pcnt_new_unit`, `pcnt_new_channel`, `pcnt_channel_set_edge_action`, `pcnt_unit_get_count`), available in Arduino-ESP32 3.x.
- **Safety in the firmware:** switch the boiler SSR off when the MAX31865 reports a fault (open or shorted probe, reading out of range) and enable the hardware watchdog, so that a frozen program releases the SSRs (on reset, the base pull-downs switch every SSR off).
- **Flashing with the machine on** is safe: during a reset or in the bootloader the GPIOs float and the base pull-downs keep the three SSRs off; D2 keeps the USB and the board supply apart. With the machine closed, plan **OTA updates over Wi-Fi** as well.
- **Encoder: keep the interrupt-based encoder library, not the PCNT.** The PCNT can decode a quadrature encoder, but the knob's push is carried by the GA line (0 Ω hack): the PCNT would see a push as a quarter step back and forth and could not tell it apart; the library's state machine recognises it. The encoder turns slowly, interrupts are enough.

## Bill of materials (through-hole)
| Qty | Part | Indicative price |
|---|---|---|
| 1 | ESP32-S3 N16R8 board (owned) | 0 |
| 2 | 1 x 20 female sockets, 8.5 mm | 1 € |
| 1 | MAX31865 module (owned) + low 1 x 8 socket | 0.3 € |
| 1 | 8-pin FPC board (owned) + 2 x 4 male header + 2 x 4 female socket | 0.5 € |
| 1 | 3-row right-angle 2.54 mm male header strip ("courbé" 3 x 40, e.g. Funduino, about 1.7 €): cut two 3 x 4 (J2 + J8, and J7) | 1.7 € |
| 1 | JST SM 2-pin plug and socket pair + about 30 cm of two-wire cable (5 V supply, PWR) | 0.5 € |
| 3 | JST XH 3-pin headers (J3, J4, J9) | 0.7 € |
| 4 | 2N2222A transistors (3 SSRs + spare output; backlight stage optional) | 0.6 € |
| 31 | axial resistors R1 to R31 (33 Ω, 1 kΩ, 4.7 kΩ, 10 kΩ, 12 kΩ, 22 kΩ; R4 with Q4 optional) | 1.5 € |
| 1 | 1.1 A resettable fuse (radial) | 0.5 € |
| 1 | 1N5819 diode (D2, ESP32 supply) | 0.2 € |
| 1 | 470 µF 10 V radial capacitor (105 °C); 3 x 100 nF (C2, C5, C6); 2 x 1 nF (C3, C4) | 1 € |
| | Dupont female housings + crimp contacts: one 2 x 4 (J2), 1 x 4 x 3 (J8, J7 rows B and C), 1 x 2 x 2 (J7 row A); JST XH 3-pin housings + crimps for the sensors that do not come with an XH plug (Digmesa, pressure sensor) | 2 € |
| 4 | 3 mm standoffs (existing) + M2.5 screws, **one of them nylon** (the hole under the antenna) | 0.2 € |
| | **Total parts** (without the ESP32, the MAX31865 module and the FPC adapter) | **about 11 €** (unit prices; more if bought in packs) |
| 5 | bare boards, 58 x 68 mm + two 42 x 7 mm tabs (front and back), 2 layers (shipping included) | 10 to 20 € |

## Points to confirm before manufacturing
1. Display ribbon (J5): the pinout of the module is known (BLK, CS, DC, RES, SDA, SCL, VCC, GND); still to confirm the ribbon type (straight or reversed contacts) and the adapter's FPC-pin-to-header mapping, and the backlight polarity of BLK.
2. Encoder: pin order GA, GB, VCC, GND confirmed (Funduino data sheet); pull-ups measured, 6.6 kΩ to VCC (3.3 kΩ resistors); the two end components on the module are not identified (capacitor or push resistor).
3. ESP32-S3 board: **confirmed**, 2 x 20 pins, rows 17.78 mm apart, 21 mm wide.
4. Dimensions of your FPC adapter board (about 22 x 26 mm estimated) and position of its mounting holes.
5. Flow sensors: the In sensor is a USN-HS06PD (5 V output, high at least 4.5 V); the circuit (4.7 kΩ pull-up, 10 kΩ / 22 kΩ divider) suits 5 V outputs, open collectors and internal pull-ups; check the wire order of the XH plug (it varies by batch).
6. MAX31865 module (Adafruit, measured from the manufacturer's drawing): 25.4 x 27.9 mm, mounting holes 0.9" apart and 0.1" from the terminal-block edge, 1 x 8 header at 0.1" pitch on the short edge.
7. Pump dimmer: one-time switch from UART to I2C (see J8); behaviour with the vibration pump to test; powered from 3.3 V, no level shifter; pull-ups of the module, if any; its 3.3 V consumption.
8. Pressure sensor: confirm 3 wires (+5 V, GND, signal) and the G1/4 fitting on the hydraulic circuit; check its **temperature rating** (many G1/4 transducers stop at 85 °C): tapped on the T next to the boiler it may see hot water, so a short metal pipe or a small loop between the T and the sensor keeps it cooler.
9. USB-C opening in the left wall (y 9 to 19 mm) and the USB cable bend outside the box.
10. Display ribbon: **20 cm long** (hence R28 / R29 and a moderate SPI clock); thickness and pin-1 orientation of your FPC adapter board; the column x 7 to 18 mm in front of it must stay free of tall parts.
11. MAX31865: powered from 3.3 V, so SDO is 3.3 V (settled).
12. Rotary knob (CJMCU-111, photo: pins GA, GB, VCC, GND): the push is on the GA line through a 3 kΩ resistor; the firmware's encoder library handles it from the GA / GB edges (as on the Nano). Pull-ups measured: 6.6 kΩ from GA / GB to VCC. **Done: the 0 Ω hack** (push resistor bridged, pins 4 and 1), required with the encoder at 3.3 V. The library's analog alternative (330 Ω and an analog read of GA) is not kept: with the 3.3 kΩ pull-up at 3.3 V a push would give only about 0.3 V against 0 V for a rotation step, too close to tell apart reliably on the ESP32 ADC (and `analogRead()` must not be called inside an interrupt routine on the ESP32).
13. Supply level of the sensors: **settled**, D1 removed (no reverse-protection diode), so the +5 V rail is about 5.0 V (5.1 V supply minus F1), at the 5 V minimum of the USN-HS06PD; R23 and R27 are 12 kΩ so that the rail measure stays at 2.7 V on GPIO 2. Check the supply range of the pressure sensor (often 5 V ± 0.25 V) and the polarity of the JST SM plug (no reverse protection any more).
14. Temperature of the ESP32 board's 3.3 V regulator (SOT-23-5, about 0.2 W with the display, the MAX31865 and the Bluetooth) inside the hot machine: touch it after 30 minutes of use; if it is too hot to keep a finger on, a 3.3 V regulator for the display on the carrier would relieve it.
