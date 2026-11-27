# Ordering the carrier board parts (Farnell France)

Prepared on 2026-11-28 from `docs/carrier_spec.md` (bill of materials). Order codes were checked on fr.farnell.com that day, except where noted. Prices and stock change: the cart shows the real total.

Already owned, not in this list: ESP32-S3 N16R8 board, MAX31865 module, FPC adapter board, JST XH cable plugs of the sensors, JST SM 2-pin pair (5 V supply), Dupont housings and contacts.

## Quick paste (Farnell order code, quantity)
Paste into the cart's quick-paste box ("Saisie rapide" / "Quick Paste"):

```
1593469, 2
2856907, 1
1593490, 1
1516277, 3
1700711, 5
9801219, 1
1345960, 1
1907187, 1
1457657, 10
9341773, 10
9341102, 10
9341951, 10
9341110, 20
9341234, 10
9341544, 10
```

| Farnell code | Part | Board use | Notes |
|---|---|---|---|
| 1593469 | Multicomp 2212S-20SG-85, female header 1 x 20, 2.54 mm, 8.5 mm | ESP32 sockets (x2) | |
| 2856907 | Samtec TSW-104-07-F-D, male header 2 x 4, through-hole | FPC adapter board | details not checked |
| 1593490 | Multicomp 2214S-10SG-85, female header 2 x 5, 8.5 mm | J5 (FPC adapter socket) | no 2 x 4 found: cut it down to 2 x 4 |
| 1516277 | JST B3B-XH-A(LF)(SN), XH 3-way vertical header | J3, J4, J9 | |
| 1700711 | onsemi PN2222ATA, NPN, TO-92 | Q1 to Q5 (Q4 optional) | minimum order 5; pinout E-B-C: match the footprint at routing |
| 9801219 | STMicroelectronics 1N5819, Schottky 1 A 40 V | D2 | |
| 1345960 | Littelfuse RXEF110, resettable fuse 1.1 A hold, 72 V, radial | F1 | |
| 1907187 | Panasonic ECA1AHG331, 330 µF 10 V, 6.3 x 11.2 mm, 2.5 mm pitch, 105 °C | C1 | fits the 6.3 mm footprint; a 470 µF 10 V is usually 8 mm wide |
| 1457657 | KEMET C315C104M5U5TA, 100 nF 50 V, 2.54 mm pitch | C2, C5, C6 | minimum order 10 |
| 9341773 | Multicomp MF25 33R, 1 %, 0.25 W | R28, R29 (x2) | resistors sold by 10 |
| 9341102 | Multicomp MF25 1K | R1 to R4, R9, R10, R19 (x7) | |
| 9341951 | Multicomp MF25 4K7 | x6: flow pull-ups (x2), R17, R20, R24, R25 | flow pull-ups, spare IN, spare OUT pull-up, I2C pull-ups |
| 9341110 | Multicomp MF25 10K | x12: R5 to R8, R18, R21, R22, R26, R30, R31, flow series (x2) | |
| 9341234 | Multicomp MF25 12K | R23, R27 (x2) | pressure and rail dividers |
| 9341544 | Multicomp MF25 22K | flow dividers (x2) | code read on element14 (Farnell's parent): check that it is accepted |

Resistor count by value (R1 to R31): 33 Ω x2, 1 kΩ x7, 4.7 kΩ x6, 10 kΩ x12, 12 kΩ x2, 22 kΩ x2.

## Not found at Farnell (buy elsewhere)
- **3-row right-angle male header, 2 x (3 x 4)** for J2 + J8 and J7: Farnell only lists the Samtec 3 x 2 (TSW-102-25-G-T-RA, 3669979; two side by side make a 3 x 4, so 4 would be needed). The Funduino "courbé" 3 x 40 strip planned in the bill of materials is cheaper.
- **Low 1 x 8 female socket for the MAX31865**: it must take **square 0.64 mm pins**. Turned-pin SIL sockets (Harwin D01 series, 177845) only take round 0.41 to 0.51 mm leads: not suitable.
- **1 nF ceramic capacitors with 2.54 mm pitch** (C3, C4): none in 50 V at Farnell; take them from an assortment (legs can be bent).
- **M2.5 nylon screw** (mounting hole under the antenna): hardware shop.

## Before ordering
- A Farnell product page states that, from 1 July 2026, EU orders need a valid intra-EU VAT number: check that Farnell accepts an order from a private person.
- Check the delivery charge against the small order value.
