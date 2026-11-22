# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=2; W,H=1800,1100
im=Image.new('RGB',(W*S,H*S),(238,238,234)); d=ImageDraw.Draw(im)
def F(s,b=False): return ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s*S)
def R(x0,y0,x1,y1,**k): d.rectangle([x0*S,y0*S,x1*S,y1*S],**k)
def RR(x0,y0,x1,y1,r,**k): d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,**k)
def E(x0,y0,x1,y1,**k): d.ellipse([x0*S,y0*S,x1*S,y1*S],**k)
def L(pts,c,w): d.line([(x*S,y*S) for x,y in pts],fill=c,width=int(w*S),joint='curve')
def Tx(x,y,s,f,c=(30,30,36),a='mm'): d.text((x*S,y*S),s,font=f,fill=c,anchor=a)
INK=(30,30,36); GRY=(110,110,116)
Tx(W/2,44,"Le montage : la carte ESP32-S3 « Nano » sur une carte porteuse, reliée à la machine",F(36,True))
Tx(W/2,86,"Illustration de principe (brochage de la carte non confirmé). Tout est en basse tension : le secteur reste dans les SSR.",F(22),GRY)
# ---------- carrier board (center)
bx0,by0,bx1,by1=560,260,1240,820
sh=Image.new('RGBA',(W*S,H*S),(0,0,0,0)); sd=ImageDraw.Draw(sh)
sd.rounded_rectangle([(bx0+12)*S,(by0+16)*S,(bx1+12)*S,(by1+16)*S],22*S,fill=(0,0,0,110)); sh=sh.filter(ImageFilter.GaussianBlur(12*S)); im.paste(sh,(0,0),sh); d=ImageDraw.Draw(im)
RR(bx0,by0,bx1,by1,22,fill=(18,92,56),outline=(10,60,36),width=4)
Tx((bx0+bx1)//2,by1-24,"carte porteuse (environ 90 x 70 mm)",F(20,True),(225,235,225))
# socket rows + ESP32-S3 nano board plugged on top
RR(640,330,1160,372,3,fill=(30,30,34)); RR(640,430,1160,472,3,fill=(30,30,34))   # female headers
# the dev board (blue-ish PCB, black)
RR(610,350,1190,452,8,fill=(28,28,34),outline=(70,70,78),width=3)
# castellated header pins gold dots
for i in range(15):
    E(650+i*34,338,664+i*34,352,fill=(214,168,80)); E(650+i*34,450,664+i*34,464,fill=(214,168,80))
# USB-C on left end of the dev board
RR(588,380,640,422,5,fill=(190,194,200),outline=(120,124,130),width=2); RR(596,396,632,406,4,fill=(40,44,50))
# module shield + ceramic antenna at the right end
RR(820,362,1000,440,4,fill=(185,189,195),outline=(120,124,130),width=2); Tx(910,394,"ESP32-S3",F(18,True),(70,74,80)); Tx(910,418,"N16R8",F(15),(90,94,100))
RR(1070,372,1150,430,6,fill=(236,226,196),outline=(180,170,140),width=2); Tx(1110,401,"antenne",F(13),(120,110,80))
# LEDs & buttons on the dev board
for x,c in [(700,(70,200,90)),(716,(240,180,40))]: RR(x,372,x+10,380,2,fill=c)
Tx(780,395,"BOOT RST",F(12),(180,180,186))
Tx(900,320,"carte ESP32-S3 Nano (N16R8), enfichée",F(22,True),(240,240,240))
# MAX31865 module plugged (right-bottom)
RR(900,560,1060,700,6,fill=(20,70,150),outline=(12,40,100),width=3); Tx(980,612,"MAX31865",F(22,True),(235,240,250)); Tx(980,642,"module PT100",F(16),(200,215,240)); R(920,676,1040,690,fill=(214,168,80))
# SSR driver transistors (3 small blocks)
for i,x in enumerate((640,700,760)):
    RR(x,580,x+36,610,3,fill=(24,24,28)); Tx(x+18,628,"Q%d"%(i+1),F(14),(230,235,230))
Tx(700,560,"3 transistors (pilotes SSR)",F(16,True),(230,240,230))
# regulator + caps
RR(660,680,740,730,4,fill=(24,24,28)); Tx(700,705,"3V3",F(15,True),(210,210,215)); Tx(700,750,"5 V → 3,3 V",F(14),(225,235,225))
E(780,680,840,740,fill=(70,76,84),outline=(30,34,40),width=3); Tx(810,710,"470µ",F(13,True),(220,224,230))
# edge connectors on carrier: left & right
def conn(x,y,w,h,label,c=(40,100,170)):
    RR(x,y,x+w,y+h,4,fill=c,outline=(15,50,110),width=3); Tx(x+w/2,y+h/2,label,F(15,True),(240,245,250) if c==(40,100,170) else (30,30,36))
conn(528,300,54,60,"J1")
conn(528,400,54,90,"J2"); conn(528,520,54,90,"J3")
conn(1218,300,54,100,"J4",(235,235,228)); conn(1218,430,54,70,"J5",(235,235,228)); conn(1218,530,54,50,"J6",(235,235,228)); conn(1218,610,54,70,"J7",(235,235,228))
for (x,y,w,h) in [(1218,300,54,100),(1218,430,54,70),(1218,530,54,50),(1218,610,54,70)]:
    Tx(x+27,y+h/2,"",F(12))
# ---------- peripherals
def box(x0,y0,x1,y1,label,sub,fill,outline=INK,fc=INK):
    RR(x0,y0,x1,y1,12,fill=fill,outline=outline,width=3); Tx((x0+x1)/2,(y0+y1)/2-12,label,F(21,True),fc); Tx((x0+x1)/2,(y0+y1)/2+16,sub,F(15),GRY if fc==INK else (225,225,225))
# power supply (left top)
box(60,180,330,300,"Alimentation 5 V","2 A, 5,15 V mesuré",(222,244,228),(40,120,70))
# SSR block (left middle)
box(60,380,330,560,"3 SSR","pompe (DC) · chaudière · vanne (AC)",(222,232,250),(40,90,170))
# flow sensors (left bottom)
box(60,640,330,760,"2 capteurs de débit","In (A1) · Out (A2)",(250,236,214),(190,120,30))
# display round (right top)
E(1380,150,1640,410,fill=(14,14,18),outline=(150,150,156),width=6); E(1400,170,1620,390,fill=(32,20,6),outline=(70,70,76),width=3)
Tx(1510,255,"131",F(60,True),(254,245,228)); Tx(1570,280,"°C",F(26,True),(254,245,228)); Tx(1510,330,"STEAM",F(18,True),(250,186,107))
Tx(1510,440,"écran rond GC9A01",F(19,True))
# encoder
E(1400,490,1500,590,fill=(60,60,66),outline=(30,30,34),width=4); E(1420,510,1480,570,fill=(120,120,126))
Tx(1590,540,"encodeur",F(19,True))
RR(1400,625,1500,685,12,fill=(200,50,50),outline=(110,20,20),width=3); Tx(1450,655,"START",F(19,True),(250,240,240)); Tx(1590,655,"bouton",F(19,True))
# PT100 probe
RR(1360,730,1660,760,10,fill=(160,164,170),outline=(90,94,100),width=3); RR(1640,722,1680,768,6,fill=(100,104,110)); Tx(1510,805,"sonde PT100 (chaudière)",F(19,True))
# USB / PC (bottom center)
box(740,900,1060,1020,"USB-C : PC","téléversement, debug (machine éteinte)",(230,238,252),(40,90,170))
# ---------- wires
def wire(pts,c,w=5): L(pts,c,w)
wire([(330,240),(430,240),(430,320),(528,320)],(190,40,40))            # supply -> J1
wire([(330,470),(528,445)],(40,90,170)); wire([(330,495),(528,470)],(40,90,170))   # SSR -> J2
wire([(330,700),(430,700),(430,565),(528,565)],(190,120,30))             # flow -> J3
wire([(1272,350),(1380,300)],(90,90,96))                                   # J4 -> display
wire([(1272,465),(1400,535)],(90,90,96)); wire([(1272,555),(1400,655)],(90,90,96))
wire([(1272,645),(1360,745)],(90,90,96))
wire([(900,830),(900,900)],(40,90,170),4)                                   # USB
# labels on connectors
Tx(430,215,"5 V + GND",F(15),(190,40,40)); Tx(440,440,"3 sorties",F(15),(40,90,170)); Tx(430,730,"signaux + 5 V",F(15),(190,120,30))
Tx(1330,265,"SPI",F(15),GRY); Tx(1318,495,"A, B",F(15),GRY); Tx(1320,715,"2 à 4 fils",F(15),GRY)
im=im.resize((W,H),Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/montage_esp32s3.png'); print('ok')
