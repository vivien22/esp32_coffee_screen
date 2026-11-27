# Design decisions and their reasons

A record of the choices made while designing the carrier board (conversation with Claude, November 2026), so that they do not have to be rediscovered. The specification (`docs/carrier_spec.md`) says *what* the board is; this file says *why*, and what was considered and rejected. Newest topics are not necessarily last: the file is grouped by subject.

## The machine (facts measured or read)
- Ascaso Steel Uno Pro, steel body. Firmware: [coffee_screen](https://github.com/vivien22/coffee_screen) (Arduino Nano, moving to this ESP32-S3 board).
- Pump: Olab Silent Green vibration pump (230 V AC coil with a series diode, so it is fed half-wave). A **DC-DC SSR works** on it, an **AC SSR does not**; 230 V AC measured across the open SSR.
- Hydraulics: tank → flow In sensor → pump → T on the boiler (one side the OPV, the other the boiler inlet). During a 35 s extraction: about 150 ml in, 60 ml in the cup, 40 to 60 ml returned by the OPV.
- The former Out flow sensor (plastic) melted near the boiler.

## Board outline and placement
- 58 x 68 mm board on the four 3 mm posts (45 x 50 mm), plus a 42 x 7 mm **front tab** (Dupont housings and JST XH plugs up to the front wall) and a 42 x 7 mm **back tab** (C1, C2, I2C and button pull-ups), 82 mm long in all; checked to fit the 85 mm enclosure.
- ESP32-S3 N16R8 board measured: 21 mm wide, 2 x 20 pins, rows 17.78 mm apart. Rotated 90°, USB-C to the left wall, antenna end on the right with a copper keep-out.
- J3, J4, J9 moved 3.5 mm left (and J3 / J4 back 0.5 mm) to get margin from the board edge and between J3 and J9.
- Q1 to Q4: two rows of two (in-line they overlapped R10 and each other). All TO-92 use a **triangular footprint** (outer legs 2.54 mm apart, middle leg bent 2.54 mm back): three round pads in line at 1.27 mm overlap and would short the legs (found by an automatic pad-clearance check).
- Mounting hole at (6.5, 9): copper ring reduced to 4.6 mm (a 5.6 mm ring came within 0.26 mm of a socket pad). Hole under the antenna: non-plated, **nylon screw**.

## Connectors
- **J7 is a 3 x 4 right-angle header**: row A start button + **steam** button (GPIO 41), row B encoder, row C spare I/O (+5 V, level-adapted IN 38 / OUT 39, GND).
- **J9** (pressure sensor, JST XH 3-pin) on the tab under J3, same pinout as J3 / J4: plugging a sensor into the wrong one of the three is harmless.
- **J8** (pump dimmer) stays the lowest row of the J2 strip. Moving it to its own keyed connector, or reordering its pins so that a misplugged J2 housing cannot switch an SSR on, was proposed and **declined**; the risk (J2 housing pushed one row too low) is handled by marking the housing.
- **Supply**: no longer on J2. Two wires soldered to the **PWR pads** (left end of the tab), ending in a **JST SM 2-pin** latching, polarised plug. J2 A1 / A2 are not connected.

## Power
- Supply 5.1 V, 2 A (measured). PWR → 1.1 A resettable fuse → +5 V rail (about 5.0 V).
- **D1 (reverse-protection 1N5819) removed**: the JST SM plug cannot be reversed, and the diode would bring the rail down to about 4.6 V, below the 5 V minimum of the USN-HS06PD flow sensor. Check the polarity of the plug once with a multimeter when crimping it.
- **D2 (1N5819) replaces the JP1 jumper** between the board rail and the ESP32 5V pin: the USB cable can be plugged with the machine on (no back-feed); with USB alone, the 5 V side (SSRs, sensors) stays off.
- 3.3 V from the ESP32 board regulator (SOT-23-5, not an AMS1117, about 500 mA): it feeds the display, MAX31865, dimmer logic, encoder and pull-ups. Its temperature in the hot machine is to be checked.
- SSRs usually fail closed: the machine's safety thermostat / thermal fuse stays in series with the boiler.

## Interfaces moved to 3.3 V (fewer level shifters)
- **Dimmer (RobotDyn DimmerLink, I2C) at 3.3 V**: no 2N7000 level shifter; 4.7 kΩ pull-ups to 3.3 V. Ships in UART mode, to be switched to I2C once.
- **SCL on GPIO 42, not 48**: on this ESP32 board GPIO 48 drives the LED marked G48 (180 Ω), which would hold SCL low. SDA on GPIO 47 (VDD_SPI domain, 3.3 V on the N16R8).
- **Encoder (CJMCU-111) at 3.3 V**: its GA / GB pull-ups measured at 6.6 kΩ (two 3.3 kΩ); at 5 V with the former 4.7 k / 10 k divider the GPIO would only see about 2.3 V. GA / GB through 1 kΩ series only. The **0 Ω hack** (push resistor bridged) is done and required. No RC filter: the encoder library's interrupt routine wants every edge, bounces included.
- **MAX31865 at 3.3 V**: SDO is then 3.3 V, nothing to measure.
- Buttons: dry contacts, 10 kΩ pull-ups to 3.3 V on the board (the internal 45 kΩ is too weak near the pump wiring), debounced in firmware. Series resistors on the buttons and on I2C were judged not useful.

## Sensors
- **Pressure** (0.5 to 4.5 V, ratiometric, 0 to 12 bar): divider 10 k / 12 k to GPIO 1; the **5 V rail is measured on GPIO 2 with the same divider** and the firmware uses the ratio (pressure = (ratio − 0.1) / 0.8 x 12). C5 / C6 (100 nF) right next to GPIO 1 / 2. Pressure regulation below the OPV threshold is planned.
- **Flow In**: USN-HS06PD (12,000 pulses / l, 5 to 24 V, 8 bar max: low-pressure side only, between tank and pump).
- **Flow Out**: Digmesa Nano brass 1.2 mm (31,100 pulses / l, 100 °C, 20 bar), on the boiler side; its turbine counts both directions, so the firmware ignores its pulses while the pump is stopped.
- Flow input circuit: 4.7 kΩ pull-up to 5 V, 10 kΩ series, 22 kΩ to GND, 1 nF (works with push-pull, open-collector and internal pull-up outputs; the former 10 k / 4.7 k / 10 k values gave only 2.0 V with an open collector).
- Flow sensors counted by the ESP32-S3 **PCNT** hardware counter; the encoder stays on its interrupt library (its push shares the GA line).

## Display
- GC9A01 round display on a **20 cm** ribbon: 33 Ω series resistors on SCK / MOSI (R28, R29, display branch only), SPI clock started at 20 to 27 MHz. Display info read on a photo of the module (no data sheet).

## Wireless
- The scale (Timemore Dot, BLE) must be received through the steel body: test the RSSI with the board in place first. The ESP32 board has a **U.FL connector**: an external antenna (U.FL to SMA pigtail, 2.4 GHz antenna, 6.5 mm hole in the enclosure) can be added later without changing the carrier.

## Mechanics
- The MAX31865 keeps its PT100 screw terminal (removing it would have freed about 5 mm of height; declined). The resistors under the module must clear the terminal-block leads (trim them or use Kapton).

## Workflow
- Commits are made locally; **push only when Vivien writes "pousse"** (the stop-hook message about unpushed commits is not an approval).
- After any change: keep `docs/carrier_spec.md`, the three scripts in `tools/` and the images in `images/` consistent, and regenerate the images.
