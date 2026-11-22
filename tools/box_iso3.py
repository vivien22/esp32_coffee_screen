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

# ESP32-S3 (21 x 52) on sockets of 8.5 mm, at the left; USB-C towards the back wall
ex, ey = CX0 + 3, CY0 + 3
add(ex, ey + 1, top, 2.4, 50, 8.5, (30, 30, 34)); add(ex + 21 - 2.4, ey + 1, top, 2.4, 50, 8.5, (30, 30, 34))
add(ex, ey, top + 8.5, 21, 52, 1.6, (236, 236, 242))
add(ex + 5.5, ey - 1.3, top + 8.5 + 1.6, 10, 7.5, 3.2, (190, 194, 200))
add(ex + 6, ey + 14, top + 8.5 + 1.6, 9, 9, 1.0, (28, 28, 34))
add(ex + 3, ey + 43, top + 8.5 + 1.6, 15, 8, 0.8, (236, 226, 196))
# MAX31865 (25 x 28, 15 high) on low sockets of 3 mm
mx, my = CX0 + 28, CY0 + 2
add(mx, my + 1, top, 2.0, 26, 3.0, (30, 30, 34)); add(mx + 23, my + 1, top, 2.0, 26, 3.0, (30, 30, 34))
add(mx, my, top + 3.0, 25, 28, 1.6, (22, 70, 160))
add(mx + 6, my + 17, top + 3.0 + 1.6, 13, 9, 15 - 1.6, (46, 104, 180))
add(mx + 4, my + 5, top + 3.0 + 1.6, 7, 7, 2.0, (24, 24, 28))
# the FPC adapter board (22 x 28), with its connector already soldered: it stands on a 2 x 4 header, at the right, under the exit
ax0, ay0 = CX0 + 29, CY0 + 32
HDR = 8.5
add(ax0 + 6, ay0 + 3, top, 10.2, 5.1, HDR, (24, 24, 28))                  # 2 x 4 header + socket
add(ax0, ay0, top + HDR, 22, 28, 1.6, (22, 130, 70))                      # the adapter board
add(ax0 + 6, ay0 + 22, top + HDR + 1.6, 10, 5, 2.6, (236, 236, 228))       # its FPC connector, towards the front wall
add(ax0 + 1.5, ay0 + 24, top, 3.5, 3.5, HDR, (110, 110, 118))              # a standoff under each mounting hole
add(ax0 + 17, ay0 + 24, top, 3.5, 3.5, HDR, (110, 110, 118))
# the Dupont block under the ESP: a right-angle 2 x 8 header (two rows of housings), cables to the front
add(CX0 + 3, CY0 + 57, top, 20.3, 5.1, 2.8, (24, 24, 28))
# three transistors, in the row below
for i in range(3):
    add(CX0 + 5 + i * 7, CY0 + 63.5, top, 4.5, 3.5, 1.6, (24, 24, 28))
# JST XH 3 pins x2 (flow sensors), at the front edge, right
for k in range(2):
    add(CX0 + 28 + k * 11, CY0 + 61.5, top, 7.5, 5.75, 6.0, (240, 240, 232))

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
rowA = [(200, 30, 30), (20, 20, 24), (150, 90, 40), (235, 235, 235), (230, 130, 30), (235, 235, 235), (235, 200, 40), (235, 235, 235)]
rowB = [(240, 240, 240), (20, 20, 24), (40, 150, 70), (60, 110, 210), (20, 20, 24), (200, 30, 30)]
for k, col in enumerate(rowA):
    xk = CX0 + 3 + (k + 0.5) * 2.54
    d.line([P(xk, CY0 + 62.1, top + 2.0), P(xk, CY0 + 62.1 + 24, top + 1.0)], fill=col, width=3 * SS)
for k, col in enumerate(rowB):
    xk = CX0 + 3 + (k + 0.5) * 2.54
    d.line([P(xk, CY0 + 62.1, top + 0.8), P(xk, CY0 + 62.1 + 24, top - 0.2)], fill=col, width=3 * SS)
for kx in range(2):
    for k, col in enumerate([(200, 30, 30), (20, 20, 24), (235, 200, 40)]):
        xk = CX0 + 28 + kx * 11 + (k + 0.5) * 2.5
        d.line([P(xk, CY0 + 67.5, top + 3), P(xk, CY0 + 67.5 + 24, top + 2)], fill=col, width=3 * SS)
# FPC ribbon from the adapter connector to the remote display
cuboid(ax0 + 8, ay0 + 27, top + HDR + 1.6 + 0.8, 6, 36, 0.4, (232, 160, 48))

# ---------------------------------------------------------------- the labels
def pl(x, y, z, tx, ty, t, color=(20, 20, 26)):
    px, py = P(x, y, z)
    d.line([(px, py), (tx * SS, ty * SS)], fill=color, width=2 * SS)
    d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS], fill=color)
    text(tx + (10 if tx >= px / SS else -10), ty, t, 17, color, True, 'lm' if tx >= px / SS else 'rm')

pl(ex + 10, ey + 26, top + 10.2, 330, 470, "ESP32-S3, au-dessus de la carte")
pl(ex + 10, ey - 0.5, top + 11, 330, 400, "USB-C : ouverture dans la paroi")
pl(mx + 12, my + 22, top + 4.6, 1230, 240, "MAX31865 (25 x 28, hauteur 15)")
pl(ax0 + 11, ay0 + 10, top + HDR + 1.6, 1230, 330, "ta carte d'adaptation FPC (sur supports)")
pl(ax0 + 11, ay0 + 24, top + HDR + 4.2, 1230, 420, "connecteur FPC déjà soudé : aucun CMS à souder")
pl(ax0 + 11, ay0 + 40, top + HDR + 2, 1230, 510, "nappe vers l'écran déporté")
pl(CX0 + 13, CY0 + 59.5, top + 2.8, 330, 600, "Dupont 2 x 8 : 5 V, SSR, bouton, enc.")
pl(CX0 + 9, CY0 + 65, top + 1.6, 330, 690, "3 transistors des SSR")
pl(CX0 + 31, CY0 + 64, top + 6, 1230, 640, "JST XH 3 : capteurs de débit In et Out")
pl(sx0, sy0 + 50, FLOOR + 3, 330, 780, "petits plots de 3 mm (45 x 50)")

# ---------------------------------------------------------------- the stack of heights
text(1230, 800, "Hauteur utile : 25 mm", 22, (30, 30, 36), True)
text(1230, 836, "plots 3 + carte 1,6 = 4,6 mm", 18, (60, 60, 66))
text(1230, 862, "ESP32 (supports 8,5) : USB-C à 17,9 mm", 18, (60, 60, 66))
text(1230, 888, "carte FPC sur supports 8,5 : 17,7 mm", 18, (60, 60, 66))
text(1230, 914, "MAX31865 (supports 3) : 22,6 mm, marge 2,4 mm", 18, (20, 110, 60), True)

im = im.resize((W, H), Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/box_iso3.png')
print('ok')
