# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S=2; K=10
W,H=1600,1000
im=Image.new('RGB',(W*S,H*S),(246,246,242)); d=ImageDraw.Draw(im)
def F(s,b=False): return ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s*S)
def R(x0,y0,x1,y1,**k): d.rectangle([x0*S,y0*S,x1*S,y1*S],**k)
def RR(x0,y0,x1,y1,r,**k): d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,**k)
def E(x0,y0,x1,y1,**k): d.ellipse([x0*S,y0*S,x1*S,y1*S],**k)
def L(pts,c,w): d.line([(x*S,y*S) for x,y in pts],fill=c,width=int(w*S))
def Tx(x,y,s,f,c=(30,30,36),a='mm'): d.text((x*S,y*S),s,font=f,fill=c,anchor=a)
INK=(30,30,36); GRY=(110,110,116); RED=(200,50,50); GRN=(20,120,60); BLU=(30,90,170)
Tx(W/2,34,"Carte porteuse dans le boîtier : zone libre 60 x 70 mm entre les gros plots",F(30,True))
# top view: width 60 (x), length 70 (y) ; origin center
cx,cy=470,520
fw,fl=60,70
x0,y0,x1,y1=cx-fw*K/2,cy-fl*K/2,cx+fw*K/2,cy+fl*K/2
RR(x0-70,y0-70,x1+70,y1+70,16,fill=(52,52,58),outline=(30,30,34),width=4)
R(x0-44,y0-44,x1+44,y1+44,fill=(70,70,78))
# big posts outside the free area
for sx in (-1,1):
    for sy in (-1,1):
        px,py=cx+sx*(fw/2+2.5)*K,cy+sy*(fl/2+2.5)*K
        E(px-4*K,py-4*K,px+4*K,py+4*K,fill=(30,30,34),outline=(110,110,118),width=3); E(px-1*K,py-1*K,px+1*K,py+1*K,fill=(70,70,78))
# free area dashed
d.rectangle([x0*S,y0*S,x1*S,y1*S],outline=(200,200,205),width=2*S)
# the carrier: 58 x 68
pw,ph=58,68
px0,py0=cx-pw*K/2,cy-ph*K/2
R(px0,py0,px0+pw*K,py0+ph*K,fill=(20,100,60)); d.rectangle([px0*S,py0*S,(px0+pw*K)*S,(py0+ph*K)*S],outline=GRN,width=5)
def P(x,y): return cx+x*K,cy+y*K     # mm from the center
# ESP32 board 21 x 52 at the left (USB-C at the top)
a,b=P(-28,-31); c,dd=P(-7,21)
RR(a,b,c,dd,4,fill=(236,236,241),outline=(150,150,158),width=2)
RR(a+4.5*K,b-3*K,a+16.5*K,b+3*K,3,fill=(190,194,200),outline=(120,124,130),width=2); Tx((a+c)/2,b-6*K,"USB-C",F(13,True),INK)
Tx((a+c)/2,(b+dd)/2,"ESP32-S3",F(20,True),(60,60,66)); Tx((a+c)/2,(b+dd)/2+28,"21 x 52",F(15),GRY)
RR(a+3*K,dd-9*K,c-3*K,dd-1*K,3,fill=(236,226,196),outline=(180,170,140),width=1); Tx((a+c)/2,dd-5*K,"antenne",F(12),(120,110,80))
Tx((a+c)/2,dd-5*K-26,"rien sous",F(11,True),RED)
# MAX31865 module 25 x 28 at the right (top)
a,b=P(-6,-31); c,dd=P(19,-3)
RR(a,b,c,dd,4,fill=(20,70,150),outline=(180,200,240),width=2); Tx((a+c)/2,(b+dd)/2-10,"MAX31865",F(20,True),(235,240,250)); Tx((a+c)/2,(b+dd)/2+18,"25 x 28 (hauteur 15)",F(14),(200,215,240))
# transistors
for i in range(3):
    a,b=P(-4+i*8,1)
    RR(a,b,a+5*K,b+4*K,2,fill=(24,24,28))
Tx(P(7,8)[0],P(7,8)[1],"3 transistors + résistances",F(13),(230,240,230))
# terminal blocks (3 rows of 7, 3.5 mm)
for r in range(3):
    for i in range(7):
        a,b=P(-6+i*3.55,11+r*7.5)
        RR(a,b,a+3.3*K,b+6*K,1,fill=(40,100,170),outline=(15,50,110),width=1)
Tx(P(6.5,31.5)[0],P(6.5,31.5)[1],"borniers : 5 V, SSR x3, débit x2, bouton",F(13),(230,240,250))
# right strip headers (display / encoder)
for i in range(8):
    a,b=P(25.5,-31+i*2.54)
    RR(a,b,a+2.2*K,b+2.2*K,1,fill=(235,235,228),outline=(180,180,172),width=1)
Tx(P(26.5,-8)[0],P(26.5,-8)[1]+8,"écran",F(11),(230,240,230))
for i in range(5):
    a,b=P(25.5,-4+i*2.54)
    RR(a,b,a+2.2*K,b+2.2*K,1,fill=(235,235,228),outline=(180,180,172),width=1)
Tx(P(26.5,10)[0],P(26.5,10)[1],"encodeur",F(11),(230,240,230))
for sx in (-1,1):
    for sy in (-1,1):
        px,py=P(sx*22.5,sy*25)
        E(px-2.6*K,py-2.6*K,px+2.6*K,py+2.6*K,outline=(250,250,250),width=3); E(px-1.1*K,py-1.1*K,px+1.1*K,py+1.1*K,fill=(70,70,78))
Tx(cx,y1+98,"Zone libre 60 x 70 mm (pointillé) · carte 58 x 68 mm · petits plots 45 x 50 mm",F(18,True),GRN)
Tx(cx,y1+124,"Les vis des deux plots de gauche passent sous la carte ESP32 (surélevée de 8,5 mm sur ses supports).",F(15),GRY)
# side view
sx0,sy0=990,150
hh=25*K
Tx(1240,100,"Vue de côté : 25 mm de profondeur",F(22,True))
R(sx0,sy0,sx0+500,sy0+hh,fill=(246,246,242),outline=(60,60,66),width=3)
fl_=sy0+hh; R(sx0,fl_,sx0+500,fl_+14,fill=(52,52,58))
st=4*K; pcb=1.6*K
for x in (sx0+30,sx0+450): R(x,fl_-st,x+16,fl_,fill=(110,110,118))
R(sx0+20,fl_-st-pcb,sx0+480,fl_-st,fill=(20,100,60)); Tx(sx0+250,fl_-st-pcb/2,"carte porteuse 1,6",F(11),(230,240,230))
hdr=8.5*K
R(sx0+40,fl_-st-pcb-hdr,sx0+190,fl_-st-pcb,fill=(30,30,34)); Tx(sx0+115,fl_-st-pcb-hdr/2,"supports 8,5",F(11),(230,230,235))
R(sx0+40,fl_-st-pcb-hdr-pcb,sx0+190,fl_-st-pcb-hdr,fill=(235,235,240),outline=(150,150,158),width=1)
R(sx0+40,fl_-st-pcb-hdr-pcb-3.2*K,sx0+90,fl_-st-pcb-hdr-pcb,fill=(190,194,200),outline=(120,124,130),width=1); Tx(sx0+65,fl_-st-pcb-hdr-pcb-3.2*K-12,"USB-C",F(11,True),INK)
Tx(sx0+140,fl_-st-pcb-hdr-pcb-3.2*K-12,"ESP32 : sommet 18,9",F(11,True),INK)
mh=3*K
R(sx0+230,fl_-st-pcb-mh,sx0+330,fl_-st-pcb,fill=(30,30,34)); Tx(sx0+280,fl_-st-pcb-mh/2,"supports bas 3",F(10),(230,230,235))
R(sx0+230,fl_-st-pcb-mh-15*K,sx0+330,fl_-st-pcb-mh,fill=(20,70,150),outline=(180,200,240),width=1); Tx(sx0+280,fl_-st-pcb-mh-7.5*K,"MAX31865 15",F(12,True),(235,240,250))
d.line([((sx0+520)*S),(sy0*S),((sx0+520)*S),((sy0+hh)*S)],fill=GRY,width=2*S); Tx(sx0+560,sy0+hh/2,"25",F(16),GRY)
Tx(sx0+250,fl_+48,"Plots 4 + carte 1,6 + supports 3 + MAX 15 = 23,6 mm : sous les 25 mm",F(14,True),GRN)
Tx(sx0+250,fl_+72,"mais seulement 1,4 mm de marge : mesure la hauteur des petits plots.",F(13),RED)
Tx(sx0+250,fl_+98,"Des supports de 8,5 mm pour le MAX donneraient 29 mm : impossible.",F(13),GRY)
Tx(sx0+250,fl_+122,"(hauteur des plots : 4 mm supposés, à vérifier)",F(13),GRY)
im=im.resize((W,H),Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/box_fit3.png'); print('ok')
