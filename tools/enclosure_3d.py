# -*- coding: utf-8 -*-
"""3D view of the carrier board in the enclosure.

Software renderer with a per-pixel depth buffer (numpy + Pillow): no painter's-algorithm artefacts.
Axes (mm): x to the right-down, y to the left-down (towards the front), z up. The camera looks along (-1, -1, -1),
so the depth of a point is x + y + z (larger = closer to the camera).
"""
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

SS = 2
W, H = 2000, 1250
WS, HS = W * SS, H * SS
s = 7.6                       # px per mm
OX, OY = 1000, 250            # screen position of the origin (back corner of the tray at floor level)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
BG = (244, 244, 240)

COL = np.empty((HS, WS, 3), np.uint8)
COL[:] = BG
DEPTH = np.full((HS, WS), -1e9, np.float32)
FID = np.zeros((HS, WS), np.int32)
_fid = [0]


def proj(x, y, z):
    """-> (u, v, depth) in supersampled pixels."""
    return ((OX + (x - y) * C30 * s) * SS, (OY + (x + y) * S30 * s - z * s) * SS, x + y + z)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def tri(a, b, c, col, fid):
    umin = int(max(0, math.floor(min(a[0], b[0], c[0]))))
    umax = int(min(WS - 1, math.ceil(max(a[0], b[0], c[0]))))
    vmin = int(max(0, math.floor(min(a[1], b[1], c[1]))))
    vmax = int(min(HS - 1, math.ceil(max(a[1], b[1], c[1]))))
    if umax < umin or vmax < vmin:
        return
    den = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
    if abs(den) < 1e-9:
        return
    ys, xs = np.mgrid[vmin:vmax + 1, umin:umax + 1]
    xs = xs.astype(np.float32) + 0.5
    ys = ys.astype(np.float32) + 0.5
    w0 = ((b[1] - c[1]) * (xs - c[0]) + (c[0] - b[0]) * (ys - c[1])) / den
    w1 = ((c[1] - a[1]) * (xs - c[0]) + (a[0] - c[0]) * (ys - c[1])) / den
    w2 = 1.0 - w0 - w1
    inside = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
    depth = (w0 * a[2] + w1 * b[2] + w2 * c[2]).astype(np.float32)
    sub = DEPTH[vmin:vmax + 1, umin:umax + 1]
    m = inside & (depth > sub)
    sub[m] = depth[m]
    COL[vmin:vmax + 1, umin:umax + 1][m] = col
    FID[vmin:vmax + 1, umin:umax + 1][m] = fid


def quad(p0, p1, p2, p3, col, bias=0.0):
    _fid[0] += 1
    f = _fid[0]
    q = [proj(*p) for p in (p0, p1, p2, p3)]
    q = [(u, v, d + bias) for (u, v, d) in q]
    tri(q[0], q[1], q[2], col, f)
    tri(q[0], q[2], q[3], col, f)


def cuboid(x, y, z, w, dp, h, color):
    """The three faces turned towards the camera: top, +x, +y."""
    quad((x, y, z + h), (x + w, y, z + h), (x + w, y + dp, z + h), (x, y + dp, z + h), shade(color, 1.12))
    quad((x + w, y, z), (x + w, y + dp, z), (x + w, y + dp, z + h), (x + w, y, z + h), shade(color, 0.85))
    quad((x, y + dp, z), (x + w, y + dp, z), (x + w, y + dp, z + h), (x, y + dp, z + h), shade(color, 0.68))


def cyl(cx, cy, r, z, h, color, n=32):
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        mid = (a0 + a1) / 2
        f = 0.55 + 0.5 * max(0.0, math.cos(mid) * 0.55 + math.sin(mid) * 0.83)
        quad((cx + r * math.cos(a0), cy + r * math.sin(a0), z), (cx + r * math.cos(a1), cy + r * math.sin(a1), z),
             (cx + r * math.cos(a1), cy + r * math.sin(a1), z + h), (cx + r * math.cos(a0), cy + r * math.sin(a0), z + h), shade(color, f))
    _fid[0] += 1
    f = _fid[0]
    c0 = proj(cx, cy, z + h)
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        tri(c0, proj(cx + r * math.cos(a0), cy + r * math.sin(a0), z + h), proj(cx + r * math.cos(a1), cy + r * math.sin(a1), z + h), shade(color, 1.25), f)


# ---------------------------------------------------------------- dimensions (mm)
WALL = 3.0
INT_X, INT_Y = 60.0, 85.0           # interior: x across, y along (the long side)
BX, BY = INT_X + 2 * WALL, INT_Y + 2 * WALL
BASE_H = 16.0                        # height of the base half (the walls)
FLOOR = 2.0
FW = 5.0                             # the front and right walls are cut low, to see inside
PLASTIC = (58, 58, 66)

# ---------------------------------------------------------------- the base (open tray)
cuboid(WALL, WALL, 0, BX - 2 * WALL, BY - 2 * WALL, FLOOR, shade(PLASTIC, 0.95))   # floor (inside the walls: no coplanar faces)
cuboid(0, 0, 0, WALL, BY, BASE_H, PLASTIC)                              # left wall (USB-C side)
cuboid(WALL, 0, 0, BX - WALL, WALL, BASE_H, PLASTIC)                    # back wall
cuboid(WALL, BY - WALL, 0, BX - WALL, WALL, FW, PLASTIC)                 # front wall (cut low)
cuboid(BX - WALL, 0, 0, WALL, BY - WALL, FW, PLASTIC)                    # right wall (cut low)
uy0 = WALL + 8.5 + 9.0
USB_OPENING = [(WALL, uy0, 12.5), (WALL, uy0 + 10, 12.5), (WALL, uy0 + 10, BASE_H), (WALL, uy0, BASE_H)]   # notch at the base / lid joint
quad(*USB_OPENING, (14, 14, 18), bias=0.05)                              # opening for the USB-C cable in the left wall
for (px, py) in [(WALL, WALL), (BX - WALL - 8, WALL), (WALL, BY - WALL - 8), (BX - WALL - 8, BY - WALL - 8)]:
    cyl(px + 4, py + 4, 4, FLOOR, BASE_H - FLOOR, (46, 46, 54))          # the four big posts, 8 mm round

# ---------------------------------------------------------------- the carrier and what it holds
CX0, CY0 = WALL + 1.0, WALL + 8.5     # origin of the carrier (58 x 68)
PCB_Z = FLOOR + 3.0                   # on the four small standoffs of 3 mm
PCBT = 1.6
top = PCB_Z + PCBT
GOLD = (214, 178, 70)
BLACK = (24, 24, 28)
WHITE = (238, 236, 226)
CREAM = (225, 215, 190)

sx0 = CX0 + (58 - 45) / 2
sy0 = CY0 + (68 - 50) / 2
for (ax, ay) in [(sx0, sy0), (sx0 + 45, sy0), (sx0, sy0 + 50), (sx0 + 45, sy0 + 50)]:
    cuboid(ax - 2.4, ay - 2.4, FLOOR, 4.8, 4.8, 3.0, (36, 36, 42))
cuboid(CX0, CY0, PCB_Z, 58, 68, PCBT, (22, 110, 66))
cuboid(CX0 + 8, CY0 + 68, PCB_Z, 42, 7, PCBT, (22, 110, 66))          # front tab (cable side)

# ESP32-S3 (~22 x 54) rotated 90 degrees on sockets of 8.5 mm: USB-C towards the left wall
ex, ey = CX0 + 2.5, CY0 + 3
cuboid(CX0 + 3.1, CY0 + 5.11 - 1.2, top, 50.8, 2.4, 8.5, BLACK)
cuboid(CX0 + 3.1, CY0 + 22.89 - 1.2, top, 50.8, 2.4, 8.5, BLACK)
cuboid(ex, ey, top + 8.5, 54, 22, 1.6, (236, 236, 242))
cuboid(CX0 + 1.0, CY0 + 9.9, top + 8.5 + 1.6, 7.5, 8.2, 3.2, (190, 194, 200))        # USB-C
cuboid(CX0 + 22, CY0 + 9.5, top + 8.5 + 1.6, 9, 9, 1.0, BLACK)                        # the module (shield)
cuboid(CX0 + 48.5, CY0 + 6, top + 8.5 + 1.6, 7.5, 16, 0.8, (236, 226, 196))           # antenna
# MAX31865 (25.4 x 27.9, 15 high) on low sockets of 3 mm, rotated 180 degrees: header at the rear, PT100 terminal at the front
mx, my = CX0 + 31, CY0 + 27.5
cuboid(mx + 3.8, my + 1.4, top, 19.0, 2.5, 3.0, BLACK)
cuboid(mx, my, top + 3.0, 25.4, 27.9, 1.6, (130, 30, 40))
cuboid(mx + 4.2, my + 20.5, top + 3.0 + 1.6, 17.0, 7.0, 10.4, (46, 120, 190))          # PT100 terminal block
cuboid(mx + 9.4, my + 9.9, top + 3.0 + 1.6, 7, 7, 1.6, BLACK)                          # the chip
# the FPC adapter board (~22 x 26.5) on a 2 x 4 header, at the left, FPC connector towards the front
ax0, ay0 = CX0 + 1.5, CY0 + 27.5
HDR = 8.5
cuboid(ax0 + 6.5, ay0 + 5.6, top, 10.2, 5.1, HDR, BLACK)
cuboid(ax0, ay0, top + HDR, 22, 26.5, 1.6, (22, 130, 70))
cuboid(ax0 + 6, ay0 + 19.0, top + HDR + 1.6, 10, 5.5, 2.6, WHITE)                      # its FPC connector
cuboid(ax0 + 1.0, ay0 + 3.1, top, 3.5, 3.5, HDR, (110, 110, 118))
cuboid(ax0 + 17.5, ay0 + 3.1, top, 3.5, 3.5, HDR, (110, 110, 118))
# J8 (dimmer, 1 x 4) and J9 (pressure, 1 x 3): straight headers in the corridor, plugs seated on top
J8X, J8Y = CX0 + 27.2 - 1.27, CY0 + 31.0 - 1.27
J9X, J9Y = CX0 + 27.2 - 1.27, CY0 + 42.0 - 1.27
cuboid(J8X, J8Y, top, 2.54, 10.16, 2.5, BLACK); cuboid(J8X + 0.2, J8Y + 0.2, top + 2.5, 2.14, 9.76, 8.0, WHITE)
cuboid(J9X, J9Y, top, 2.54, 7.62, 2.5, BLACK); cuboid(J9X + 0.2, J9Y + 0.2, top + 2.5, 2.14, 7.22, 8.0, WHITE)
# J2 (2 x 4 right-angle, rows stacked vertically) and four 2-pin housings plugged in from the front
cuboid(CX0 + 12.2 - 1.27, CY0 + 60.2, top, 10.16, 5.0, 5.9, BLACK)
for k in range(4):
    cuboid(CX0 + 12.2 - 1.27 + k * 2.54 + 0.15, CY0 + 65.2, top + 0.4, 2.24, 8.6, 5.1, WHITE)
# J7 (2 x 6 right-angle): lower row = 4-pin encoder housing, upper row = 2-pin button + 4-pin spare housings
cuboid(CX0 + 22.4 - 1.27, CY0 + 60.2, top, 15.24, 5.0, 5.9, BLACK)
cuboid(CX0 + 22.4 - 1.27 + 0.15, CY0 + 65.2, top + 0.4, 10.0, 8.6, 2.3, WHITE)
cuboid(CX0 + 22.4 - 1.27 + 0.15, CY0 + 65.2, top + 3.0, 4.9, 8.6, 2.3, WHITE)
cuboid(CX0 + 22.4 - 1.27 + 5.23, CY0 + 65.2, top + 3.0, 9.9, 8.6, 2.3, (225, 222, 205))
# polyfuse, standing diode, electrolytic, 100 nF, and the two JST XH (vertical headers with their plugs)
cuboid(CX0 + 1.9, CY0 + 64.4, top, 7.2, 3.2, 11.0, (232, 200, 60))
cuboid(CX0 + 1.2, CY0 + 61.2, top, 2.7, 2.7, 5.2, BLACK)
cyl(CX0 + 27.2, CY0 + 54.0, 3.15, top, 12.0, (30, 40, 90))                                # 470 uF electrolytic
cuboid(CX0 + 25.5, CY0 + 48.2, top, 4.0, 1.6, 4.2, (200, 120, 40))                        # 100 nF
for k in range(2):
    xb = CX0 + 42.0 + k * 10.5 - 4.95
    cuboid(xb, CY0 + 62.1, top, 9.9, 5.8, 5.8, WHITE)                                     # JST XH header
    cuboid(xb + 0.3, CY0 + 62.4, top + 5.8, 9.3, 5.2, 6.0, CREAM)                         # its plug

# FPC ribbon: leaves the connector towards the front and runs straight out
Y_END = CY0 + 97.0
RZ0 = top + HDR + 1.6 + 1.2
cuboid(ax0 + 8, ay0 + 24.5, RZ0, 6, Y_END - (ay0 + 24.5), 0.4, (232, 160, 48))

# ---------------------------------------------------------------- cables: small flat ribbons, 1.5 mm per wire (4 wires = 6 mm), 1.3 mm thick
WIRE = 1.5
TH = 1.3
RED, YEL, BLU = (205, 35, 35), (235, 200, 40), (60, 110, 210)
CABLES = []     # (number, label, connector, wires, color, end point)


def cable(label, conn, wires, color, end):
    CABLES.append((len(CABLES) + 1, label, conn, wires, color, end))


def run_x(xc, y0, y1, zc, wires, color):
    """Ribbon running along +y, width along x (horizontal housings)."""
    w = wires * WIRE
    cuboid(xc - w / 2, y0, zc - TH / 2, w, y1 - y0, TH, color)


def run_z(xc, y0, y1, zc, wires, color):
    """Ribbon running along +y, width along z (vertical 2-pin housings): seen edge-on."""
    w = wires * WIRE
    cuboid(xc - TH / 2, y0, zc - w / 2, TH, y1 - y0, w, color)


def riser_y(xc, yc, z0, z1, wires, color):
    """Short vertical piece leaving a plug whose pins run along y (J8, J9): width along y."""
    w = wires * WIRE
    cuboid(xc - TH / 2, yc - w / 2, z0, TH, w, z1 - z0, color)


def riser_x(xc, yc, z0, z1, wires, color):
    """Same, for a plug whose pins run along x (JST XH): width along x."""
    w = wires * WIRE
    cuboid(xc - w / 2, yc - TH / 2, z0, w, TH, z1 - z0, color)


Y0 = CY0 + 73.8
# J2: four 2-pin housings -> 5 V supply and the three SSRs (2 wires each)
for k, (lab, col) in enumerate([("5 V supply", RED), ("pump SSR", (150, 90, 40)), ("boiler SSR", (232, 130, 30)), ("valve SSR", YEL)]):
    xk = CX0 + 12.2 + k * 2.54
    zk = top + 0.4 + 2.55
    run_z(xk, Y0, Y_END, zk, 2, col)
    cable(lab, "J2", 2, col, (xk, Y_END, zk))
# J7: button (2 wires), encoder (4 wires, lower row), spare I/O (4 wires)
xb, xe, xs = CX0 + 22.4 + 1.27, CX0 + 22.4 + 3.81, CX0 + 22.4 + 8.89
run_x(xb, Y0, Y_END, top + 4.15, 2, (240, 240, 240)); cable("button", "J7", 2, (240, 240, 240), (xb, Y_END, top + 4.15))
run_x(xe, Y0, Y_END, top + 1.55, 4, (40, 150, 70)); cable("encoder", "J7", 4, (40, 150, 70), (xe, Y_END, top + 1.55))
run_x(xs, Y0, Y_END, top + 4.15, 4, (150, 90, 200)); cable("spare I/O", "J7", 4, (150, 90, 200), (xs, Y_END, top + 4.15))
# J8 (4 wires) and J9 (3 wires): up from the plugs, then forward; J9 passes under J8 and over C1
c8, c9 = (30, 170, 200), BLU
riser_y(CX0 + 27.2, CY0 + 34.8, top + 10.5, top + 17.0, 4, c8)
cuboid(CX0 + 26.2 - 3.0, CY0 + 34.8 - 3.0, top + 17.0, 6.0, Y_END - (CY0 + 34.8 - 3.0), TH, c8)
cable("pump dimmer (I2C)", "J8", 4, c8, (CX0 + 26.2, Y_END, top + 17.0))
riser_y(CX0 + 27.2, CY0 + 44.5, top + 10.5, top + 14.2, 3, c9)
cuboid(CX0 + 29.0 - 2.25, CY0 + 44.5 - 2.25, top + 14.2, 4.5, Y_END - (CY0 + 44.5 - 2.25), TH, c9)
cable("pressure sensor", "J9", 3, c9, (CX0 + 29.0, Y_END, top + 14.2))
# JST XH: flow sensors (3 wires each), up from the plugs then forward
c3, c4 = (20, 150, 150), (90, 80, 190)
riser_x(CX0 + 40.5, CY0 + 65.0, top + 11.8, top + 14.0, 3, c3)
cuboid(CX0 + 40.5 - 2.25, CY0 + 65.0 - 0.65, top + 14.0, 4.5, Y_END - (CY0 + 65.0 - 0.65), TH, c3)
cable("flow sensor In", "J3", 3, c3, (CX0 + 40.5, Y_END, top + 14.0))
riser_x(CX0 + 52.5, CY0 + 65.0, top + 11.8, top + 14.0, 3, c4)
cuboid(CX0 + 52.5 - 2.25, CY0 + 65.0 - 0.65, top + 14.0, 4.5, Y_END - (CY0 + 65.0 - 0.65), TH, c4)
cable("flow sensor Out", "J4", 3, c4, (CX0 + 52.5, Y_END, top + 14.0))
# PT100 (3 wires): leaves the MAX31865 terminal block, rises in front of it and passes over J3
cp = (230, 110, 160)
xp = CX0 + 43.5
cuboid(xp - 2.25, my + 27.9, top + 8.8 - TH / 2, 4.5, (CY0 + 57.0) - (my + 27.9), TH, cp)
riser_x(xp, CY0 + 57.0, top + 8.8 - TH / 2, top + 17.0 + TH, 3, cp)
cuboid(xp - 2.25, CY0 + 57.0 - 0.65, top + 17.0, 4.5, Y_END - (CY0 + 57.0 - 0.65), TH, cp)
cable("PT100 probe", "MAX31865", 3, cp, (xp, Y_END, top + 17.0))
RIBBON_NUMBER = len(CABLES) + 1

# ---------------------------------------------------------------- outlines (edges between different faces)
edge = np.zeros((HS, WS), bool)
edge[:, 1:] |= FID[:, 1:] != FID[:, :-1]
edge[1:, :] |= FID[1:, :] != FID[:-1, :]
e2 = edge.copy()
e2[:, :-1] |= edge[:, 1:]
e2[:-1, :] |= edge[1:, :]
COL[e2] = (22, 22, 26)

# ---------------------------------------------------------------- compose: image, overlays
im = Image.fromarray(COL)
d = ImageDraw.Draw(im)


def F(sz, b=False):
    return ImageFont.truetype('C:/Windows/Fonts/%s.ttf' % ('arialbd' if b else 'arial'), int(sz * SS))


def P2(x, y, z):
    u, v, _ = proj(x, y, z)
    return u, v


def text(x, y, t, size=18, color=(30, 30, 36), bold=False, anchor='lm'):
    d.text((x * SS, y * SS), t, font=F(size, bold), fill=color, anchor=anchor)


d.line([P2(*p) for p in USB_OPENING] + [P2(*USB_OPENING[0])], fill=(230, 230, 235), width=2 * SS)
text(W / 2, 40, "Enclosure view: the carrier board with its connectors (the display is remote)", 30, bold=True, anchor='mm')
text(W / 2, 80, "Enclosure base, lid removed. Scaled concept drawing following the placement plan: not a board layout.", 20, (110, 110, 116), anchor='mm')


def pl(x, y, z, tx, ty, t, color=(20, 20, 26)):
    px, py = P2(x, y, z)
    d.line([(px, py), (tx * SS, ty * SS)], fill=color, width=2 * SS)
    d.ellipse([px - 4 * SS, py - 4 * SS, px + 4 * SS, py + 4 * SS], fill=color)
    text(tx + (10 if tx >= px / SS else -10), ty, t, 17, color, True, 'lm' if tx >= px / SS else 'rm')


pl(ex + 30, ey + 11, top + 10.2, 330, 330, "ESP32-S3, rotated 90 deg")
pl(CX0 + 3, CY0 + 14, top + 12, 330, 250, "USB-C: left wall opening")
pl(mx + 12, my + 8, top + 15, 1560, 330, "MAX31865 (PT100 to the front)")
pl(ax0 + 11, ay0 + 10, top + HDR + 1.6, 330, 430, "your FPC adapter board (on sockets)")
pl(ax0 + 11, ay0 + 22, top + HDR + 4.2, 330, 520, "FPC connector pre-soldered")
pl(sx0, sy0 + 50, FLOOR + 3, 330, 640, "3 mm small posts (45 x 50)")
pl(BX - WALL - 4, BY - WALL - 4, BASE_H, 1560, 520, "8 mm round corner posts")
pl(CX0 + 30, BY, FW, 1560, 640, "slot to cut in the front wall (cables)")
pl(CX0 + 27.2, CY0 + 40, top + 11, 330, 740, "J8 dimmer and J9 pressure (corridor)")

# numbered tags at the cable ends, staggered so that they do not overlap
ends = []
for (n, lab, conn, wires, col, end) in CABLES:
    ends.append((n, end, col))
ends.append((RIBBON_NUMBER, (ax0 + 11, Y_END, RZ0), (232, 160, 48)))
order = sorted(ends, key=lambda e: e[1][0])
for rank, (n, p, col) in enumerate(order):
    u, v = P2(*p)
    off = (rank % 4) * 30
    tx, ty = u - 0.866 * off * 0 + (-0.866) * (14 + off) * 1.0 * 0, v
    # direction of the cables on screen (towards +y): (-C30, +S30)
    ux, uy = -C30, S30
    cx, cy = u + ux * (30 + off * SS), v + uy * (30 + off * SS)
    d.line([(u, v), (cx, cy)], fill=(40, 40, 46), width=2 * SS)
    d.ellipse([cx - 11 * SS, cy - 11 * SS, cx + 11 * SS, cy + 11 * SS], fill=col, outline=(30, 30, 34), width=2 * SS)
    d.text((cx, cy), str(n), font=F(15, True), fill=(20, 20, 24) if sum(col) > 400 else (255, 255, 255), anchor='mm')

# cable legend
text(560, 955, "Cables: small flat ribbons, 1.5 mm per wire (all leave through the front slot)", 20, (30, 30, 36), True)
entries = [(n, "%s  %s  (%d wires, %.1f mm)" % (conn, lab, wires, wires * WIRE), col) for (n, lab, conn, wires, col, end) in CABLES] + [(RIBBON_NUMBER, "J5  display FPC ribbon (6 mm)", (232, 160, 48))]
per_col = 7
for i, (n, lab, col) in enumerate(entries):
    cx = 580 + (i // per_col) * 560
    cy = 995 + (i % per_col) * 31
    d.ellipse([(cx - 11) * SS, (cy - 11) * SS, (cx + 11) * SS, (cy + 11) * SS], fill=col, outline=(30, 30, 34), width=2 * SS)
    d.text((cx * SS, cy * SS), str(n), font=F(14, True), fill=(20, 20, 24) if sum(col) > 400 else (255, 255, 255), anchor='mm')
    text(cx + 22, cy, lab, 18, (30, 30, 36))

# the stack of heights
text(1560, 760, "Usable height: 25 mm", 22, (30, 30, 36), True)
text(1560, 796, "posts 3 + board 1.6 = 4.6 mm", 18, (60, 60, 66))
text(1560, 822, "ESP32 (8.5 sockets): USB-C at 17.9 mm", 18, (60, 60, 66))
text(1560, 848, "FPC board on 8.5 sockets: 17.7 mm", 18, (60, 60, 66))
text(1560, 874, "MAX31865 (3 sockets): 22.6 mm, margin 2.4 mm", 18, (20, 110, 60), True)
text(1560, 910, "Electrolytic C1 and polyfuse F1: about 15 mm", 18, (60, 60, 66))

im = im.resize((W, H), Image.LANCZOS)
im.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'images', 'enclosure_3d.png'))
print('ok')
