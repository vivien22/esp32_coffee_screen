import os
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S = 2
W, H = 1800, 1440
im = Image.new('RGB', (W * S, H * S), (248, 248, 244))
d = ImageDraw.Draw(im)

def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/%s.ttf' % ('arialbd' if b else 'arial'), sz * S)
def R(x0, y0, x1, y1, **k): d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], **k)
def RR(x0, y0, x1, y1, r, **k): d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], r * S, **k)
def E(x0, y0, x1, y1, **k): d.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], **k)
def L(pts, c, w=3): d.line([(x * S, y * S) for x, y in pts], fill=c, width=int(w * S), joint='curve')
def T(x, y, s, f, c=(30, 30, 36), a='mm'): d.text((x * S, y * S), s, font=f, fill=c, anchor=a)

INK = (30, 30, 36); GRY = (110, 110, 116); RED = (200, 40, 40); BLU = (30, 90, 170); GRN = (20, 120, 60)
ORG = (214, 110, 20); BRN = (140, 90, 40); YEL = (200, 160, 0); VIO = (110, 70, 170)

T(W / 2, 36, "ESP32-S3 carrier board: connection schematic (all through-hole, no SMD soldering)", F(30, True))
T(W / 2, 74, "Concept schematic: validate before manufacturing (display, encoder and dimmer details to confirm).", F(19), GRY)

# ================================================================ 1. connectors
def pin(x, y, label, fill, size=15, w=84, h=44, txt=(255, 255, 255)):
    RR(x, y, x + w, y + h, 6, fill=fill, outline=(20, 20, 24), width=2)
    T(x + w / 2, y + h / 2, label, F(size, True), txt)

DK = (60, 60, 66); LG = (150, 150, 156)
def head(x, y, title, sub=None):
    T(x, y, title, F(22, True), INK, 'lm')
    if sub:
        T(x, y + 28, sub, F(15), GRY, 'lm')

# ---- J2 : 2 x 4 right-angle header, ONE 2 x 4 Dupont housing, two ribbons of 4 wires (one per row)
head(60, 118, "J2: right-angle 2 x 4 male header, one 2 x 4 Dupont housing", "two ribbons of 4 wires: row A (top) and row B (bottom)")
rowA = [("+5 V", RED), ("GND", DK), ("pump +", BRN), ("pump −", BRN)]
rowB = [("boiler +", ORG), ("boiler −", ORG), ("valve +", YEL), ("valve −", YEL)]
x0, yA, yB = 60, 190, 240
for i, (lab, col) in enumerate(rowA):
    pin(x0 + i * 88, yA, lab, col, 14)
for i, (lab, col) in enumerate(rowB):
    pin(x0 + i * 88, yB, lab, col, 14)
T(x0 + 2 * 88, 306, "ribbon 1: 5 V supply + pump SSR", F(13, True), RED, 'mm') if False else None
T(x0 + 176, 306, "ribbon 1 (row A): 5 V supply, then pump SSR", F(13, True), RED)
T(x0 + 176, 328, "ribbon 2 (row B): boiler SSR, then valve SSR", F(13, True), ORG)
T(x0 + 370, 214, "a 2 x 4 housing can be plugged 180 degrees", F(14), GRY, 'lm')
T(x0 + 370, 236, "the wrong way round: use a keyed (shrouded)", F(14), GRY, 'lm')
T(x0 + 370, 258, "2 x 4 header, or mark the housing", F(14), GRY, 'lm')

# ---- J7 : 2 x 6 (two stacked rows of housings)
head(60, 350, "J7: right-angle 2 x 6 male header: button, encoder (5 V) and 4 spare I/O pins")
j7a = [("button", (90, 90, 96)), ("GND", DK), ("+5 V", RED), ("IN 38", VIO), ("OUT 39", VIO), ("GND", DK)]
j7b = [("+5 V", RED), ("GND", DK), ("enc. A", GRN), ("enc. B", GRN)]
for i, (lab, col) in enumerate(j7a):
    pin(60 + i * 88, 382, lab, col, 14)
for i, (lab, col) in enumerate(j7b):
    pin(60 + i * 88, 430, lab, col, 14)
T(620, 404, "row A: 2-pin + 4-pin spare", F(14), GRY, 'lm')
T(620, 452, "row B: 4-pin encoder", F(14), GRY, 'lm')

# ---- J8 / J9
head(60, 490, "J8: pump dimmer (I2C)", "RobotDyn 4 A, DimmerLink")
for i, (lab, col) in enumerate([("3V3", RED), ("GND", DK), ("SDA", VIO), ("SCL", VIO)]):
    pin(60 + i * 88, 548, lab, col, 14)
head(480, 490, "J9: pressure sensor", "0.5 to 4.5 V, 0 to 12 bar")
for i, (lab, col) in enumerate([("+5 V", RED), ("GND", DK), ("signal", BLU)]):
    pin(480 + i * 88, 548, lab, col, 14)

# ---- J3 / J4
head(60, 628, "J3, J4: JST XH 3-pin, flow sensors In and Out", "sensor wire order: often red / yellow / black: check your cable")
for k, (name, x) in enumerate([("J3  flow In", 60), ("J4  flow Out", 480)]):
    T(x, 690, name, F(15, True), INK, 'lm')
    for i, (lab, col) in enumerate([("+5 V", RED), ("signal", BLU), ("GND", DK)]):
        pin(x + i * 88, 710, lab, col, 14)

# ---- J5
head(60, 790, "J5: 2 x 4 socket for your FPC adapter board (8 pins)", "your board's numbering: top row 1, 3, 5, 7; bottom row 2, 4, 6, 8")
fpc_top = [("1", "GND"), ("3", "SCL"), ("5", "DC"), ("7", "RST")]
fpc_bot = [("2", "3V3"), ("4", "SDA"), ("6", "CS"), ("8", "BL")]
for i, (n, sg) in enumerate(fpc_top):
    pin(60 + i * 96, 850, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
for i, (n, sg) in enumerate(fpc_bot):
    pin(60 + i * 96, 900, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
T(60, 966, "Provisional assignment (typical 8-pin GC9A01): the exact order comes from your display datasheet.", F(14), RED, 'lm')

# ---- J6
head(60, 1000, "J6: 1 x 8 socket for the MAX31865 module", "Adafruit order; powered from 3.3 V; 3Vo and RDY unused")
mx = [("VIN", RED), ("3Vo", LG), ("GND", DK), ("CLK", VIO), ("SDO", VIO), ("SDI", VIO), ("CS", VIO), ("RDY", LG)]
for i, (lab, col) in enumerate(mx):
    pin(60 + i * 88, 1060, lab, col, 14)

# ================================================================ 2. GPIO table
gx = 860
T(gx, 118, "ESP32-S3: pins used", F(22, True), INK, 'lm')
rows = [("5V", "+5 V (after diode and fuse)", RED), ("3V3", "powers MAX31865, display, dimmer", RED),
        ("GPIO 17", "pump SSR drive", BRN), ("GPIO 18", "boiler SSR drive", ORG), ("GPIO 21", "valve SSR drive", YEL),
        ("GPIO 15", "flow In", BLU), ("GPIO 16", "flow Out", BLU), ("GPIO 1", "pressure sensor (ADC)", BLU),
        ("GPIO 4 / 5", "encoder A / B", GRN), ("GPIO 6", "start button", (90, 90, 96)),
        ("GPIO 47 / 48", "dimmer I2C: SDA / SCL", VIO),
        ("GPIO 11 / 12 / 13", "SPI: MOSI / SCK / MISO", VIO), ("GPIO 10", "display CS", VIO), ("GPIO 9 / 8", "display DC / RST", VIO),
        ("GPIO 14", "display backlight (transistor)", VIO), ("GPIO 7", "MAX31865 CS", VIO), ("GPIO 38", "spare input on J7 (5 V divider)", (150, 150, 156)), ("GPIO 39", "spare output on J7 (to 5 V, inverting)", (150, 150, 156))]
for i, (a, b, col) in enumerate(rows):
    y = 150 + i * 34
    RR(gx, y, gx + 180, y + 28, 5, fill=col, outline=(20, 20, 24), width=1)
    T(gx + 90, y + 14, a, F(14, True), (255, 255, 255))
    T(gx + 192, y + 14, b, F(15), INK, 'lm')
T(gx, 786, "Avoided: 0, 3, 45, 46 (strapping), 19 and 20 (USB), 35 to 37 (PSRAM).", F(15), GRY, 'lm')

# ================================================================ 2b. input circuits (chains)
def box(x, y, w, h, label, fill=(250, 250, 240), col=INK, size=12):
    RR(x, y, x + w, y + h, 4, fill=fill, outline=col, width=2)
    T(x + w / 2, y + h / 2, label, F(size, True), col)
def shunt(x, y, label):
    L([(x, y), (x, y + 22)], INK, 2)
    box(x - 24, y + 22, 48, 22, label)
    L([(x, y + 44), (x, y + 58)], INK, 2); T(x, y + 70, "GND", F(11, True))
def chain(x, y, title, src, res, end, shunts, col):
    T(x, y - 26, title, F(16, True), col, 'lm')
    box(x, y - 16, 92, 32, src, (232, 240, 252), BLU, 12)
    L([(x + 92, y), (x + 150, y)], col, 3)
    box(x + 150, y - 12, 56, 24, res)
    L([(x + 206, y), (x + 340, y)], col, 3)
    T(x + 352, y, end, F(13, True), col, 'lm')
    for sx, lab in shunts:
        L([(x + sx, y), (x + sx, y)], col, 2)
        shunt(x + sx, y, lab)
cy = 850
chain(gx, cy, "Encoder A, B, button, spare IN 38 (x4): 5 V to 3.3 V", "module out", "4.7 k", "GPIO", [(270, "10 k")], GRN)
chain(gx, cy + 120, "Pressure input: 4.5 V to 3.0 V", "sensor", "10 k", "GPIO 1", [(250, "20 k"), (320, "100 nF")], BLU)
T(gx, cy + 262, "Dimmer I2C pull-ups: 4.7 k from SDA (GPIO 47) and from SCL (GPIO 48) to 3V3", F(14, True), VIO, 'lm')
T(gx, cy + 286, "(100 kHz, cable under 30 cm; the module is shipped in UART mode: switch it to I2C once)", F(13), GRY, 'lm')

# ================================================================ 3. circuits
cx0 = 1370
T(cx0, 118, "Circuits on the board", F(22, True), INK, 'lm')

# power
T(cx0, 160, "Power", F(17, True), RED, 'lm')
L([(cx0, 200), (cx0 + 40, 200)], RED, 3); T(cx0 - 6, 200, "A1", F(13, True), RED, 'rm')
RR(cx0 + 40, 188, cx0 + 118, 212, 4, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 79, 200, "fuse 1.1 A", F(11, True))
L([(cx0 + 118, 200), (cx0 + 150, 200)], RED, 3)
d.polygon([((cx0 + 150) * S, 188 * S), ((cx0 + 150) * S, 212 * S), ((cx0 + 180) * S, 200 * S)], fill=(250, 250, 240), outline=INK)
L([(cx0 + 180, 186), (cx0 + 180, 214)], INK, 3); T(cx0 + 165, 232, "1N5819", F(11, True))
L([(cx0 + 180, 200), (cx0 + 270, 200)], RED, 3)
T(cx0 + 300, 200, "+5 V board", F(14, True), RED, 'lm')
L([(cx0 + 215, 200), (cx0 + 215, 232)], RED, 2)
L([(cx0 + 205, 232), (cx0 + 225, 232)], INK, 3); L([(cx0 + 205, 240), (cx0 + 225, 240)], INK, 3)
L([(cx0 + 215, 240), (cx0 + 215, 262)], INK, 2); T(cx0 + 215, 276, "470 µF + 100 nF", F(11, True))

# SSR driver
T(cx0, 330, "SSR drive (x3)", F(17, True), BRN, 'lm')
L([(cx0 + 20, 365), (cx0 + 250, 365)], RED, 3); T(cx0 + 262, 365, "+5 V", F(13, True), RED, 'lm')
RR(cx0 + 110, 385, cx0 + 200, 430, 6, fill=(232, 240, 252), outline=BLU, width=3); T(cx0 + 155, 400, "SSR", F(12, True), BLU); T(cx0 + 155, 417, "input + −", F(12, True), BLU)
L([(cx0 + 155, 365), (cx0 + 155, 385)], RED, 3)
L([(cx0 + 155, 430), (cx0 + 155, 470)], INK, 3)
E(cx0 + 125, 470, cx0 + 185, 530, outline=INK, width=3)
L([(cx0 + 140, 485), (cx0 + 140, 515)], INK, 4)
L([(cx0 + 140, 495), (cx0 + 165, 478), (cx0 + 165, 470), (cx0 + 155, 470)], INK, 3)
L([(cx0 + 140, 505), (cx0 + 165, 522), (cx0 + 165, 560)], INK, 3)
L([(cx0 + 165, 560), (cx0 + 165, 590)], INK, 3); T(cx0 + 165, 604, "GND", F(12, True))
L([(cx0 + 60, 500), (cx0 + 140, 500)], INK, 3)
RR(cx0 + 20, 488, cx0 + 60, 512, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 40, 500, "1 k", F(12, True))
L([(cx0 - 20, 500), (cx0 + 20, 500)], BRN, 3); T(cx0 - 28, 500, "GPIO", F(12, True), BRN, 'rm')
L([(cx0 + 100, 500), (cx0 + 100, 540)], INK, 2)
RR(cx0 + 88, 540, cx0 + 112, 575, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 100, 557, "10k", F(11, True))
L([(cx0 + 100, 575), (cx0 + 100, 590)], INK, 2); T(cx0 + 100, 604, "GND", F(12, True))
T(cx0 + 20, 640, "2N2222A (TO-92): the SSR input receives almost the full 5 V", F(13), GRY, 'lm')

# flow input
T(cx0, 700, "Flow sensor input (x2)", F(17, True), BLU, 'lm')
L([(cx0 + 20, 735), (cx0 + 250, 735)], RED, 3); T(cx0 + 262, 735, "+5 V", F(13, True), RED, 'lm')
L([(cx0 + 60, 735), (cx0 + 60, 765)], RED, 2)
RR(cx0 + 48, 765, cx0 + 72, 800, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 60, 782, "10k", F(11, True))
L([(cx0 + 60, 800), (cx0 + 60, 830)], BLU, 2)
L([(cx0 - 20, 830), (cx0 + 60, 830), (cx0 + 100, 830)], BLU, 3); T(cx0 - 28, 830, "signal J3", F(12, True), BLU, 'rm')
RR(cx0 + 100, 818, cx0 + 150, 842, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 125, 830, "4.7k", F(11, True))
L([(cx0 + 150, 830), (cx0 + 230, 830)], BLU, 3); T(cx0 + 242, 830, "GPIO", F(13, True), BLU, 'lm')
L([(cx0 + 190, 830), (cx0 + 190, 860)], BLU, 2)
RR(cx0 + 178, 860, cx0 + 202, 895, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 190, 877, "10k", F(11, True))
L([(cx0 + 190, 895), (cx0 + 190, 915)], INK, 2); T(cx0 + 190, 928, "GND", F(12, True))
L([(cx0 + 225, 830), (cx0 + 225, 860)], BLU, 2); L([(cx0 + 215, 860), (cx0 + 235, 860)], INK, 3); L([(cx0 + 215, 868), (cx0 + 235, 868)], INK, 3)
L([(cx0 + 225, 868), (cx0 + 225, 890)], INK, 2); T(cx0 + 225, 904, "1 nF", F(11, True))
T(cx0 + 20, 960, "Works with a 5 V output sensor (the divider gives 3.4 V)", F(13), GRY, 'lm')
T(cx0 + 20, 982, "or open collector (the 10 k resistor pulls up to 5 V).", F(13), GRY, 'lm')

# spare output stage (GPIO 39 -> 5 V, inverting), under the flow circuit
T(cx0, 1040, "Spare output OUT (GPIO 39): 3.3 V to 5 V, inverting", F(16, True), VIO, 'lm')
L([(cx0 + 20, 1085), (cx0 + 250, 1085)], RED, 3); T(cx0 + 262, 1085, "+5 V", F(13, True), RED, 'lm')
L([(cx0 + 155, 1085), (cx0 + 155, 1105)], RED, 2)
RR(cx0 + 143, 1105, cx0 + 167, 1140, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 155, 1122, "4.7k", F(11, True))
L([(cx0 + 155, 1140), (cx0 + 155, 1175)], VIO, 3)
L([(cx0 + 155, 1158), (cx0 + 240, 1158)], VIO, 3); T(cx0 + 252, 1158, "OUT (J7)", F(13, True), VIO, 'lm')
RR(cx0 + 125, 1175, cx0 + 185, 1235, 8, fill=(250, 250, 240), outline=INK, width=3); T(cx0 + 155, 1205, "Q5", F(14, True))
L([(cx0 + 155, 1235), (cx0 + 155, 1262)], INK, 3); T(cx0 + 155, 1275, "GND", F(12, True))
L([(cx0 + 60, 1205), (cx0 + 125, 1205)], VIO, 3)
RR(cx0 + 20, 1193, cx0 + 60, 1217, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 40, 1205, "1 k", F(12, True))
L([(cx0 - 20, 1205), (cx0 + 20, 1205)], VIO, 3); T(cx0 - 28, 1205, "GPIO 39", F(12, True), VIO, 'rm')
L([(cx0 + 90, 1205), (cx0 + 90, 1240)], INK, 2)
RR(cx0 + 78, 1240, cx0 + 102, 1275, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 90, 1257, "10k", F(11, True))
T(cx0 + 20, 1310, "GPIO high -> OUT low; GPIO low -> OUT 5 V (invert in firmware).", F(13), GRY, 'lm')

# ================================================================ 4. notes
T(60, 1140, "Design notes", F(22, True), INK, 'lm')
notes = [
    "The three voltage levels: +5 V board (after fuse and diode), 3.3 V from the ESP32-S3 board, common GND.",
    "The display backlight is driven by a transistor on GPIO 14 (the current exceeds what a pin can supply).",
    "No regulator on the board: the ESP32-S3 provides the 3.3 V (check it can supply the MAX31865, display and dimmer).",
    "The pump dimmer stays off the board on the mains side: only its 4-wire I2C cable comes to J8.",
    "All parts are through-hole (TO-92, axial resistors, radial capacitors, DO-41): ordinary soldering iron.",
    "On the board: a ground plane, no copper under the ESP32 antenna, 4 mounting holes (45 x 50 mm).",
    "Silkscreen: name of each connector, pin 1 mark, and the signal of each pin (+5 V, GND, SSR +, SSR −, signal...).",
]
for i, t in enumerate(notes):
    T(60, 1176 + i * 30, "• " + t, F(16), INK, 'lm')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'connection_schematic.png'))
print('ok')
