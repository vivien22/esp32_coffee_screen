# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S = 2
W, H = 1800, 1360
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

T(W / 2, 36, "Carte porteuse ESP32-S3 : schéma de connexion (tout en composants traversants, aucun CMS à souder)", F(30, True))
T(W / 2, 74, "Schéma de principe : à valider avant de lancer la fabrication (brochage de l'écran, de l'encodeur et du module MAX31865 à confirmer).", F(19), GRY)

# ================================================================ 1. connectors
def pin(x, y, label, fill, size=15, w=84, h=44, txt=(255, 255, 255)):
    RR(x, y, x + w, y + h, 6, fill=fill, outline=(20, 20, 24), width=2)
    T(x + w / 2, y + h / 2, label, F(size, True), txt)

T(60, 118, "J2 : barrette mâle 2 x 8 coudée, boîtiers Dupont femelles", F(22, True), INK, 'lm')
T(60, 146, "rangée A (haut) et rangée B (bas) ; les boîtiers se rangent côte à côte", F(16), GRY, 'lm')
rowA = [("+5 V", RED), ("GND", (60, 60, 66)), ("pompe +", BRN), ("pompe −", BRN), ("chaud. +", ORG), ("chaud. −", ORG), ("vanne +", YEL), ("vanne −", YEL)]
rowB = [("bouton", (90, 90, 96)), ("GND", (60, 60, 66)), ("3V3", RED), ("GND", (60, 60, 66)), ("enc. A", GRN), ("enc. B", GRN), ("réserve", (150, 150, 156)), ("GND", (60, 60, 66))]
x0, yA, yB = 60, 200, 250
for i, (lab, col) in enumerate(rowA):
    pin(x0 + i * 88, yA, lab, col, 14)
for i, (lab, col) in enumerate(rowB):
    pin(x0 + i * 88, yB, lab, col, 14)
# group brackets
def bracket(i0, i1, y, text, col, below=True):
    xa, xb = x0 + i0 * 88, x0 + (i1 + 1) * 88 - 4
    yy = y + (50 if below else -8)
    L([(xa, yy), (xb, yy)], col, 3)
    T((xa + xb) / 2, yy + (14 if below else -10), text, F(14, True), col)
bracket(0, 1, yA, "alimentation", RED, below=False)
bracket(2, 3, yA, "SSR pompe (DC)", BRN, below=False)
bracket(4, 5, yA, "SSR chaudière", ORG, below=False)
bracket(6, 7, yA, "SSR vanne", YEL, below=False)
bracket(0, 1, yB, "bouton start", (90, 90, 96))
bracket(2, 5, yB, "encodeur (ordre des fils : voir le module)", GRN)
bracket(6, 7, yB, "réserve", (150, 150, 156))

T(60, 346, "J3, J4 : JST XH 3 broches, capteurs de débit", F(22, True), INK, 'lm')
for k, (name, y) in enumerate([("J3  débit In", 375), ("J4  débit Out", 445)]):
    T(60, y + 22, name, F(16, True), INK, 'lm')
    for i, (lab, col) in enumerate([("+5 V", RED), ("signal", BLU), ("GND", (60, 60, 66))]):
        pin(200 + i * 88, y, lab, col, 14)
T(60, 520, "Ordre des fils du capteur : souvent rouge / jaune / noir : à vérifier sur ton câble.", F(15), GRY, 'lm')

T(60, 570, "J5 : support 2 x 4 pour ta carte d'adaptation FPC (8 broches)", F(22, True), INK, 'lm')
T(60, 598, "numérotation de ta carte : rangée haute 1, 3, 5, 7 ; rangée basse 2, 4, 6, 8", F(16), GRY, 'lm')
fpc_top = [("1", "GND"), ("3", "SCL"), ("5", "DC"), ("7", "RST")]
fpc_bot = [("2", "3V3"), ("4", "SDA"), ("6", "CS"), ("8", "BL")]
for i, (n, sg) in enumerate(fpc_top):
    pin(60 + i * 96, 620, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
for i, (n, sg) in enumerate(fpc_bot):
    pin(60 + i * 96, 672, "%s  %s" % (n, sg), (60, 110, 170), 14, 90)
T(60, 740, "Affectation provisoire (typique d'un GC9A01 8 broches) : l'ordre exact vient de la fiche de ton écran.", F(15), RED, 'lm')

T(60, 790, "J6 : support 1 x 8 pour le module MAX31865", F(22, True), INK, 'lm')
mx = [("VIN", RED), ("3Vo", (150, 150, 156)), ("GND", (60, 60, 66)), ("CLK", VIO), ("SDO", VIO), ("SDI", VIO), ("CS", VIO), ("RDY", (150, 150, 156))]
for i, (lab, col) in enumerate(mx):
    pin(60 + i * 88, 820, lab, col, 14)
T(60, 888, "Alimenté en 3,3 V. 3Vo et RDY ne sont pas utilisés. Ordre des broches à vérifier sur ton module.", F(15), GRY, 'lm')

# ================================================================ 2. GPIO table
gx = 860
T(gx, 118, "ESP32-S3 : broches utilisées", F(22, True), INK, 'lm')
rows = [("5V", "+5 V (après diode et fusible)", RED), ("3V3", "alimente MAX31865, encodeur, écran", RED),
        ("GPIO 17", "commande SSR pompe", BRN), ("GPIO 18", "commande SSR chaudière", ORG), ("GPIO 21", "commande SSR vanne", YEL),
        ("GPIO 15", "débit In", BLU), ("GPIO 16", "débit Out", BLU),
        ("GPIO 4 / 5", "encodeur A / B", GRN), ("GPIO 6", "bouton start", (90, 90, 96)),
        ("GPIO 11 / 12 / 13", "SPI : MOSI / SCK / MISO", VIO), ("GPIO 10", "écran CS", VIO), ("GPIO 9 / 8", "écran DC / RST", VIO),
        ("GPIO 14", "écran rétroéclairage (transistor)", VIO), ("GPIO 7", "MAX31865 CS", VIO), ("GPIO 38", "réserve", (150, 150, 156))]
for i, (a, b, col) in enumerate(rows):
    y = 150 + i * 34
    RR(gx, y, gx + 180, y + 28, 5, fill=col, outline=(20, 20, 24), width=1)
    T(gx + 90, y + 14, a, F(14, True), (255, 255, 255))
    T(gx + 192, y + 14, b, F(15), INK, 'lm')
T(gx, 672, "Évitées : 0, 3, 45, 46 (amorçage), 19 et 20 (USB), 35 à 37 (mémoire PSRAM).", F(15), GRY, 'lm')

# ================================================================ 3. circuits
cx0 = 1370
T(cx0, 118, "Circuits sur la carte", F(22, True), INK, 'lm')

# power
T(cx0, 160, "Alimentation", F(17, True), RED, 'lm')
L([(cx0, 200), (cx0 + 40, 200)], RED, 3); T(cx0 - 6, 200, "A1", F(13, True), RED, 'rm')
RR(cx0 + 40, 188, cx0 + 118, 212, 4, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 79, 200, "fusible 1,1 A", F(11, True))
L([(cx0 + 118, 200), (cx0 + 150, 200)], RED, 3)
d.polygon([((cx0 + 150) * S, 188 * S), ((cx0 + 150) * S, 212 * S), ((cx0 + 180) * S, 200 * S)], fill=(250, 250, 240), outline=INK)
L([(cx0 + 180, 186), (cx0 + 180, 214)], INK, 3); T(cx0 + 165, 232, "1N5819", F(11, True))
L([(cx0 + 180, 200), (cx0 + 270, 200)], RED, 3)
T(cx0 + 300, 200, "+5 V carte", F(14, True), RED, 'lm')
L([(cx0 + 215, 200), (cx0 + 215, 232)], RED, 2)
L([(cx0 + 205, 232), (cx0 + 225, 232)], INK, 3); L([(cx0 + 205, 240), (cx0 + 225, 240)], INK, 3)
L([(cx0 + 215, 240), (cx0 + 215, 262)], INK, 2); T(cx0 + 215, 276, "470 µF + 100 nF", F(11, True))

# SSR driver
T(cx0, 330, "Commande d'un SSR (x3)", F(17, True), BRN, 'lm')
L([(cx0 + 20, 365), (cx0 + 250, 365)], RED, 3); T(cx0 + 262, 365, "+5 V", F(13, True), RED, 'lm')
RR(cx0 + 110, 385, cx0 + 200, 430, 6, fill=(232, 240, 252), outline=BLU, width=3); T(cx0 + 155, 400, "entrée du", F(12, True), BLU); T(cx0 + 155, 417, "SSR  + −", F(12, True), BLU)
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
T(cx0 + 20, 640, "2N2222A (TO-92) : l'entrée du SSR reçoit presque tout le 5 V", F(13), GRY, 'lm')

# flow input
T(cx0, 700, "Entrée d'un capteur de débit (x2)", F(17, True), BLU, 'lm')
L([(cx0 + 20, 735), (cx0 + 250, 735)], RED, 3); T(cx0 + 262, 735, "+5 V", F(13, True), RED, 'lm')
L([(cx0 + 60, 735), (cx0 + 60, 765)], RED, 2)
RR(cx0 + 48, 765, cx0 + 72, 800, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 60, 782, "10k", F(11, True))
L([(cx0 + 60, 800), (cx0 + 60, 830)], BLU, 2)
L([(cx0 - 20, 830), (cx0 + 60, 830), (cx0 + 100, 830)], BLU, 3); T(cx0 - 28, 830, "signal J3", F(12, True), BLU, 'rm')
RR(cx0 + 100, 818, cx0 + 150, 842, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 125, 830, "4,7k", F(11, True))
L([(cx0 + 150, 830), (cx0 + 230, 830)], BLU, 3); T(cx0 + 242, 830, "GPIO", F(13, True), BLU, 'lm')
L([(cx0 + 190, 830), (cx0 + 190, 860)], BLU, 2)
RR(cx0 + 178, 860, cx0 + 202, 895, 3, fill=(250, 250, 240), outline=INK, width=2); T(cx0 + 190, 877, "10k", F(11, True))
L([(cx0 + 190, 895), (cx0 + 190, 915)], INK, 2); T(cx0 + 190, 928, "GND", F(12, True))
L([(cx0 + 225, 830), (cx0 + 225, 860)], BLU, 2); L([(cx0 + 215, 860), (cx0 + 235, 860)], INK, 3); L([(cx0 + 215, 868), (cx0 + 235, 868)], INK, 3)
L([(cx0 + 225, 868), (cx0 + 225, 890)], INK, 2); T(cx0 + 225, 904, "1 nF", F(11, True))
T(cx0 + 20, 960, "Fonctionne avec un capteur à sortie 5 V (le pont divise à 3,4 V)", F(13), GRY, 'lm')
T(cx0 + 20, 982, "ou à collecteur ouvert (la résistance de 10 k remonte à 5 V).", F(13), GRY, 'lm')

# ================================================================ 4. notes
T(60, 960, "Notes de conception", F(22, True), INK, 'lm')
notes = [
    "Les trois niveaux de tension : +5 V carte (après fusible et diode), 3,3 V fourni par la carte ESP32-S3, GND commun.",
    "Le rétroéclairage de l'écran est commandé par un transistor sur GPIO 14 (le courant dépasse ce que supporte une broche).",
    "Pas de régulateur sur la carte : l'ESP32-S3 fournit le 3,3 V (vérifier qu'il tient le MAX31865, l'encodeur et l'écran).",
    "Tous les composants sont traversants (TO-92, résistances axiales, condensateurs radiaux, DO-41) : soudure au fer classique.",
    "À prévoir sur la carte : un plan de masse, aucun cuivre sous l'antenne de l'ESP32, 4 trous de fixation (45 x 50 mm).",
    "Sérigraphie : nom de chaque connecteur, repère de la broche 1, et le signal de chaque broche (+5 V, GND, SSR +, SSR −, signal...).",
]
for i, t in enumerate(notes):
    T(60, 998 + i * 34, "• " + t, F(16), INK, 'lm')

im = im.resize((W, H), Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/carrier_schema.png')
print('ok')
