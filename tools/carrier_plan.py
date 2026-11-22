import os
# -*- coding: utf-8 -*-
"""Top view, to scale, of the carrier board in the box: placement of the parts (not a routed layout)."""
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1760, 1260
K = 12.5                      # px per mm
base = Image.new('RGBA', (W * SS, H * SS), (244, 244, 240, 255))
ov = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(base)
o = ImageDraw.Draw(ov)

def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/%s.ttf' % ('arialbd' if b else 'arial'), int(sz * SS))
def px(x): return x * SS

# the PCB origin on the page and the conversion
OX, OY = 150, 225
def X(mm): return OX + mm * K
def Y(mm): return OY + mm * K

def rect(dr, x0, y0, x1, y1, **k): dr.rectangle([px(x0), px(y0), px(x1), px(y1)], **k)
def rrect(dr, x0, y0, x1, y1, r, **k): dr.rounded_rectangle([px(x0), px(y0), px(x1), px(y1)], px(r), **k)
def circ(dr, cx, cy, r, **k): dr.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], **k)
def line(dr, pts, c, w=2): dr.line([(px(x), px(y)) for x, y in pts], fill=c, width=int(w * SS), joint='curve')
def text(dr, x, y, s, sz=14, c=(30, 30, 36), b=False, a='mm'): dr.text((px(x), px(y)), s, font=F(sz, b), fill=c, anchor=a)

INK = (30, 30, 36); GRY = (110, 110, 116)
MASK = (20, 100, 62); MASK2 = (26, 116, 72)
SILK = (240, 240, 232); PAD = (205, 205, 210); HOLE = (36, 36, 40)

text(d, W / 2, 36, "Carrier board in the enclosure: to-scale placement (top view)", 30, INK, True)
text(d, W / 2, 74, "Proposed component placement: track routing is done afterwards in a CAD tool. Enclosure base, lid removed.", 18, GRY)

# ---------------------------------------------------------------- the box (interior 66 x 80, free area 60 x 70)
INT_W, INT_L = 66.0, 80.0
bx0, by0 = X(-4), Y(-6)
bx1, by1 = bx0 + INT_W * K, by0 + INT_L * K
rrect(d, bx0 - 3 * K, by0 - 3 * K, bx1 + 3 * K, by1 + 3 * K, 14, fill=(52, 52, 58, 255), outline=(30, 30, 34, 255), width=4)
rect(d, bx0, by0, bx1, by1, fill=(74, 74, 82, 255))
# the opening for the USB-C cable in the back wall (y = top)
rect(d, X(5.5), by0 - 3 * K, X(18.5), by0, fill=(20, 20, 24, 255), outline=(230, 230, 235, 255), width=2)
text(d, X(12), by0 - 1.5 * K, "USB-C opening", 12, (230, 230, 235), True)
# the four big posts (lid screws), diameter 8, at the corners of the interior
for (cx, cy) in [(bx0 + 3.6 * K, by0 + 3.6 * K), (bx1 - 3.6 * K, by0 + 3.6 * K), (bx0 + 3.6 * K, by1 - 3.6 * K), (bx1 - 3.6 * K, by1 - 3.6 * K)]:
    circ(d, cx, cy, 4.0 * K, fill=(30, 30, 34, 255), outline=(120, 120, 128, 255), width=3)
    circ(d, cx, cy, 1.1 * K, fill=(70, 70, 78, 255))
# the free area 60 x 70 between the posts
fx0, fy0 = X(-1), Y(-1)
for (xa, ya, xb, yb) in [(fx0, fy0, fx0 + 60 * K, fy0), (fx0, fy0 + 70 * K, fx0 + 60 * K, fy0 + 70 * K), (fx0, fy0, fx0, fy0 + 70 * K), (fx0 + 60 * K, fy0, fx0 + 60 * K, fy0 + 70 * K)]:
    line(d, [(xa, ya), (xb, yb)], (200, 200, 205), 1.5)

# ---------------------------------------------------------------- the board 58 x 68
PW, PL = 58.0, 68.0
rrect(d, X(0) + 6, Y(0) + 8, X(PW) + 6, Y(PL) + 8, 12, fill=(0, 0, 0, 90))          # shadow
rrect(d, X(0), Y(0), X(PW), Y(PL), 2.5 * K / 2.5, fill=MASK + (255,), outline=(8, 60, 36, 255), width=3)
rect(d, X(0.8), Y(0.8), X(PW - 0.8), Y(PL - 0.8), outline=MASK2 + (255,), width=1)

def hole(cx, cy, dia, ring):
    circ(d, X(cx), Y(cy), ring / 2 * K, fill=PAD + (255,), outline=(120, 120, 126, 255), width=1)
    circ(d, X(cx), Y(cy), dia / 2 * K, fill=HOLE + (255,))

def tpad(cx, cy, square=False, ring=1.8, drill=1.0):
    if square:
        rect(d, X(cx) - ring / 2 * K, Y(cy) - ring / 2 * K, X(cx) + ring / 2 * K, Y(cy) + ring / 2 * K, fill=PAD + (255,), outline=(120, 120, 126, 255), width=1)
    else:
        circ(d, X(cx), Y(cy), ring / 2 * K, fill=PAD + (255,), outline=(120, 120, 126, 255), width=1)
    circ(d, X(cx), Y(cy), drill / 2 * K, fill=HOLE + (255,))

def silk(x, y, s, sz=12, a='mm'):
    text(d, X(x), Y(y), s, sz, SILK, True, a)

# mounting holes on the four small standoffs: 45 x 50, centered
MH = [(6.5, 9.0), (51.5, 9.0), (6.5, 59.0), (51.5, 59.0)]
for (cx, cy) in MH:
    hole(cx, cy, 2.7, 5.6)
    circ(d, X(cx), Y(cy), 4.4 * K / 2 + 3, outline=SILK + (255,), width=2)

# ---------------------------------------------------------------- U1: ESP32-S3 sockets (2 x 1x20, pitch 2.54, rows 17.78 apart)
ROW_L, ROW_R = 2.61, 20.39
Y0 = 4.87
for rx in (ROW_L, ROW_R):
    rect(d, X(rx) - 1.27 * K, Y(Y0) - 1.27 * K, X(rx) + 1.27 * K, Y(Y0 + 19 * 2.54) + 1.27 * K, fill=(28, 28, 32, 255), outline=(10, 10, 12, 255), width=1)
    for i in range(20):
        tpad(rx, Y0 + i * 2.54, square=(i == 0 and rx == ROW_L), ring=1.7, drill=1.0)
silk(11.5, 1.2, "U1  ESP32-S3 (2 x 1x20)", 11)
# ---------------------------------------------------------------- under the ESP32 (clearance 8.5 mm): transistors and resistors
def axial(cx, cy, pitch=10.16, label=None):
    x0, x1 = cx - pitch / 2, cx + pitch / 2
    line(d, [(X(x0), Y(cy)), (X(x1), Y(cy))], (190, 190, 196, 255), 2)
    rrect(d, X(cx) - 3.2 / 2 * K * 1.0 * 1.0 - 0.9 * K, Y(cy) - 1.2 * K, X(cx) + 3.2 / 2 * K + 0.9 * K, Y(cy) + 1.2 * K, 6, fill=(214, 190, 140, 255), outline=(120, 90, 40, 255), width=1)
    for xx in (x0, x1):
        tpad(xx, cy, ring=1.8, drill=0.8)
    if label:
        text(d, X(cx), Y(cy) - 2.1 * K * 0.9, label, 9, SILK, True)

def to92(cx, cy, label):
    # three pads at 1.27 pitch, flat face down
    for k in (-1, 0, 1):
        tpad(cx + k * 1.27, cy, ring=1.4, drill=0.8)
    # silkscreen D shape
    line(d, [(X(cx - 2.4), Y(cy - 0.9)), (X(cx + 2.4), Y(cy - 0.9))], SILK + (255,), 2)
    ang = [(cx + 2.4 * __import__('math').cos(__import__('math').radians(t)), cy - 0.9 - 2.4 * __import__('math').sin(__import__('math').radians(t))) for t in range(0, 181, 15)]
    line(d, [(X(a_), Y(b_)) for a_, b_ in ang], SILK + (255,), 2)
    text(d, X(cx), Y(cy + 2.4), label, 10, SILK, True)

# Q1..Q4 and their resistors, in the clear zone between the two socket rows (x 4.5 .. 18.5)
for i, name in enumerate(["Q1", "Q2", "Q3", "Q4"]):
    to92(6.4 + i * 4.0, 15.0, name)
for i, name in enumerate(["R1", "R2", "R3", "R4"]):          # base resistors 1 k
    axial(11.5, 19.5 + i * 3.0, label=name)
for i, name in enumerate(["R5", "R6", "R7", "R8"]):          # base pull-downs 10 k
    axial(11.5, 31.5 + i * 3.0, label=name)
axial(11.5, 43.5, label="R9")                                  # encoder pull-up A
axial(11.5, 46.2, label="R10")                                 # encoder pull-up B

# keep-out under the antenna
for k in range(0, 14):
    line(d, [(X(3.6), Y(49 + k)), (X(19.4), Y(49 + k - 6))], (170, 30, 30, 160), 1)
rect(d, X(3.6), Y(49.0), X(19.4), Y(55), outline=(210, 50, 50, 255), width=2)

# ---------------------------------------------------------------- U2: MAX31865 module socket (1x8) along the left edge of the module
for i in range(8):
    tpad(32.8 + i * 2.54, 27.1, square=(i == 0), ring=1.7, drill=1.0)
rect(d, X(32.8) - 1.27 * K, Y(27.1) - 1.27 * K, X(32.8 + 7 * 2.54) + 1.27 * K, Y(27.1) + 1.27 * K, outline=(20, 20, 24, 255), width=2)
silk(41.7, 25.0, "U2  MAX31865 (1x8)", 11)

# ---------------------------------------------------------------- J5: socket 2 x 4 for the FPC adapter
for r_ in range(2):
    for c_ in range(4):
        tpad(35.5 + c_ * 2.54, 36.0 + r_ * 2.54, square=(r_ == 0 and c_ == 0), ring=1.7, drill=1.0)
rect(d, X(35.5) - 1.5 * K, Y(36.0) - 1.5 * K, X(35.5 + 3 * 2.54) + 1.5 * K, Y(38.54) + 1.5 * K, outline=SILK + (255,), width=2)
silk(40.6, 34.4, "J5  FPC board (2 x 4)", 11)
# two M2 holes for the standoffs of the FPC adapter (positions to be taken from your board)
for (cx, cy) in [(31.0, 33.5), (49.0, 33.5)]:
    hole(cx, cy, 2.2, 4.2)
silk(40, 31.7, "2 x M2 (position to measure)", 9)

# flow input conditioning under the adapter: R11..R16 + C3, C4
for i, name in enumerate(["R11", "R12", "R13", "R14", "R15", "R16"]):
    axial(36.5, 42.5 + i * 2.7, pitch=10.16, label=None)
    text(d, X(42.5), Y(42.5 + i * 2.7), name, 9, SILK, True, 'lm')
for cx, name in [(48.2, "C3"), (48.2, "C4")]:
    pass
for i, name in enumerate(["C3", "C4"]):
    tpad(47.5, 43.0 + i * 3.0, ring=1.6, drill=0.8); tpad(49.5, 43.0 + i * 3.0, ring=1.6, drill=0.8)
    text(d, X(51.0), Y(43.0 + i * 3.0), name, 9, SILK, True, 'lm')

# ---------------------------------------------------------------- front strip: J2 (2x4), J7 (1x6), polyfuse, diode, electrolytic, XH x2
# J2: 2 x 4 right-angle header, SSR + power
for r_ in range(2):
    for c_ in range(4):
        tpad(13.0 + c_ * 2.54, 57.0 + r_ * 2.54, square=(r_ == 0 and c_ == 0), ring=1.7, drill=1.0)
rect(d, X(13.0) - 1.4 * K, Y(57.0) - 1.4 * K, X(13.0 + 3 * 2.54) + 1.4 * K, Y(59.54) + 1.4 * K, outline=SILK + (255,), width=2)
silk(17.5, 54.8, "J2  SSRs + 5 V (2 x 4)", 10)
for c_, lab in enumerate(["+5V", "P+", "B+", "V+"]):
    text(d, X(13.0 + c_ * 2.54), Y(57.0) - 1.9 * K, lab, 8, SILK, True)
for c_, lab in enumerate(["GND", "P−", "B−", "V−"]):
    text(d, X(13.0 + c_ * 2.54), Y(59.54) + 1.9 * K, lab, 8, SILK, True)
# J7: 1 x 6 right-angle header, button and encoder
for i in range(6):
    tpad(25.0 + i * 2.54, 58.2, square=(i == 0), ring=1.7, drill=1.0)
rect(d, X(25.0) - 1.4 * K, Y(58.2) - 1.4 * K, X(25.0 + 5 * 2.54) + 1.4 * K, Y(58.2) + 1.4 * K, outline=SILK + (255,), width=2)
silk(31.5, 55.4, "J7  button + encoder (1 x 6)", 10)
for i, lab in enumerate(["BT", "G", "5V", "G", "A", "B"]):
    text(d, X(25.0 + i * 2.54), Y(58.2) + 2.1 * K, lab, 8, SILK, True)
# J8: 1 x 4 vertical header, dimmer (UART / I2C) in the corridor between ESP32 and FPC board; J9: 1 x 3, pressure sensor
for i, lab in enumerate(["3V3", "GND", "SDA", "SCL"]):
    tpad(25.5, 33.0 + i * 2.54, square=(i == 0), ring=1.7, drill=1.0)
    text(d, X(27.0), Y(33.0 + i * 2.54), lab, 7, SILK, True, 'lm')
rect(d, X(25.5) - 1.4 * K, Y(33.0) - 1.4 * K, X(25.5) + 1.4 * K, Y(33.0 + 3 * 2.54) + 1.4 * K, outline=SILK + (255,), width=2)
silk(25.0, 31.4, "J8 dimmer", 8)
for i, lab in enumerate(["5V", "GND", "SIG"]):
    tpad(25.5, 43.2 + i * 2.54, square=(i == 0), ring=1.7, drill=1.0)
    text(d, X(27.0), Y(43.2 + i * 2.54), lab, 7, SILK, True, 'lm')
rect(d, X(25.5) - 1.4 * K, Y(43.2) - 1.4 * K, X(25.5) + 1.4 * K, Y(43.2 + 2 * 2.54) + 1.4 * K, outline=SILK + (255,), width=2)
silk(25.0, 41.5, "J9 pressure", 8)
# F1 polyfuse (radial, pitch 5), D1 1N5819 (axial 10.16), C1 470 uF (radial 5 mm dia, pitch 2.5), C2 100 nF
tpad(3.0, 65.0, ring=1.8, drill=0.9); tpad(8.0, 65.0, ring=1.8, drill=0.9)
rrect(d, X(1.9), Y(63.4), X(9.1), Y(66.6), 6, outline=SILK + (255,), width=2); silk(5.5, 61.9, "F1 1,1 A", 9)
axial(18.0, 64.2, pitch=10.16); text(d, X(18.0), Y(64.2) - 2.1 * K, "D1", 9, SILK, True)
circ(d, X(27.0), Y(64.0), 3.15 * K, fill=None, outline=SILK + (255,), width=2)
tpad(25.75, 64.0, ring=1.8, drill=0.8); tpad(28.25, 64.0, ring=1.8, drill=0.8); silk(27.0, 61.2, "C1", 9)
tpad(12.5, 66.8, ring=1.6, drill=0.8); tpad(15.0, 66.8, ring=1.6, drill=0.8); silk(13.8, 62.2, "C2", 9)
# XH x2 (side entry, 3 pins 2.5 pitch)
for k, (x0, name) in enumerate([(32.0, "J3  flow In"), (41.5, "J4  flow Out")]):
    for i in range(3):
        tpad(x0 + i * 2.5, 62.8, square=(i == 0), ring=1.8, drill=1.0)
    rect(d, X(x0) - 1.9 * K, Y(62.8) - 1.8 * K, X(x0 + 5) + 1.9 * K, Y(62.8) + 4.6 * K, outline=SILK + (255,), width=2)
    text(d, X(x0 + 2.5), Y(62.8) - 2.9 * K, name, 9, SILK, True)

# silkscreen title
silk(46.0, 66.6, "ESP32-S3 / SSR  rev A", 9)

# ---------------------------------------------------------------- the raised boards, translucent (they hide nothing)
# ESP32-S3 board 21 x 52 at x 1..22, y 3..55
rrect(o, px(X(1.0)) / SS, px(Y(3.0)) / SS, px(X(22.0)) / SS, px(Y(55.0)) / SS, 6, fill=(240, 240, 248, 120), outline=(240, 240, 248, 255), width=3)
rect(o, px(X(7.5)) / SS, px(Y(1.7)) / SS, px(X(15.5)) / SS, px(Y(7.0)) / SS, fill=(190, 194, 200, 200), outline=(120, 124, 130, 255), width=2)
text(o, X(11.5), Y(10.2), "ESP32-S3   21 x 52  (at 8.5 mm)", 11, (60, 60, 70), True)
text(o, X(11.5), Y(51.8), "antenna zone: nothing underneath", 10, (150, 30, 30), True)
text(o, X(11.5), Y(4.5), "USB-C", 10, (60, 60, 70), True)
# MAX31865 module 25 x 28 at x 29..54, y 2..30
rrect(o, px(X(29.0)) / SS, px(Y(2.0)) / SS, px(X(54.4)) / SS, px(Y(29.9)) / SS, 6, fill=(20, 80, 170, 150), outline=(150, 190, 250, 255), width=3)
rect(o, px(X(33.3)) / SS, px(Y(2.4)) / SS, px(X(50.5)) / SS, px(Y(9.5)) / SS, fill=(46, 104, 180, 220), outline=(180, 210, 250, 255), width=2)
text(o, X(41.7), Y(14.5), "MAX31865", 15, (235, 240, 255), True)
text(o, X(41.7), Y(17.0), "25.4 x 27.9, height 15", 11, (220, 232, 255))
text(o, X(41.9), Y(6.0), "PT100 terminal", 10, (235, 240, 255), True)
# FPC adapter board ~22 x 28 at x 29..51, y 32..60
rrect(o, px(X(29.0)) / SS, px(Y(30.4)) / SS, px(X(51.0)) / SS, px(Y(56.9)) / SS, 6, fill=(22, 150, 80, 130), outline=(150, 240, 190, 255), width=3)
rect(o, px(X(35.0)) / SS, px(Y(49.0)) / SS, px(X(45.0)) / SS, px(Y(54.5)) / SS, fill=(236, 236, 228, 230), outline=(120, 120, 110, 255), width=2)
text(o, X(40.0), Y(51.8), "FPC connector", 10, (50, 50, 44), True)
text(o, X(40.0), Y(47.0), "FPC board ~22 x 26 (at 8.5 mm)", 10, (230, 255, 240), True)
base = Image.alpha_composite(base, ov)
d = ImageDraw.Draw(base)

# ---------------------------------------------------------------- dimensions
def dim_h(x0, x1, y, label):
    line(d, [(X(x0), Y(y)), (X(x1), Y(y))], (60, 60, 66), 2)
    for xx in (x0, x1):
        line(d, [(X(xx), Y(y) - 8), (X(xx), Y(y) + 8)], (60, 60, 66), 2)
    text(d, X((x0 + x1) / 2), Y(y) - 12, label, 13, (50, 50, 56), True)
def dim_v(x, y0, y1, label):
    line(d, [(X(x), Y(y0)), (X(x), Y(y1))], (60, 60, 66), 2)
    for yy in (y0, y1):
        line(d, [(X(x) - 8, Y(yy)), (X(x) + 8, Y(yy))], (60, 60, 66), 2)
    d.text((px(X(x) - 14), px(Y((y0 + y1) / 2))), label, font=F(13, True), fill=(50, 50, 56), anchor='rm')
dim_h(0, 58, 70.6, "58 mm")
dim_v(-7.2, 0, 68, "68 mm")

# ---------------------------------------------------------------- legend, to the right
lx = 1010
text(d, lx, 140, "Legend", 22, INK, True, 'lm')
leg = [
    ((205, 205, 210), "through-hole pad (1 mm hole)"),
    ((240, 240, 232), "silkscreen: connector marks and orientation"),
    ((240, 240, 248), "ESP32-S3 board, raised 8.5 mm"),
    ((20, 80, 170), "MAX31865 module, raised 3 mm"),
    ((22, 150, 80), "FPC board, raised 8.5 mm"),
    ((210, 50, 50), "keep-out under the antenna"),
]
for i, (c, t) in enumerate(leg):
    y = 180 + i * 34
    rect(d, lx, y - 10, lx + 26, y + 10, fill=c, outline=(40, 40, 44), width=1)
    text(d, lx + 40, y, t, 16, INK, False, 'lm')

text(d, lx, 410, "Components", 22, INK, True, 'lm')
comp = [
    "U1  2 female 1 x 20 sockets (ESP32-S3 board)",
    "U2  low 1 x 8 socket (MAX31865 module)",
    "J2  right-angle 2 x 4 header: SSRs and 5 V supply",
    "J3, J4  JST XH 3-pin: flow sensors In and Out",
    "J5  2 x 4 socket: FPC adapter board",
    "J7  right-angle 1 x 6 header: button and encoder (5 V)",
    "J8  1 x 4: pump dimmer (I2C)  ·  J9  1 x 3: pressure sensor",
    "Q1 to Q3  SSR drive ; Q4  backlight (2N2222A)",
    "R1 to R4  1 kΩ  ·  R5 to R8  10 kΩ  ·  R9, R10  encoder dividers",
    "R11 to R16  flow sensor inputs  ·  C3, C4  1 nF",
    "F1  1.1 A resettable fuse  ·  D1  1N5819",
    "C1  470 µF  ·  C2  100 nF",
]
for i, t in enumerate(comp):
    text(d, lx, 450 + i * 30, t, 15, INK, False, 'lm')

text(d, lx, 810, "Heights (enclosure floor = 0)", 22, INK, True, 'lm')
hs = [
    "posts 3 + board 1.6 = 4.6 mm",
    "ESP32 on 8.5 mm sockets: USB-C at 17.9 mm",
    "FPC board on 8.5 mm sockets: 17.7 mm",
    "MAX31865 on 3 mm sockets: 22.6 mm",
    "usable depth: 25 mm: margin 2.4 mm",
    "electrolytic C1: about 15.6 mm",
]
for i, t in enumerate(hs):
    text(d, lx, 850 + i * 30, t, 15, INK if i != 4 else (20, 110, 60), i == 4, 'lm')

text(d, lx, 1060, "Points to check on your board:", 18, (190, 40, 40), True, 'lm')
chk = [
    "one mounting hole (top right) passes under the MAX31865: flat-head screw,",
    "1.5 mm high at most, under the module's 3 mm;",
    "positions of the 2 M2 holes of the FPC board; pin order of J5, J6 and J7.",
]
for i, t in enumerate(chk):
    text(d, lx, 1092 + i * 26, t, 15, INK, False, 'lm')

out = base.resize((W, H), Image.LANCZOS).convert('RGB')
out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'carrier_plan.png'))
print('ok')
