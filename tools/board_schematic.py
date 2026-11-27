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
T(W / 2, 74, "Concept schematic: validate before manufacturing (display ribbon and dimmer details to confirm).", F(19), GRY)

# ================================================================ 1. connectors
def pin(x, y, label, fill, size=15, w=84, h=44, txt=(255, 255, 255)):
    RR(x, y, x + w, y + h, 6, fill=fill, outline=(20, 20, 24), width=2)
    T(x + w / 2, y + h / 2, label, F(size, True), txt)

DK = (60, 60, 66); LG = (150, 150, 156)
def head(x, y, title, sub=None):
    T(x, y, title, F(22, True), INK, 'lm')
    if sub:
        T(x, y + 28, sub, F(15), GRY, 'lm')

# ---- J2 + J8 : 3 x 4 right-angle header (3 stacked rows), J7 : 3 x 4
head(60, 118, "J2 + J8: right-angle 3 x 4 male header", "rows A and B: J2 (one 2 x 4 housing, two ribbons of 4 wires); row C: J8")
rowA = [("+5 V", RED), ("GND", DK), ("pump +", BRN), ("pump −", BRN)]
rowB = [("boiler +", ORG), ("boiler −", ORG), ("valve +", YEL), ("valve −", YEL)]
rowC = [("+3.3 V", RED), ("GND", DK), ("SDA", VIO), ("SCL", VIO)]
x0, yA, yB, yC = 60, 186, 232, 278
for i, (lab, col) in enumerate(rowA):
    pin(x0 + i * 88, yA, lab, col, 14)
for i, (lab, col) in enumerate(rowB):
    pin(x0 + i * 88, yB, lab, col, 14)
for i, (lab, col) in enumerate(rowC):
    pin(x0 + i * 88, yC, lab, col, 14)
T(x0 + 370, 196, "row A: 5 V supply + pump SSR (ribbon 1)", F(14, True), RED, 'lm')
T(x0 + 370, 242, "row B: boiler SSR + valve SSR (ribbon 2)", F(14, True), ORG, 'lm')
T(x0 + 370, 288, "row C: J8 pump dimmer, RobotDyn (I2C)", F(14, True), VIO, 'lm')
T(x0 + 370, 312, "a 2 x 4 housing can be plugged 180 degrees the wrong way:", F(13), GRY, 'lm')
T(x0 + 370, 330, "mark it (paint dot on +5 V): no keyed header on a 3-row strip", F(13), GRY, 'lm')

head(60, 366, "J7: right-angle 3 x 4 male header")
j7a = [("button", (90, 90, 96)), ("GND", DK), ("steam", (90, 90, 96)), ("GND", DK)]
j7b = [("GA", GRN), ("GB", GRN), ("+3.3 V", RED), ("GND", DK)]
j7c = [("+5 V", RED), ("IN 38", VIO), ("OUT 39", VIO), ("GND", DK)]
for i, (lab, col) in enumerate(j7a):
    pin(60 + i * 88, 396, lab, col, 14)
for i, (lab, col) in enumerate(j7b):
    pin(60 + i * 88, 442, lab, col, 14)
for i, (lab, col) in enumerate(j7c):
    pin(60 + i * 88, 488, lab, col, 14)
T(440, 418, "row A: start button (2) + steam button (2)", F(14), GRY, 'lm')
T(440, 464, "row B: encoder (module order)", F(14), GRY, 'lm')
T(440, 510, "row C: spare I/O (5 V, level-adapted in / out)", F(14), GRY, 'lm')

# ---- J3 / J4
head(60, 628, "J3, J4: JST XH 3-pin, flow sensors In and Out", "sensor wire order: often red / yellow / black: check your cable")
for k, (name, x) in enumerate([("J3  flow In", 60), ("J4  flow Out", 480)]):
    T(x, 690, name, F(15, True), INK, 'lm')
    for i, (lab, col) in enumerate([("+5 V", RED), ("signal", BLU), ("GND", DK)]):
        pin(x + i * 88, 710, lab, col, 14)
# J9: same JST XH order, pressure sensor (on the tab under J3), drawn under J7 where there is room
T(60, 546, "J9  pressure sensor (JST XH 3-pin, same order as J3 / J4)", F(15, True), INK, 'lm')
for i, (lab, col) in enumerate([("+5 V", RED), ("signal", BLU), ("GND", DK)]):
    pin(60 + i * 88, 562, lab, col, 14)

# ---- J5
head(60, 790, "J5: 2 x 4 socket for your FPC adapter board (8 pins)", "your board's numbering: top row 1, 3, 5, 7; bottom row 2, 4, 6, 8")
fpc_top = [("1", "BLK"), ("3", "DC"), ("5", "SDA"), ("7", "VCC")]
fpc_bot = [("2", "CS"), ("4", "RES"), ("6", "SCL"), ("8", "GND")]
for i, (n, sg) in enumerate(fpc_top):
    pin(60 + i * 96, 850, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
for i, (n, sg) in enumerate(fpc_bot):
    pin(60 + i * 96, 900, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
T(60, 950, "Display module order BLK, CS, DC, RES, SDA, SCL, VCC, GND (photo); straight ribbon assumed.", F(14), RED, 'lm')
T(60, 972, "SDA (GPIO 11) and SCL (GPIO 12) through 33 Ω (R28, R29) on the J5 branch only: 20 cm ribbon.", F(14), BLU, 'lm')

# ---- J6
head(60, 1000, "J6: 1 x 8 socket for the MAX31865 module", "Adafruit order; VIN = +3.3 V (accepts 3 to 5 V): all levels 3.3 V; 3Vo, RDY unused")
mx = [("VIN", RED), ("3Vo", LG), ("GND", DK), ("CLK", VIO), ("SDO", VIO), ("SDI", VIO), ("CS", VIO), ("RDY", LG)]
for i, (lab, col) in enumerate(mx):
    pin(60 + i * 88, 1060, lab, col, 14)

# ================================================================ 2. GPIO table
gx = 860
T(gx, 118, "ESP32-S3: pins used", F(22, True), INK, 'lm')
rows = [("5V", "+5 V via JP1 (after diode and fuse)", RED), ("3V3", "display, MAX31865, dimmer, encoder", RED),
        ("GPIO 17", "pump SSR drive", BRN), ("GPIO 18", "boiler SSR drive", ORG), ("GPIO 21", "valve SSR drive", YEL),
        ("GPIO 15", "flow In", BLU), ("GPIO 16", "flow Out", BLU), ("GPIO 1", "pressure sensor (ADC)", BLU), ("GPIO 2", "5 V rail measure (ADC)", RED),
        ("GPIO 4 / 5", "encoder A / B", GRN), ("GPIO 6 / 41", "start / steam buttons", (90, 90, 96)),
        ("GPIO 47 / 42", "dimmer I2C: SDA / SCL", VIO),
        ("GPIO 11 / 12 / 13", "SPI: MOSI / SCK / MISO", VIO), ("GPIO 10", "display CS", VIO), ("GPIO 9 / 8", "display DC / RST", VIO),
        ("GPIO 14", "display BLK (direct, Q4 optional)", VIO), ("GPIO 7", "MAX31865 CS", VIO), ("GPIO 38", "spare input on J7 (5 V divider)", (150, 150, 156)), ("GPIO 39", "spare output on J7 (to 5 V, inverting)", (150, 150, 156))]
for i, (a, b, col) in enumerate(rows):
    y = 150 + i * 34
    RR(gx, y, gx + 180, y + 28, 5, fill=col, outline=(20, 20, 24), width=1)
    T(gx + 90, y + 14, a, F(14, True), (255, 255, 255))
    T(gx + 192, y + 14, b, F(15), INK, 'lm')
T(gx, 806, "Avoided: 0, 3, 45, 46 (strapping), 19, 20 (USB), 35-37 (PSRAM), 48 (LED).", F(14), GRY, 'lm')

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
cy = 866
chain(gx, cy, "Spare IN 38: 5 V to 3.3 V (encoder: 3.3 V, 1 k series)", "5 V in", "4.7 k", "GPIO 38", [(270, "10 k")], GRN)
chain(gx, cy + 120, "Pressure input: 4.5 V to 2.7 V", "sensor", "10 k", "GPIO 1", [(250, "15 k"), (320, "100 nF")], BLU)
chain(gx, cy + 240, "5 V rail measure (same ratio: pressure = signal / rail)", "+5 V rail", "10 k", "GPIO 2", [(250, "15 k")], RED)
T(gx, cy + 352, "Dimmer I2C: module powered from 3.3 V, no level shifter", F(14, True), VIO, 'lm')
T(gx, cy + 374, "4.7 k pull-ups to 3V3 (R24, R25); SDA 47, SCL 42, 100 kHz", F(13), GRY, 'lm')
T(gx, cy + 394, "ships in UART mode: switch it to I2C once", F(13), GRY, 'lm')

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

T(cx0, 292, "JP1 (1 x 2 header + jumper): +5 V board -> ESP32 5V pin", F(12, True), RED, 'lm')
T(cx0, 306, "fitted: normal; removed: the ESP32 is powered by its USB port", F(12), GRY, 'lm')

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
T(cx0 + 20, 640, "2N2222A (TO-92): the SSR input receives about 4.4 V", F(13), GRY, 'lm')

# flow input
T(cx0, 700, "Flow sensor input (x2)", F(17, True), BLU, 'lm')
L([(cx0 + 20, 735), (cx0 + 250, 735)], RED, 3); T(cx0 + 262, 735, "+5 V", F(13, True), RED, 'lm')
L([(cx0 + 60, 735), (cx0 + 60, 765)], RED, 2)
RR(cx0 + 48, 765, cx0 + 72, 800, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 60, 782, "4.7k", F(10, True))
L([(cx0 + 60, 800), (cx0 + 60, 830)], BLU, 2)
L([(cx0 - 20, 830), (cx0 + 60, 830), (cx0 + 100, 830)], BLU, 3); T(cx0 - 28, 830, "signal J3", F(12, True), BLU, 'rm')
RR(cx0 + 100, 818, cx0 + 150, 842, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 125, 830, "10k", F(11, True))
L([(cx0 + 150, 830), (cx0 + 230, 830)], BLU, 3); T(cx0 + 242, 830, "GPIO", F(13, True), BLU, 'lm')
L([(cx0 + 190, 830), (cx0 + 190, 860)], BLU, 2)
RR(cx0 + 178, 860, cx0 + 202, 895, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 190, 877, "22k", F(11, True))
L([(cx0 + 190, 895), (cx0 + 190, 915)], INK, 2); T(cx0 + 190, 928, "GND", F(12, True))
L([(cx0 + 225, 830), (cx0 + 225, 860)], BLU, 2); L([(cx0 + 215, 860), (cx0 + 235, 860)], INK, 3); L([(cx0 + 215, 868), (cx0 + 235, 868)], INK, 3)
L([(cx0 + 225, 868), (cx0 + 225, 890)], INK, 2); T(cx0 + 225, 904, "1 nF", F(11, True))
T(cx0 + 20, 960, "5 V output sensor: 3.4 V at the GPIO", F(13), GRY, 'lm')
T(cx0 + 20, 982, "open collector (4.7 k pull-up loaded by the divider): 3.0 V", F(13), GRY, 'lm')

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
    "JP1: fitted, the ESP32 takes its 5 V from the board; removed, from its USB port only (never fit it with USB plugged).",
    "The three voltage levels: +5 V board (after fuse and diode), 3.3 V from the ESP32-S3 board, common GND.",
    "The display module has its own backlight transistor: BLK is driven directly by GPIO 14 (stage Q4 optional).",
    "No regulator on the board: the 3.3 V (display, MAX31865, dimmer, encoder) comes from the ESP32-S3.",
    "The pump dimmer stays off the board on the mains side: only its 4-wire I2C cable comes to J8.",
    "All parts are through-hole (TO-92, axial resistors, radial capacitors, DO-41): ordinary soldering iron.",
    "On the board: a ground plane, no copper under the ESP32 antenna, 4 mounting holes (45 x 50 mm).",
    "Silkscreen: name of each connector, pin 1 mark, and the signal of each pin (+5 V, GND, SSR +, SSR −, signal...).",
]
for i, t in enumerate(notes):
    T(60, 1176 + i * 30, "• " + t, F(16), INK, 'lm')

im = im.resize((W, H), Image.LANCZOS)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'board_schematic.png'))
print('ok')
