# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S=2; K=10
W,H=1600,980
im=Image.new('RGB',(W*S,H*S),(246,246,242)); d=ImageDraw.Draw(im)
def F(s,b=False): return ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s*S)
def R(x0,y0,x1,y1,**k): d.rectangle([x0*S,y0*S,x1*S,y1*S],**k)
def RR(x0,y0,x1,y1,r,**k): d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,**k)
def E(x0,y0,x1,y1,**k): d.ellipse([x0*S,y0*S,x1*S,y1*S],**k)
def L(pts,c,w): d.line([(x*S,y*S) for x,y in pts],fill=c,width=int(w*S))
def Tx(x,y,s,f,c=(30,30,36),a='mm'): d.text((x*S,y*S),s,font=f,fill=c,anchor=a)
INK=(30,30,36); GRY=(110,110,116); RED=(200,50,50); GRN=(20,120,60); BLU=(30,90,170); ORG=(200,120,20)
Tx(W/2,36,"Le boîtier avec la carte ESP32-S3 et le module MAX31865 (estimations d'après les photos, ±2 mm)",F(30,True))
# ---------------- top view (length 81 vertical? no: draw landscape: length 81 horizontal, width 55 vertical)
cx,cy=510,430
iw,ih=81,55
x0,y0,x1,y1=cx-iw*K/2,cy-ih*K/2,cx+iw*K/2,cy+ih*K/2
RR(x0-26,y0-26,x1+26,y1+26,14,fill=(52,52,58),outline=(30,30,34),width=4); R(x0,y0,x1,y1,fill=(70,70,78))
for sx in (-1,1):
    for sy in (-1,1):
        px,py=cx+sx*37*K,cy+sy*26*K
        E(px-3.8*K,py-3.8*K,px+3.8*K,py+3.8*K,fill=(30,30,34),outline=(110,110,118),width=3); E(px-1*K,py-1*K,px+1*K,py+1*K,fill=(70,70,78))
for sx in (-1,1):
    for sy in (-1,1):
        px,py=cx+sx*19.5*K,cy+sy*18*K          # small standoffs: 39 x 36 mm
        E(px-2.4*K,py-2.4*K,px+2.4*K,py+2.4*K,fill=(30,30,34),outline=(150,150,158),width=2)
# the carrier 64 x 52 mm (green), no notch: between the 4 posts
pw,ph=64,52
px0,py0=cx-pw*K/2,cy-ph*K/2
R(px0,py0,px0+pw*K,py0+ph*K,fill=(20,100,60)); d.rectangle([px0*S,py0*S,(px0+pw*K)*S,(py0+ph*K)*S],outline=GRN,width=5)
# the ESP32 board 46 x 17 (USB-C to the left), the MAX31865 module 25 x 20 beside it
ex0,ey0=px0+4*K,py0+4*K
RR(ex0,ey0,ex0+46*K,ey0+17*K,4,fill=(235,235,240),outline=(150,150,158),width=2)
RR(ex0-3*K,ey0+5*K,ex0+3.2*K,ey0+12*K,3,fill=(190,194,200),outline=(120,124,130),width=2)
Tx(ex0+22*K,ey0+8.5*K,"ESP32-S3  46 x 17",F(15,True),(60,60,66))
RR(ex0+38*K,ey0+4*K,ex0+46*K,ey0+13*K,3,fill=(236,226,196),outline=(180,170,140),width=1); Tx(ex0+42*K,ey0+8.5*K,"ant.",F(10),(120,110,80))
mx0,my0=px0+4*K,py0+26*K
RR(mx0,my0,mx0+25*K,my0+20*K,4,fill=(20,70,150),outline=(180,200,240),width=2); Tx(mx0+12.5*K,my0+10*K,"MAX31865",F(15,True),(235,240,250))
Tx(mx0+12.5*K,my0+14*K,"25 x 20",F(12),(200,215,240))
for i in range(3): RR(px0+36*K+i*7*K,py0+30*K,px0+36*K+i*7*K+4*K,py0+30*K+5*K,2,fill=(24,24,28))
Tx(px0+43*K,py0+39*K,"3 transistors",F(12),(230,240,230))
for i in range(6): RR(px0+36*K+i*4.7*K,py0+22*K,px0+36*K+i*4.7*K+4*K,py0+22*K+5*K,1,fill=(40,100,170),outline=(15,50,110),width=1)
Tx(px0+48*K,py0+20*K,"borniers",F(11),(230,240,250))
Tx(cx,y1+52,"Vue de dessus : carte porteuse 64 x 52 mm entre les 4 gros plots, vissée sur les 4 petits",F(20,True),GRN)
Tx(cx,y1+80,"(plots d'angle : 74 x 52 mm entre axes ; petits plots : 39 x 36 mm entre axes)",F(18),GRY)
d.line([(x0*S,(y0-44)*S),(x1*S,(y0-44)*S)],fill=GRY,width=2*S); Tx(cx,y0-60,"≈ 81 mm (intérieur)",F(16),GRY)
d.line([((x0-52)*S,y0*S),((x0-52)*S,y1*S)],fill=GRY,width=2*S); Tx(x0-84,cy,"≈ 55",F(16),GRY)
# ---------------- side view (height)
sx0,sy0=990,150
hh=35*K   # 35 mm total
Tx(1240,118,"Vue de côté : 35 mm de hauteur utile",F(22,True))
R(sx0,sy0,sx0+500,sy0+hh,fill=(246,246,242),outline=(60,60,66),width=3)
L([(sx0,sy0+hh/2),(sx0+500,sy0+hh/2)],(150,150,158),2)
Tx(sx0+250,sy0+hh/2+11,"",F(12),GRY)
fl=sy0+hh   # floor
R(sx0,fl,sx0+500,fl+14,fill=(52,52,58))
# standoffs 6 mm, carrier 1.6, headers 8.5, ESP 1.6, USB 3.2
st=6*K; pcb=1.6*K
for x in (sx0+40,sx0+440): R(x,fl-st,x+16,fl,fill=(110,110,118))
R(sx0+20,fl-st-pcb,sx0+480,fl-st,fill=(20,100,60)); Tx(sx0+250,fl-st-pcb/2,"carte porteuse 1,6",F(11),(230,240,230))
hdr=8.5*K
R(sx0+60,fl-st-pcb-hdr,sx0+330,fl-st-pcb,fill=(30,30,34)); Tx(sx0+195,fl-st-pcb-hdr/2,"supports 8,5",F(11),(230,230,235))
R(sx0+60,fl-st-pcb-hdr-pcb,sx0+330,fl-st-pcb-hdr,fill=(235,235,240),outline=(150,150,158),width=1)
R(sx0+60,fl-st-pcb-hdr-pcb-3.2*K,sx0+110,fl-st-pcb-hdr-pcb,fill=(190,194,200),outline=(120,124,130),width=1)
Tx(sx0+90,fl-st-pcb-hdr-pcb-3.2*K-14,"USB-C",F(11,True),INK)
Tx(sx0+195,fl-st-pcb-hdr-pcb-3.2*K-14,"ESP32-S3",F(11,True),INK)
# MAX module on a second level at the side (10 mm standoffs)
R(sx0+350,fl-st-pcb-10*K,sx0+366,fl-st-pcb,fill=(110,110,118)); R(sx0+440,fl-st-pcb-10*K,sx0+456,fl-st-pcb,fill=(110,110,118))
R(sx0+340,fl-st-pcb-10*K-pcb,sx0+470,fl-st-pcb-10*K,fill=(20,70,150)); Tx(sx0+405,fl-st-pcb-10*K-pcb/2,"MAX31865",F(11,True),(235,240,250))
R(sx0+395,fl-st-pcb-10*K-pcb-8*K,sx0+450,fl-st-pcb-10*K-pcb,fill=(40,100,170),outline=(15,50,110),width=1); Tx(sx0+422,fl-st-pcb-10*K-pcb-4*K,"borne",F(10),(235,240,250))
d.line([((sx0+520)*S),(sy0*S),((sx0+520)*S),((sy0+hh)*S)],fill=GRY,width=2*S); Tx(sx0+560,sy0+hh/2,"≈ 35",F(16),GRY)
Tx(sx0+250,fl+50,"Les deux niveaux sont possibles :",F(15,True),INK)
Tx(sx0+250,fl+74,"côte à côte (comme à gauche) ou le MAX31865 sur un second étage",F(15),INK)
Tx(sx0+250,fl+98,"(entretoises de 10 mm) au-dessus de la carte. Trait gris = séparation des moitiés (≈ 17,5 mm chacune).",F(13),INK)
# pin check
Tx(990,690,"Broches de ta carte (lues sur la photo) :",F(20,True),INK,'lm')
rows=["gauche  : GND  5V  G48  BOT  48  47  38  39  40  21  GND  GND  18  17  16  15  41  42  45  46",
      "droite  : GND  3V3  PWR  RST  14  13  12  11  10  09  08  07  GND  06  05  04  03  02  01"]
for i,r in enumerate(rows): Tx(990,722+i*26,r,F(12),INK,'lm')
Tx(990,790,"Les broches prévues sont toutes présentes :",F(16,True),GRN,'lm')
Tx(990,818,"SPI 11 / 12 / 13 · écran 8, 9, 10, 14 · MAX 7 · encodeur 4, 5 · start 6",F(14),INK,'lm')
Tx(990,842,"débit 15, 16 · SSR 17, 18, 21 · 45 et 46 (amorçage) restent libres",F(14),INK,'lm')
im=im.resize((W,H),Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/box_fit2.png'); print('ok')
