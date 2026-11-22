import os
# -*- coding: utf-8 -*-
import math
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 2000, 1150
im = Image.new('RGB', (W * SS, H * SS), (244, 244, 240))
d = ImageDraw.Draw(im)
s = 7.6                      # px per mm
OX, OY = 1000, 240            # screen position of the origin (back corner of the tray at floor level)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))

def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/%s.ttf' % ('arialbd' if b else 'arial'), sz * SS)

def P(x, y, z):
    """x to the right-down, y to the left-down, z up (mm) -> pixels (supersampled)."""
    return ((OX + (x - y) * C30 * s) * SS, (OY + (x + y) * S30 * s - z * s) * SS)

def poly(pts, fill, outline=None, w=1):
    d.polygon([P(*p) for p in pts], fill=fill, outline=outline)
    if outline:
        d.line([P(*p) for p in pts] + [P(*pts[0])], fill=outline, width=w * SS)

def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)

def cuboid(x, y, z, w, dp, h, color, outline=(20, 20, 24)):
    """Three visible faces: top, +x face, +y face."""
    poly([(x, y, z + h), (x + w, y, z + h), (x + w, y + dp, z + h), (x, y + dp, z + h)], shade(color, 1.12), outline)
    poly([(x + w, y, z), (x + w, y + dp, z), (x + w, y + dp, z + h), (x + w, y, z + h)], shade(color, 0.85), outline)
    poly([(x, y + dp, z), (x + w, y + dp, z), (x + w, y + dp, z + h), (x, y + dp, z + h)], shade(color, 0.68), outline)

def text(x, y, t, size=18, color=(30, 30, 36), bold=False, anchor='lm'):
    d.text((x * SS, y * SS), t, font=F(size, bold), fill=color, anchor=anchor)

def label(px, py, tx, ty, t, color=(30, 30, 36), size=17):
    """Text at (tx, ty) with a leader to the screen point (px, py) given as a P() result."""
    d.line([(px, py), (tx * SS, ty * SS)], fill=color, width=2 * SS)
    d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS], fill=color)
    text(tx + (8 if tx > 0 else 0), ty, t, size, color, True, 'lm' if tx >= px / SS else 'rm')

# ---------------------------------------------------------------- dimensions (mm)
WALL = 3.0
INT_X, INT_Y = 66.0, 80.0           # interior: x across, y along (the long side)
BX, BY = INT_X + 2 * WALL, INT_Y + 2 * WALL
BASE_H = 16.0                        # height of the base half (the walls)
FLOOR = 2.0

PLASTIC = (58, 58, 66)
text(W / 2, 40, "Enclosure view: the carrier board with its connectors (the display is remote)", 30, bold=True, anchor='mm')
text(W / 2, 80, "Enclosure base, lid removed. Scaled concept drawing following the placement plan: not a board layout.", 20, (110, 110, 116), anchor='mm')

# ---------------------------------------------------------------- the base (open tray)
# floor
poly([(0, 0, FLOOR), (BX, 0, FLOOR), (BX, BY, FLOOR), (0, BY, FLOOR)], shade(PLASTIC, 0.95), (20, 20, 24))
# inner faces of the two back walls (visible from inside)
poly([(WALL, WALL, FLOOR), (BX - WALL, WALL, FLOOR), (BX - WALL, WALL, BASE_H), (WALL, WALL, BASE_H)], shade(PLASTIC, 0.78), (20, 20, 24))
poly([(WALL, WALL, FLOOR), (WALL, BY - WALL, FLOOR), (WALL, BY - WALL, BASE_H), (WALL, WALL, BASE_H)], shade(PLASTIC, 0.9), (20, 20, 24))
# the opening for the USB-C cable in the back wall y = 0 (seen on its inner face)
ux0 = WALL + 9.0
poly([(ux0, WALL, 7), (ux0 + 12, WALL, 7), (ux0 + 12, WALL, 15), (ux0, WALL, 15)], (14, 14, 18), (230, 230, 235), 2)
# top of the back walls
poly([(0, 0, BASE_H), (BX, 0, BASE_H), (BX - WALL, WALL, BASE_H), (WALL, WALL, BASE_H)], shade(PLASTIC, 1.25), (20, 20, 24))
poly([(0, 0, BASE_H), (0, BY, BASE_H), (WALL, BY - WALL, BASE_H), (WALL, WALL, BASE_H)], shade(PLASTIC, 1.2), (20, 20, 24))
# the four big posts at the corners (lid screws)
for (px, py) in [(WALL + 3.5, WALL + 3.5), (BX - WALL - 3.5, WALL + 3.5), (WALL + 3.5, BY - WALL - 3.5), (BX - WALL - 3.5, BY - WALL - 3.5)]:
    cuboid(px - 3.4, py - 3.4, FLOOR, 6.8, 6.8, BASE_H - FLOOR, (40, 40, 46))

# ---------------------------------------------------------------- the carrier and what it holds
CX0, CY0 = WALL + 4.0, WALL + 6.0     # origin of the carrier (58 x 68)
PCB_Z = FLOOR + 3.0                   # on the four small standoffs of 3 mm
PCBT = 1.6
top = PCB_Z + PCBT
items = []
def add(x, y, z, w, dp, h, color):
    items.append(((x + w / 2) + (y + dp / 2) + z * 0.001, lambda x=x, y=y, z=z, w=w, dp=dp, h=h, color=color: cuboid(x, y, z, w, dp, h, color)))

# the standoffs (3 mm), 45 x 50 apart, then the carrier slab itself: they are under it, it is under everything else
sx0 = CX0 + (58 - 45) / 2
sy0 = CY0 + (68 - 50) / 2
for (ax, ay) in [(sx0, sy0), (sx0 + 45, sy0), (sx0, sy0 + 50), (sx0 + 45, sy0 + 50)]:
    cuboid(ax - 2.4, ay - 2.4, FLOOR, 4.8, 4.8, 3.0, (36, 36, 42))
cuboid(CX0, CY0, PCB_Z, 58, 68, PCBT, (22, 110, 66))

GOLD = (214, 178, 70)
BLACK = (24, 24, 28)
WHITE = (238, 236, 226)

# ESP32-S3 (21 x 52) on sockets of 8.5 mm, at the left; USB-C towards the back wall
ex, ey = CX0 + 1, CY0 + 3
add(ex, ey + 1, top, 2.4, 50, 8.5, BLACK); add(ex + 21 - 2.4, ey + 1, top, 2.4, 50, 8.5, BLACK)
add(ex, ey, top + 8.5, 21, 52, 1.6, (236, 236, 242))
add(ex + 5.5, ey - 1.3, top + 8.5 + 1.6, 10, 7.5, 3.2, (190, 194, 200))     # USB-C
add(ex + 6, ey + 14, top + 8.5 + 1.6, 9, 9, 1.0, BLACK)                     # the module (shield)
add(ex + 3, ey + 43, top + 8.5 + 1.6, 15, 8, 0.8, (236, 226, 196))          # antenna
# MAX31865 (25.4 x 27.9, 15 high) on low sockets of 3 mm, rotated 180 degrees: header at the rear, PT100 terminal at the front
mx, my = CX0 + 29, CY0 + 28.8
add(mx + 3.8, my + 1.4, top, 19.0, 2.5, 3.0, BLACK)
add(mx, my, top + 3.0, 25.4, 27.9, 1.6, (130, 30, 40))                      # Adafruit board is red-purple
add(mx + 4.2, my + 20.5, top + 3.0 + 1.6, 17.0, 7.0, 10.4, (46, 120, 190))  # PT100 terminal block (blue)
add(mx + 9.4, my + 9.9, top + 3.0 + 1.6, 7, 7, 1.6, BLACK)                  # the MAX31865 chip
# the FPC adapter board (~22 x 26.5) on a 2 x 4 header, at the top right, FPC connector towards the back wall
ax0, ay0 = CX0 + 29, CY0 + 2
HDR = 8.5
add(ax0 + 6.5, ay0 + 15.8, top, 10.2, 5.1, HDR, BLACK)                      # 2 x 4 header + socket
add(ax0, ay0, top + HDR, 22, 26.5, 1.6, (22, 130, 70))
add(ax0 + 6, ay0 + 2.0, top + HDR + 1.6, 10, 5.5, 2.6, WHITE)               # its FPC connector
add(ax0 + 1.0, ay0 + 19.9, top, 3.5, 3.5, HDR, (110, 110, 118))             # standoffs under the mounting holes
add(ax0 + 17.5, ay0 + 19.9, top, 3.5, 3.5, HDR, (110, 110, 118))

# J8 (dimmer, 1 x 4) and J9 (pressure, 1 x 3): straight headers in the corridor, plugs seated on top
J8X, J8Y = CX0 + 25.5 - 1.27, CY0 + 33.0 - 1.27
J9X, J9Y = CX0 + 25.5 - 1.27, CY0 + 43.2 - 1.27
add(J8X, J8Y, top, 2.54, 10.16, 2.5, BLACK); add(J8X + 0.2, J8Y + 0.2, top + 2.5, 2.14, 9.76, 8.0, WHITE)
add(J9X, J9Y, top, 2.54, 7.62, 2.5, BLACK); add(J9X + 0.2, J9Y + 0.2, top + 2.5, 2.14, 7.22, 8.0, WHITE)
# J2 (2 x 4 right-angle, rows stacked vertically) and four 2-pin housings plugged in from the front
add(CX0 + 13 - 1.27, CY0 + 56.0, top, 10.16, 5.6, 5.9, BLACK)
for k in range(4):
    add(CX0 + 13 - 1.27 + k * 2.54 + 0.15, CY0 + 61.6, top + 0.4, 2.24, 8.6, 5.1, WHITE)
# J7 (1 x 6 right-angle): a 2-pin housing (button) and a 4-pin housing (encoder)
add(CX0 + 25 - 1.27, CY0 + 56.8, top, 15.24, 3.0, 2.5, BLACK)
add(CX0 + 25 - 1.27 + 0.15, CY0 + 59.8, top + 0.2, 4.78, 8.6, 2.1, WHITE)
add(CX0 + 25 - 1.27 + 5.08 + 0.15, CY0 + 59.8, top + 0.2, 9.86, 8.6, 2.1, WHITE)
# two transistors' worth of small parts at the front: polyfuse, diode, electrolytic, JST XH x2
add(CX0 + 1.9, CY0 + 63.4, top, 7.2, 3.2, 8.5, (232, 200, 60))                # polyfuse
add(CX0 + 13.5, CY0 + 63.2, top, 9.0, 2.0, 2.0, BLACK)                         # 1N5819 diode
add(CX0 + 23.8, CY0 + 61.0, top, 6.3, 6.3, 12.0, (30, 40, 90))                # 470 uF electrolytic
for k in range(2):
    add(CX0 + 31.2 + k * 9.5, CY0 + 61.6, top, 7.5, 5.75, 6.0, WHITE)          # JST XH 3 (plug on the board header)

items.sort(key=lambda t: t[0])
for _, fn in items:
    fn()

# ---------------------------------------------------------------- the front walls of the base (cut low, to see inside)
FW = 5.0
poly([(0, BY, 0), (BX, BY, 0), (BX, BY, FW), (0, BY, FW)], shade(PLASTIC, 0.62), (20, 20, 24))
poly([(BX, 0, 0), (BX, BY, 0), (BX, BY, FW), (BX, 0, FW)], shade(PLASTIC, 0.8), (20, 20, 24))
poly([(0, BY, FW), (BX, BY, FW), (BX, BY - WALL, FW), (0, BY - WALL, FW)], shade(PLASTIC, 1.2), (20, 20, 24))
poly([(BX, 0, FW), (BX, BY, FW), (BX - WALL, BY - WALL, FW), (BX - WALL, WALL, FW)], shade(PLASTIC, 1.15), (20, 20, 24))

# ---------------------------------------------------------------- the cables, leaving through the front
def wire(x, y, z, pts_z_end, col, w=3):
    pass

# J2: 4 housings, two wires each (stacked rows): +5 V / GND, pump, boiler, valve
j2cols = [((200, 30, 30), (20, 20, 24)), ((150, 90, 40), (235, 235, 235)), ((230, 130, 30), (235, 235, 235)), ((235, 200, 40), (235, 235, 235))]
for k, (c1, c2) in enumerate(j2cols):
    xk = CX0 + 13 + k * 2.54
    d.line([P(xk, CY0 + 70.2, top + 4.1), P(xk, CY0 + 84, top + 3.0)], fill=c1, width=3 * SS)
    d.line([P(xk, CY0 + 70.2, top + 1.6), P(xk, CY0 + 84, top + 0.6)], fill=c2, width=3 * SS)
# J7: button (2 wires) and encoder (4 wires)
j7cols = [(240, 240, 240), (20, 20, 24), (200, 30, 30), (20, 20, 24), (40, 150, 70), (60, 110, 210)]
for k, col in enumerate(j7cols):
    xk = CX0 + 25 + k * 2.54
    d.line([P(xk, CY0 + 68.4, top + 1.2), P(xk, CY0 + 82, top - 0.3)], fill=col, width=3 * SS)
# J8 / J9: wires rise above the plugs then leave towards the front, above everything
for k, col in enumerate([(200, 30, 30), (20, 20, 24), (235, 200, 40), (60, 110, 210)]):
    y = CY0 + 33.0 + k * 2.54
    d.line([P(CX0 + 25.5, y, top + 10.5), P(CX0 + 25.5, y, top + 14 + k), P(CX0 + 25.5, CY0 + 84, top + 10 + k)], fill=col, width=3 * SS)
for k, col in enumerate([(200, 30, 30), (20, 20, 24), (40, 150, 70)]):
    y = CY0 + 43.2 + k * 2.54
    d.line([P(CX0 + 25.5, y, top + 10.5), P(CX0 + 25.5, y, top + 19 + k), P(CX0 + 25.5, CY0 + 84, top + 15 + k)], fill=col, width=3 * SS)
# JST XH flow sensors
for kx in range(2):
    for k, col in enumerate([(200, 30, 30), (235, 200, 40), (20, 20, 24)]):
        xk = CX0 + 32 + kx * 9.5 + k * 2.5
        d.line([P(xk, CY0 + 67.3, top + 5), P(xk, CY0 + 82, top + 3)], fill=col, width=3 * SS)
# PT100 wires leave the terminal block towards the front, above J7 / XH
for k, col in enumerate([(200, 30, 30), (200, 30, 30), (235, 235, 235)]):
    xk = mx + 7.0 + k * 3.6
    d.line([P(xk, my + 27.9, top + 8.8), P(xk, CY0 + 84, top + 7.5 - k * 0.5)], fill=col, width=3 * SS)
# FPC ribbon from the adapter connector towards the back wall (slot to cut)
cuboid(ax0 + 8, ay0 - 12, top + HDR + 1.6 + 0.8, 6, 14.5, 0.4, (232, 160, 48))

# ---------------------------------------------------------------- the labels
def pl(x, y, z, tx, ty, t, color=(20, 20, 26)):
    px, py = P(x, y, z)
    d.line([(px, py), (tx * SS, ty * SS)], fill=color, width=2 * SS)
    d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS], fill=color)
    text(tx + (10 if tx >= px / SS else -10), ty, t, 17, color, True, 'lm' if tx >= px / SS else 'rm')

pl(ex + 10, ey + 26, top + 10.2, 300, 470, "ESP32-S3, above the board")
pl(ex + 10, ey - 0.5, top + 11, 300, 400, "USB-C: opening in the wall")
pl(mx + 12, my + 12, top + 15, 1560, 240, "MAX31865 (rotated 180 deg, PT100 to the front)")
pl(ax0 + 11, ay0 + 10, top + HDR + 1.6, 1560, 300, "your FPC adapter board (on sockets)")
pl(ax0 + 11, ay0 + 4, top + HDR + 4.2, 1560, 420, "FPC connector pre-soldered")
pl(ax0 + 11, ay0 - 8, top + HDR + 2, 1560, 510, "ribbon to the remote display (back wall)")
pl(CX0 + 25.5, CY0 + 38, top + 10.5, 300, 560, "J8 dimmer (I2C), J9 pressure")
pl(CX0 + 16, CY0 + 66, top + 3.5, 300, 650, "J2: 5 V + 3 SSRs (4 housings, 2 x 4)")
pl(CX0 + 31, CY0 + 66, top + 3.5, 300, 735, "J7: button + encoder (1 x 6)")
pl(CX0 + 40, CY0 + 65, top + 6, 1560, 640, "JST XH 3: flow sensors In and Out")
pl(sx0, sy0 + 50, FLOOR + 3, 300, 820, "3 mm small posts (45 x 50)")

# ---------------------------------------------------------------- the stack of heights
text(1560, 800, "Usable height: 25 mm", 22, (30, 30, 36), True)
text(1560, 836, "posts 3 + board 1.6 = 4.6 mm", 18, (60, 60, 66))
text(1560, 862, "ESP32 (8.5 sockets): USB-C at 17.9 mm", 18, (60, 60, 66))
text(1560, 888, "FPC board on 8.5 sockets: 17.7 mm", 18, (60, 60, 66))
text(1560, 914, "MAX31865 (3 sockets): 22.6 mm, margin 2.4 mm", 18, (20, 110, 60), True)
text(1560, 950, "Electrolytic C1 and polyfuse F1: about 15 mm", 18, (60, 60, 66))

im = im.resize((W, H), Image.LANCZOS)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'box_iso3.png'))
print('ok')
