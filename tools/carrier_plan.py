import os
# -*- coding: utf-8 -*-
"""Top view, to scale, of the carrier board in the box: placement of the parts (not a routed layout)."""
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1760, 1340
K = 12.5                      # px per mm
base = Image.new('RGBA', (W * SS, H * SS), (244, 244, 240, 255))
ov = Image.new('RGBA', (W * SS, H * SS), (0, 0, 0, 0))
d = ImageDraw.Draw(base)
o = ImageDraw.Draw(ov)

def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/%s.ttf' % ('arialbd' if b else 'arial'), int(sz * SS))
def px(x): return x * SS

# the PCB origin on the page and the conversion
OX, OY = 150, 262
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

# ---------------------------------------------------------------- the box (interior 60 x 85, posts 8 x 8 in the corners)
INT_W, INT_L = 60.0, 85.0
bx0, by0 = X(-1), Y(-8.5)
bx1, by1 = bx0 + INT_W * K, by0 + INT_L * K
rrect(d, bx0 - 3 * K, by0 - 3 * K, bx1 + 3 * K, by1 + 3 * K, 14, fill=(52, 52, 58, 255), outline=(30, 30, 34, 255), width=4)
rect(d, bx0, by0, bx1, by1, fill=(74, 74, 82, 255))
# the opening for the USB-C cable in the back wall (y = top)
rect(d, X(5.5), by0 - 3 * K, X(18.5), by0, fill=(20, 20, 24, 255), outline=(230, 230, 235, 255), width=2)
text(d, X(12), by0 - 1.5 * K, "USB-C opening", 12, (230, 230, 235), True)
# the four big posts (lid screws): 8 x 8 mm in the corners of the interior. They leave a plus-shaped usable area:
# 60 wide over 69 long, and 44 wide over the full 85 length.
for (xa, xb, ya, yb) in [(-1, 7, -8.5, -0.5), (51, 59, -8.5, -0.5), (-1, 7, 68.5, 76.5), (51, 59, 68.5, 76.5)]:
    rrect(d, X(xa), Y(ya), X(xb), Y(yb), 8, fill=(30, 30, 34, 255), outline=(120, 120, 128, 255), width=3)
    circ(d, (X(xa) + X(xb)) / 2, (Y(ya) + Y(yb)) / 2, 1.6 * K, fill=(70, 70, 78, 255))
cross = [(-1, -0.5), (7, -0.5), (7, -8.5), (51, -8.5), (51, -0.5), (59, -0.5), (59, 68.5), (51, 68.5), (51, 76.5), (7, 76.5), (7, 68.5), (-1, 68.5)]
line(d, [(X(a), Y(b)) for a, b in cross + [cross[0]]], (150, 200, 150), 2)
text(d, X(29), Y(-4.5), "back extension (not used)", 10, (150, 220, 150), True)

# ---------------------------------------------------------------- the board 58 x 68
PW, PL = 58.0, 68.0
rrect(d, X(0) + 6, Y(0) + 8, X(PW) + 6, Y(PL) + 8, 12, fill=(0, 0, 0, 90))          # shadow
rrect(d, X(0), Y(0), X(PW), Y(PL), 2.5 * K / 2.5, fill=MASK + (255,), outline=(8, 60, 36, 255), width=3)
rect(d, X(0.8), Y(0.8), X(PW - 0.8), Y(PL - 0.8), outline=MASK2 + (255,), width=1)
# front tab of the board (42 x 7) on the cable side, in the central extension
rect(d, X(8) + 6, Y(PL) + 4, X(50) + 6, Y(75) + 8, fill=(0, 0, 0, 90))
rect(d, X(8), Y(PL) - 5, X(50), Y(75), fill=MASK + (255,))
line(d, [(X(8), Y(PL)), (X(8), Y(75)), (X(50), Y(75)), (X(50), Y(PL))], (8, 60, 36, 255), 3)

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
to92(11.5, 9.0, "Q5")                                           # spare output stage (2N2222A)
# spare I/O conditioning, flat resistors under the MAX31865 (3 mm clearance): R17 4.7 k + R18 10 k (input divider), R19 1 k base, R20 4.7 k pull-up to 5 V, R21 10 k base to GND
for i, name in enumerate(["R17", "R18", "R19", "R20", "R21"]):
    axial(41.7, 35.5 + i * 2.7, pitch=10.16, label=None)
    text(d, X(47.6), Y(35.5 + i * 2.7), name, 8, SILK, True, 'lm')

# keep-out under the antenna
for k in range(0, 12):
    line(d, [(X(3.6), Y(49 + k)), (X(19.4), Y(49 + k - 6))], (170, 30, 30, 160), 1)
rect(d, X(3.6), Y(49.0), X(19.4), Y(57), outline=(210, 50, 50, 255), width=2)

# ---------------------------------------------------------------- U2: MAX31865 module socket (1x8), module rotated 180 degrees:
# header on the rear edge of the module (pin 1 VIN on the right), PT100 terminal block facing the front
for i in range(8):
    tpad(32.8 + i * 2.54, 31.6, square=(i == 7), ring=1.7, drill=1.0)
rect(d, X(32.8) - 1.27 * K, Y(31.6) - 1.27 * K, X(32.8 + 7 * 2.54) + 1.27 * K, Y(31.6) + 1.27 * K, outline=(20, 20, 24, 255), width=2)
silk(41.7, 29.9, "U2  MAX31865 (1x8, pin 1 VIN on the right)", 10)

# ---------------------------------------------------------------- J5: socket 2 x 4 for the FPC adapter (board at the top right, rotated 180: connector towards the front)
for r_ in range(2):
    for c_ in range(4):
        tpad(35.5 + c_ * 2.54, 7.6 + r_ * 2.54, square=(r_ == 0 and c_ == 0), ring=1.7, drill=1.0)
rect(d, X(35.5) - 1.5 * K, Y(7.6) - 1.5 * K, X(35.5 + 3 * 2.54) + 1.5 * K, Y(10.14) + 1.5 * K, outline=SILK + (255,), width=2)
silk(41.0, 5.6, "J5  FPC board (2 x 4)", 10)
# two M2 holes for the standoffs of the FPC adapter (positions to be taken from your board)
for (cx, cy) in [(31.0, 5.1), (49.0, 5.1)]:
    hole(cx, cy, 2.2, 4.2)
silk(40, 3.6, "2 x M2 (to measure)", 9)

# flow input conditioning under the adapter: R11..R16 (two columns of three, pitch 7.62) + C3, C4
for i, name in enumerate(["R11", "R12", "R13", "R14", "R15", "R16"]):
    cx_ = 34.3 if i < 3 else 44.9
    cy_ = 13.8 + (i % 3) * 2.6
    axial(cx_, cy_, pitch=7.62, label=None)
    text(d, X(cx_), Y(cy_) - 1.6 * K, name, 8, SILK, True)
for i, name in enumerate(["C3", "C4"]):
    tpad(52.4, 15.0 + i * 3.0, ring=1.6, drill=0.8); tpad(54.4, 15.0 + i * 3.0, ring=1.6, drill=0.8)
    text(d, X(56.0), Y(15.0 + i * 3.0), name, 8, SILK, True, 'lm')

# ---------------------------------------------------------------- front strip: J2 (2x4), J7 (1x6), polyfuse, diode, electrolytic, XH x2
# Front edge: every right-angle header has its Dupont housings plugged in towards the front (about 9 mm of keep-out in front of the pads).
# J2: 2 x 4 right-angle header, SSR + power (housing keep-out x 11.7 .. 21.9)
for r_ in range(2):
    for c_ in range(4):
        tpad(12.2 + c_ * 2.54, 61.0 + r_ * 2.54, square=(r_ == 0 and c_ == 0), ring=1.7, drill=1.0)
rect(d, X(12.2) - 1.4 * K, Y(61.0) - 1.4 * K, X(12.2 + 3 * 2.54) + 1.4 * K, Y(63.54) + 1.4 * K, outline=SILK + (255,), width=2)
silk(15.4, 58.4, "J2  SSRs + 5 V", 9)
for c_, lab in enumerate(["+5V", "P+", "B+", "V+"]):
    text(d, X(12.2 + c_ * 2.54), Y(61.0) - 1.9 * K, lab, 8, SILK, True)
for c_, lab in enumerate(["GND", "P−", "B−", "V−"]):
    text(d, X(12.2 + c_ * 2.54), Y(63.54) + 1.9 * K, lab, 8, SILK, True)
# J7: 2 x 6 right-angle header (two stacked rows of housings): button, encoder, and 4 spare pins (+5 V, IN, OUT, GND)
# row A (top): BT, GND | +5 V, IN38, OUT39, GND      row B (bottom): +5 V, GND, A, B
for c_ in range(6):
    tpad(22.4 + c_ * 2.54, 61.0, square=(c_ == 0), ring=1.7, drill=1.0)
for c_ in range(4):
    tpad(22.4 + c_ * 2.54, 63.54, ring=1.7, drill=1.0)
rect(d, X(22.4) - 1.4 * K, Y(61.0) - 1.4 * K, X(22.4 + 5 * 2.54) + 1.4 * K, Y(63.54) + 1.4 * K, outline=SILK + (255,), width=2)
silk(31.0, 58.4, "J7  button / encoder / spare I/O", 9)
for c_, lab in enumerate(["BT", "GND", "5V", "IN", "OUT", "GND"]):
    text(d, X(22.4 + c_ * 2.54), Y(61.0) - 1.9 * K, lab, 7, SILK, True)
for c_, lab in enumerate(["5V", "GND", "A", "B"]):
    text(d, X(22.4 + c_ * 2.54), Y(63.54) + 1.9 * K, lab, 7, SILK, True)
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
# F1 polyfuse (radial, pitch 5) and D1 1N5819 (standing) in the front-left corner, in front of the mounting hole
tpad(3.0, 66.0, ring=1.8, drill=0.9); tpad(8.0, 66.0, ring=1.8, drill=0.9)
rrect(d, X(1.9), Y(64.4), X(9.1), Y(67.6), 6, outline=SILK + (255,), width=2); text(d, X(10.4), Y(66.0), "F1", 8, SILK, True, 'lm')
tpad(2.5, 62.6, ring=1.8, drill=0.8); tpad(5.04, 62.6, ring=1.8, drill=0.8)
text(d, X(6.6), Y(62.6), "D1", 8, SILK, True, 'lm')
# C1 470 uF (radial 6.3 mm) and C2 100 nF, in the corridor between ESP32 and MAX31865
circ(d, X(25.7), Y(54.3), 3.15 * K, fill=None, outline=SILK + (255,), width=2)
tpad(24.45, 54.3, ring=1.8, drill=0.8); tpad(26.95, 54.3, ring=1.8, drill=0.8); silk(25.7, 54.3, "C1", 9)
tpad(24.5, 50.4, ring=1.6, drill=0.8); tpad(27.0, 50.4, ring=1.6, drill=0.8); silk(25.7, 49.2, "C2", 8) if False else text(d, X(28.4), Y(50.4), "C2", 8, SILK, True, 'lm')
# JST XH x2: vertical headers, rotated (pins along y), the plugs come out upwards: no keep-out towards the front
for k, (x0, name) in enumerate([(39.6, "J3 flow In"), (45.6, "J4 flow Out")]):
    for i in range(3):
        tpad(x0, 61.5 + i * 2.5, square=(i == 0), ring=1.8, drill=1.0)
    rect(d, X(x0) - 2.9 * K, Y(61.5) - 2.1 * K, X(x0) + 2.9 * K, Y(66.5) + 2.1 * K, outline=SILK + (255,), width=2)
    text(d, X(x0), Y(66.5) + 3.4 * K, name, 8, SILK, True)

# silkscreen title
silk(53.0, 66.6, "rev A", 9)

# ---------------------------------------------------------------- the raised boards, translucent (they hide nothing)
# ESP32-S3 board 21 x 52 at x 1..22, y 3..55
rrect(o, px(X(0.5)) / SS, px(Y(3.0)) / SS, px(X(22.5)) / SS, px(Y(57.0)) / SS, 6, fill=(240, 240, 248, 120), outline=(240, 240, 248, 255), width=3)
rect(o, px(X(7.5)) / SS, px(Y(1.7)) / SS, px(X(15.5)) / SS, px(Y(7.0)) / SS, fill=(190, 194, 200, 200), outline=(120, 124, 130, 255), width=2)
text(o, X(11.5), Y(10.2), "ESP32-S3   ~22 x 54  (at 8.5 mm)", 11, (60, 60, 70), True)
text(o, X(11.5), Y(53.5), "antenna zone: nothing underneath", 10, (150, 30, 30), True)
text(o, X(11.5), Y(4.5), "USB-C", 10, (60, 60, 70), True)
# MAX31865 module 25.4 x 27.9 at x 29..54.4, y 28.8..56.7, rotated 180 degrees (terminal block at the front)
rrect(o, px(X(29.0)) / SS, px(Y(28.8)) / SS, px(X(54.4)) / SS, px(Y(56.7)) / SS, 6, fill=(20, 80, 170, 150), outline=(150, 190, 250, 255), width=3)
rect(o, px(X(33.3)) / SS, px(Y(49.2)) / SS, px(X(50.5)) / SS, px(Y(56.3)) / SS, fill=(46, 104, 180, 220), outline=(180, 210, 250, 255), width=2)
text(o, X(41.7), Y(34.0), "MAX31865   25.4 x 27.9, height 15", 11, (235, 240, 255), True)
text(o, X(41.9), Y(52.7), "PT100 terminal (wires exit to the front)", 10, (235, 240, 255), True)
# FPC adapter board ~22 x 26.5 at x 29..51, y 2..28.5 (rotated 180: connector towards the front, ribbon goes over the MAX31865)
rrect(o, px(X(29.0)) / SS, px(Y(2.0)) / SS, px(X(51.0)) / SS, px(Y(28.5)) / SS, 6, fill=(22, 150, 80, 130), outline=(150, 240, 190, 255), width=3)
rect(o, px(X(35.0)) / SS, px(Y(22.9)) / SS, px(X(45.0)) / SS, px(Y(28.4)) / SS, fill=(236, 236, 228, 230), outline=(120, 120, 110, 255), width=2)
text(o, X(40.0), Y(25.6), "FPC connector (ribbon to the front)", 9, (50, 50, 44), True)
text(o, X(40.0), Y(20.6), "FPC board ~22 x 26 (at 8.5 mm)", 10, (230, 255, 240), True)
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
dim_h(0, 58, 82.6, "58 mm (tab 42 x 7 at the front)")
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
    "J7  right-angle 2 x 6 header: button, encoder (5 V), 4 spare I/O pins",
    "J8  1 x 4: pump dimmer (I2C)  ·  J9  1 x 3: pressure sensor",
    "Q1 to Q3  SSR drive ; Q4  backlight (2N2222A)",
    "R1 to R4  1 kΩ  ·  R5 to R8  10 kΩ  ·  R9, R10, R17, R18  5 V input dividers",
    "Q5, R19 to R21  spare output stage (3.3 V to 5 V)",
    "R11 to R16  flow sensor inputs  ·  C3, C4  1 nF",
    "F1  1.1 A resettable fuse  ·  D1  1N5819",
    "C1  470 µF  ·  C2  100 nF",
]
for i, t in enumerate(comp):
    text(d, lx, 440 + i * 27, t, 15, INK, False, 'lm')

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
    "the FPC ribbon goes over the MAX31865 (about 23.5 mm, 1 mm under the 25 mm limit);",
    "PT100 wires leave at the front above J7 / J3 / J4, at about 14 mm;",
    "Dupont housings end at the front wall (the board has a 42 x 7 tab there); cable slot in the wall;",
    "M2 holes and pin-1 orientation of the FPC board; pin order of J5, J6 and J7.",
]
for i, t in enumerate(chk):
    text(d, lx, 1092 + i * 26, t, 15, INK, False, 'lm')

out = base.resize((W, H), Image.LANCZOS).convert('RGB')
out.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'carrier_plan.png'))
print('ok')
