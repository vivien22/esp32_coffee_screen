# -*- coding: utf-8 -*-
import math
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 1700, 1200
im = Image.new('RGB', (W * SS, H * SS), (244, 244, 240))
d = ImageDraw.Draw(im)
s = 6.2                      # px per mm
OX, OY = 800, 440            # screen position of the origin (back corner of the tray at floor level)
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
text(W / 2, 40, "Projection du boîtier : la carte porteuse avec ses connecteurs (l'écran est déporté)", 30, bold=True, anchor='mm')
text(W / 2, 80, "Fond du boîtier, couvercle retiré. Dessin de principe à l'échelle : ce n'est pas un plan de la carte.", 20, (110, 110, 116), anchor='mm')

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
items = []                            # (sort key, drawing function)
def add(x, y, z, w, dp, h, color, name=None):
    items.append(((x + w / 2) + (y + dp / 2) + z * 0.001, lambda x=x, y=y, z=z, w=w, dp=dp, h=h, color=color: cuboid(x, y, z, w, dp, h, color)))

# the standoffs (3 mm), 45 x 50 apart
sx0 = CX0 + (58 - 45) / 2
sy0 = CY0 + (68 - 50) / 2
for (ax, ay) in [(sx0, sy0), (sx0 + 45, sy0), (sx0, sy0 + 50), (sx0 + 45, sy0 + 50)]:
    add(ax - 2.4, ay - 2.4, FLOOR, 4.8, 4.8, 3.0, (36, 36, 42))
# the carrier
add(CX0, CY0, PCB_Z, 58, 68, PCBT, (22, 110, 66))
top = PCB_Z + PCBT
# ESP32-S3: sockets 8.5, board 21 x 52, USB-C
ex, ey = CX0 + 3, CY0 + 3
add(ex, ey + 1, top, 2.4, 50, 8.5, (30, 30, 34)); add(ex + 21 - 2.4, ey + 1, top, 2.4, 50, 8.5, (30, 30, 34))
add(ex, ey, top + 8.5, 21, 52, 1.6, (236, 236, 242))
add(ex + 5.5, ey - 1.3, top + 8.5 + 1.6, 10, 7.5, 3.2, (190, 194, 200))
add(ex + 6, ey + 14, top + 8.5 + 1.6, 9, 9, 1.0, (28, 28, 34))      # the ESP32 chip
add(ex + 3, ey + 43, top + 8.5 + 1.6, 15, 8, 0.8, (236, 226, 196))  # the antenna
# MAX31865: low sockets 3, board 25 x 28, terminal block, total 15
mx, my = CX0 + 28, CY0 + 3
add(mx, my + 1, top, 2.0, 26, 3.0, (30, 30, 34)); add(mx + 23, my + 1, top, 2.0, 26, 3.0, (30, 30, 34))
add(mx, my, top + 3.0, 25, 28, 1.6, (22, 70, 160))
add(mx + 6, my + 17, top + 3.0 + 1.6, 13, 9, 15 - 1.6, (46, 104, 180))   # the terminal block: the module is 15 mm high
add(mx + 4, my + 5, top + 3.0 + 1.6, 7, 7, 2.0, (24, 24, 28))              # the chip
# three transistors
for i in range(3):
    add(CX0 + 30 + i * 8, CY0 + 36, top, 4.5, 3.5, 1.6, (24, 24, 28))
# the FPC connector (0.5 mm, 8 pins) at the front edge, for the remote display
add(CX0 + 4, CY0 + 61, top, 12, 5.0, 2.8, (236, 236, 228))
# JST XH 3 pins x2 (flow sensors) at the front edge: 7.5 x 5.75 x 6
for k in range(2):
    add(CX0 + 22 + k * 11, CY0 + 60.5, top, 7.5, 5.75, 6.0, (240, 240, 232))
# Dupont pin headers (right angle) along the right edge: 5V 2, pump 2, heater 2, valve 2, button 2, encoder 4
dup = [("5V", 2), ("pompe", 2), ("chaudière", 2), ("vanne", 2), ("bouton", 2), ("encodeur", 4)]
dy = CY0 + 6.0
dup_pos = []
for name, n in dup:
    add(CX0 + 46.5, dy, top, 8.5, n * 2.54, 2.8, (24, 24, 28))
    dup_pos.append((name, n, dy))
    dy += n * 2.54 + 2.2

items.sort(key=lambda t: t[0])
for _, fn in items:
    fn()

# ---------------------------------------------------------------- the front walls of the base (cut low, to see inside)
FW = 5.0
poly([(0, BY, 0), (BX, BY, 0), (BX, BY, FW), (0, BY, FW)], shade(PLASTIC, 0.62), (20, 20, 24))
poly([(BX, 0, 0), (BX, BY, 0), (BX, BY, FW), (BX, 0, FW)], shade(PLASTIC, 0.8), (20, 20, 24))
poly([(0, BY, FW), (BX, BY, FW), (BX, BY - WALL, FW), (0, BY - WALL, FW)], shade(PLASTIC, 1.2), (20, 20, 24))
poly([(BX, 0, FW), (BX, BY, FW), (BX - WALL, BY - WALL, FW), (BX - WALL, WALL, FW)], shade(PLASTIC, 1.15), (20, 20, 24))

# ---------------------------------------------------------------- the cables (Dupont wires, XH cables, FPC ribbon), leaving the carrier
WCOL = {"5V": [(200, 30, 30), (20, 20, 24)], "pompe": [(150, 90, 40), (230, 230, 230)], "chaudière": [(230, 130, 30), (230, 230, 230)],
        "vanne": [(230, 200, 40), (230, 230, 230)], "bouton": [(240, 240, 240), (20, 20, 24)], "encodeur": [(40, 150, 70), (60, 110, 210), (20, 20, 24), (200, 30, 30)]}
for name, n, yy in dup_pos:
    for k in range(n):
        yk = yy + (k + 0.5) * 2.54
        col = WCOL[name][k]
        d.line([P(CX0 + 55, yk, top + 1.4), P(CX0 + 55 + 24, yk, top + 1.4 - 1.0)], fill=col, width=3 * SS)
        d.line([P(CX0 + 55, yk, top + 1.4), P(CX0 + 55 + 24, yk, top + 1.4 - 1.0)], fill=(20, 20, 24), width=1)
for kx in range(2):
    for k, col in enumerate([(200, 30, 30), (20, 20, 24), (235, 200, 40)]):
        xk = CX0 + 22 + kx * 11 + (k + 0.5) * 2.5
        d.line([P(xk, CY0 + 66, top + 3), P(xk, CY0 + 66 + 24, top + 2)], fill=col, width=3 * SS)
# FPC ribbon: flat, orange, to the display
cuboid(CX0 + 7, CY0 + 66, top + 1.2, 6, 30, 0.4, (232, 160, 48))

# ---------------------------------------------------------------- the labels
def pl(x, y, z, tx, ty, t, color=(20, 20, 26)):
    px, py = P(x, y, z)
    d.line([(px, py), (tx * SS, ty * SS)], fill=color, width=2 * SS)
    d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS], fill=color)
    text(tx + (10 if tx >= px / SS else -10), ty, t, 17, color, True, 'lm' if tx >= px / SS else 'rm')

pl(ex + 10, ey + 26, top + 10.1, 330, 520, "carte ESP32-S3 (21 x 52)")
pl(ex + 10, ey - 0.5, top + 11, 330, 440, "USB-C : ouverture dans la paroi")
pl(mx + 12, my + 22, top + 4.6, 330, 620, "MAX31865 (25 x 28, hauteur 15)")
pl(CX0 + 34, CY0 + 38, top + 1.6, 330, 720, "3 transistors de commande des SSR")
pl(sx0, sy0 + 50, FLOOR + 3, 330, 800, "petits plots de 3 mm (45 x 50)")
names = {"5V": "Dupont 2 : alimentation 5 V", "pompe": "Dupont 2 : SSR pompe", "chaudière": "Dupont 2 : SSR chaudière", "vanne": "Dupont 2 : SSR vanne", "bouton": "Dupont 2 : bouton start", "encodeur": "Dupont 4 : encodeur"}
ty = 200
for name, n, yy in dup_pos:
    pl(CX0 + 51, yy + n * 1.27, top + 2.8, 1230, ty, names[name]); ty += 56
pl(CX0 + 26, CY0 + 63, top + 6, 1230, 560, "JST XH 3 : capteur de débit In (A)")
pl(CX0 + 37, CY0 + 63, top + 6, 1230, 616, "JST XH 3 : capteur de débit Out")
pl(CX0 + 10, CY0 + 63, top + 2.8, 1230, 672, "connecteur FPC 8 broches : vers l'écran déporté")

# ---------------------------------------------------------------- the stack of heights
text(1230, 800, "Hauteur utile : 25 mm", 22, (30, 30, 36), True)
text(1230, 836, "plots 3 + carte 1,6 = 4,6 mm", 18, (60, 60, 66))
text(1230, 862, "ESP32 (supports 8,5) : USB-C à 17,9 mm", 18, (60, 60, 66))
text(1230, 888, "MAX31865 (supports 3) : 22,6 mm, marge 2,4 mm", 18, (20, 110, 60), True)
text(1230, 914, "connecteurs Dupont coudés : 2,8 mm", 18, (60, 60, 66))

im = im.resize((W, H), Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/box_iso2.png')
print('ok')
