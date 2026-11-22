# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=2   # supersampling
W,H=1500,1100
im=Image.new('RGB',(W*S,H*S),(40,44,52)); d=ImageDraw.Draw(im)
def F(s,b=False): return ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s*S)
def R(x0,y0,x1,y1,**k): d.rectangle([x0*S,y0*S,x1*S,y1*S],**k)
def RR(x0,y0,x1,y1,r,**k): d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,**k)
def E(x0,y0,x1,y1,**k): d.ellipse([x0*S,y0*S,x1*S,y1*S],**k)
def L(pts,c,w): d.line([(x*S,y*S) for x,y in pts],fill=c,width=int(w*S),joint='curve')
def Tx(x,y,s,f,c,a='la'): d.text((x*S,y*S),s,font=f,fill=c,anchor=a)
# background title
Tx(W/2,46,"Rendu d'illustration : carte de commande ESP32-S3 (80 x 60 mm)",F(36,True),(235,235,235),'mm')
Tx(W/2,90,"Vue de dessus, dessin de principe : ce n'est pas la sortie d'un logiciel de CAO.",F(22),(170,175,185),'mm')
# shadow
sh=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); sd=ImageDraw.Draw(sh)
bx0,by0,bx1,by1=250,250,1250,990
sd.rounded_rectangle([(bx0+14)*S,(by0+18)*S,(bx1+14)*S,(by1+18)*S],26*S,fill=(0,0,0,150))
sh=sh.filter(ImageFilter.GaussianBlur(14*S)); im.paste(sh,(0,0),sh); d=ImageDraw.Draw(im)
# board: green soldermask
RR(bx0,by0,bx1,by1,26,fill=(18,92,56),outline=(10,60,36),width=4)
# subtle inner edge
RR(bx0+8,by0+8,bx1-8,by1-8,20,outline=(26,112,70),width=2)
# ground-fill hatch (copper pour hint)
for x in range(bx0+90,bx1-30,18):
    L([(x,by0+30),(x-60,by1-30)],(22,102,62),1)
# traces (light copper-ish under mask)
TR=(46,140,92)
def trace(pts): L(pts,TR,5)
trace([(330,420),(330,640),(520,640)]); trace([(380,420),(380,600),(520,600)])
trace([(700,560),(700,700),(900,700)]); trace([(760,560),(760,730),(960,730)])
trace([(1000,420),(1000,520),(1120,520)]); trace([(900,330),(1120,330),(1120,420)])
trace([(560,820),(820,820),(820,760)]); trace([(430,900),(430,760),(560,760)])
# mounting holes
for (x,y) in [(285,285),(1215,285),(285,955),(1215,955)]:
    E(x-20,y-20,x+20,y+20,fill=(214,168,80),outline=(150,110,40),width=3); E(x-11,y-11,x+11,y+11,fill=(40,44,52))
# silkscreen helper
WH=(238,238,230)
def sil(x,y,s,sz=16,b=False,a='la'): Tx(x,y,s,F(sz,b),WH,a)
# ESP32 module: silver shield + antenna board with meander
RR(560,262,920,420,4,fill=(30,100,60))   # antenna area (module PCB, green)
# meander antenna
pts=[]; x=590; y=300; 
meander=[(590,395),(590,285),(620,285),(620,395),(650,395),(650,285),(680,285),(680,395),(710,395),(710,285),(740,285),(740,395),(770,395),(770,285),(800,285),(800,395),(830,395),(830,285)]
L(meander,(214,168,80),5)
RR(560,420,920,640,6,fill=(180,184,190),outline=(120,124,130),width=3)  # metal shield
RR(572,432,908,628,4,outline=(150,154,160),width=2)
Tx(740,500,"ESP32-S3",F(34,True),(70,74,80),'mm'); Tx(740,545,"WROOM-1",F(26),(90,94,100),'mm')
Tx(740,590,"ESPRESSIF",F(16),(110,114,120),'mm')
# castellated pads along module sides
for i in range(14):
    R(552,430+i*14,566,438+i*14,fill=(214,168,80)); R(914,430+i*14,928,438+i*14,fill=(214,168,80))
# MAX31865 (QFN)
RR(930,560,1010,640,4,fill=(24,24,28)); Tx(970,600,"MAX",F(14,True),(200,200,205),'mm'); Tx(970,618,"31865",F(14),(200,200,205),'mm')
E(938,568,946,576,fill=(120,120,125))
# LDO regulator (SOT-223)
RR(360,700,440,760,4,fill=(24,24,28)); Tx(400,730,"3V3",F(15,True),(200,200,205),'mm')
for i in range(3): R(366+i*25,760,380+i*25,776,fill=(190,194,200))
R(380,684,420,700,fill=(190,194,200))
# SSR driver transistors (SOT-23) x3
for i,x in enumerate((900,950,1000)):
    RR(x,720,x+30,744,3,fill=(24,24,28))
    R(x+2,744,x+8,754,fill=(190,194,200)); R(x+22,744,x+28,754,fill=(190,194,200)); R(x+12,708,x+18,720,fill=(190,194,200))
# Schmitt trigger IC (SSOP)
RR(1000,350,1070,390,3,fill=(24,24,28)); Tx(1035,370,"74LVC",F(13,True),(200,200,205),'mm')
# resistors / caps (SMD 0603 style)
import random; random.seed(3)
def smd(x,y,hor=True,c=(30,30,34)):
    if hor: RR(x,y,x+22,y+12,2,fill=c); R(x,y,x+4,y+12,fill=(190,194,200)); R(x+18,y,x+22,y+12,fill=(190,194,200))
    else: RR(x,y,x+12,y+22,2,fill=c); R(x,y,x+12,y+4,fill=(190,194,200)); R(x,y+18,x+12,y+22,fill=(190,194,200))
for (x,y,h) in [(470,520,True),(470,545,True),(470,570,True),(600,680,True),(630,680,True),(660,680,True),(850,790,True),(880,790,True),(910,790,True),(940,790,True),(1010,690,False),(1040,690,False),(1070,690,False),(1100,690,False),(560,700,False),(590,700,False),(520,760,True),(520,790,True),(1060,450,True),(1060,475,True),(1060,500,True)]:
    smd(x,y,h)
# electrolytic capacitor
E(470,640,540,710,fill=(70,76,84),outline=(30,34,40),width=3); E(480,650,530,700,fill=(150,156,164)); Tx(505,675,"470µ",F(13,True),(40,44,50),'mm')
# polyfuse & diode
RR(380,470,440,500,3,fill=(220,200,90)); RR(450,470,480,500,3,fill=(30,30,34)); R(452,470,458,500,fill=(200,200,205))
# LEDs
for i,c in enumerate([(70,200,90),(240,180,40),(230,60,60)]): RR(990+i*22,860,1008+i*22,872,2,fill=c)
# buttons BOOT / RESET
for x in (640,720):
    RR(x,880,x+54,934,6,fill=(30,30,34)); E(x+12,892,x+42,922,fill=(190,194,200))
sil(667,946,"BOOT",14,False,'ma'); sil(747,946,"RESET",14,False,'ma')
# USB-C at bottom edge
RR(430,935,520,1010,6,fill=(180,184,190),outline=(120,124,130),width=3); RR(442,990,508,1004,6,fill=(30,30,34))
sil(475,926,"USB-C",16,True,'ma')
# screw terminal J1 (left)
def terminal(x,y,n,label):
    RR(x,y,x+60,y+n*50,4,fill=(40,100,170),outline=(20,60,110),width=3)
    for i in range(n):
        E(x+14,y+i*50+10,x+46,y+i*50+40,fill=(190,194,200),outline=(110,114,120),width=2); L([(x+18,y+i*50+25),(x+42,y+i*50+25)],(90,94,100),3)
    sil(x-10,y+n*25,label,16,True,'rm')
terminal(262,330,2,"J1 5V"); terminal(262,470,3,"J2 SSR"); terminal(262,640,3,"J3 débit")
# JST/pin headers on the right edge
def header(x,y,n,label):
    RR(x,y,x+44,y+n*34,3,fill=(235,235,228),outline=(180,180,172),width=2)
    for i in range(n): RR(x+12,y+i*34+9,x+32,y+i*34+25,2,fill=(30,30,34)); R(x+18,y+i*34+14,x+26,y+i*34+20,fill=(214,168,80))
    sil(x-10,y+n*17,label,16,True,'rm')
header(1196,290,8,"J4 écran"); header(1196,580,5,"J5 enc."); header(1196,760,3,"J6 start"); header(1196,880,4,"J7 PT100")
# silkscreen labels
sil(900,966,"coffee_screen  ESP32-S3  rev A",18,True,'ma')
sil(400,810,"5V → 3V3",16,False,'ma'); sil(950,770,"Q1 Q2 Q3  (SSR)",15,False,'ma'); sil(970,548,"U2",15,False,'ma'); sil(1035,340,"U3",15,False,'ma')
sil(740,665,"U1",15,False,'ma')
# board outline note: antenna overhang
Tx(740,225,"antenne : rien sous cette zone",F(18),(220,200,120),'mm')
im=im.resize((W,H),Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/pcb_render.png')
print('ok')
