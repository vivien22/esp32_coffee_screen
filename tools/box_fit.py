# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
S=2; K=11    # 14 px per mm (x2 supersample)
W,H=1500,900
im=Image.new('RGB',(W*S,H*S),(246,246,242)); d=ImageDraw.Draw(im)
def F(s,b=False): return ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s*S)
def R(x0,y0,x1,y1,**k): d.rectangle([x0*S,y0*S,x1*S,y1*S],**k)
def RR(x0,y0,x1,y1,r,**k): d.rounded_rectangle([x0*S,y0*S,x1*S,y1*S],r*S,**k)
def E(x0,y0,x1,y1,**k): d.ellipse([x0*S,y0*S,x1*S,y1*S],**k)
def Tx(x,y,s,f,c=(30,30,36),a='mm'): d.text((x*S,y*S),s,font=f,fill=c,anchor=a)
INK=(30,30,36); GRY=(110,110,116); RED=(200,50,50); GRN=(20,120,60); BLU=(30,90,170)
Tx(W/2,40,"Le boîtier et les cartes : ce qui rentre (vue de dessus, à l'échelle)",F(34,True))
Tx(W/2,82,"Dimensions estimées d'après les photos (marge d'erreur environ ±3 mm) : à confirmer au pied à coulisse.",F(20),GRY)
# box interior 71 x 52 mm centered at (cx,cy)
cx,cy=520,470
iw,ih=71,52
bx0,by0,bx1,by1=cx-iw*K/2,cy-ih*K/2,cx+iw*K/2,cy+ih*K/2
RR(bx0-14,by0-14,bx1+14,by1+14,16,fill=(52,52,58),outline=(30,30,34),width=4)   # outer wall
R(bx0,by0,bx1,by1,fill=(70,70,78))
# 4 corner posts (screws of the lid), diameter 9 mm, centers about 5.5 mm from the inner corners
for sx in (-1,1):
    for sy in (-1,1):
        px=cx+sx*(iw/2-5.0)*K; py=cy+sy*(ih/2-5.0)*K
        E(px-4.5*K,py-4.5*K,px+4.5*K,py+4.5*K,fill=(30,30,34),outline=(110,110,118),width=3); E(px-1.2*K,py-1.2*K,px+1.2*K,py+1.2*K,fill=(70,70,78))
# 4 small standoffs for a PCB: about 42 x 41 mm pattern
for sx in (-1,1):
    for sy in (-1,1):
        px=cx+sx*21*K; py=cy+sy*20.5*K
        E(px-2.6*K,py-2.6*K,px+2.6*K,py+2.6*K,fill=(30,30,34),outline=(150,150,158),width=2); E(px-0.8*K,py-0.8*K,px+0.8*K,py+0.8*K,fill=(70,70,78))
# my first concept: 80 x 60 mm (red, does not fit)
def outline(w,h,c,label):
    x0,y0,x1,y1=cx-w*K/2,cy-h*K/2,cx+w*K/2,cy+h*K/2
    d.rectangle([x0*S,y0*S,x1*S,y1*S],outline=c,width=5*S//2)
outline(80,60,RED,"")
Tx(cx-40*K+10,cy+30*K-14,"première idée : 80 x 60 mm, ne rentre pas",F(17,True),RED,'lm')
# proposed: 62 x 44 mm carrier with a notch of 10 x 10 mm in each corner (the posts of the lid)
pw,ph,nt=62,44,10
px0,py0=cx-pw*K/2,cy-ph*K/2
pts=[(px0+nt*K,py0),(px0+(pw-nt)*K,py0),(px0+(pw-nt)*K,py0+nt*K),(px0+pw*K,py0+nt*K),(px0+pw*K,py0+(ph-nt)*K),(px0+(pw-nt)*K,py0+(ph-nt)*K),(px0+(pw-nt)*K,py0+ph*K),(px0+nt*K,py0+ph*K),(px0+nt*K,py0+(ph-nt)*K),(px0,py0+(ph-nt)*K),(px0,py0+nt*K),(px0+nt*K,py0+nt*K)]
d.polygon([(x*S,y*S) for x,y in pts],fill=(20,100,60),outline=GRN,width=5*S//2)
# the ESP32-S3 Nano board in the wide central band, the connectors in the top strip, the MAX31865 chip and the drivers in the bottom strip
RR(px0+8*K,py0+13*K,px0+8*K+45*K,py0+13*K+18*K,4,fill=(28,28,34),outline=(200,200,205),width=2)
Tx(px0+8*K+22.5*K,py0+13*K+9*K,"ESP32-S3 Nano 45 x 18",F(14,True),(235,235,235))
for i in range(6): RR(px0+12*K+i*6.2*K,py0+2*K,px0+12*K+i*6.2*K+5*K,py0+2*K+6*K,2,fill=(40,100,170),outline=(15,50,110),width=2)
Tx(px0+31*K,py0+9.2*K,"borniers",F(11),(230,240,250))
RR(px0+12*K,py0+36*K,px0+12*K+6*K,py0+36*K+6*K,2,fill=(24,24,28)); Tx(px0+15*K,py0+39*K,"MAX",F(9,True),(220,220,225))
Tx(px0+15*K,py0+34.3*K,"MAX31865 (puce)",F(11),(230,240,230))
for i in range(3): RR(px0+26*K+i*6*K,py0+37*K,px0+26*K+i*6*K+4*K,py0+37*K+4*K,2,fill=(24,24,28))
Tx(px0+35*K,py0+34.3*K,"3 transistors",F(11),(230,240,230))
# mounting holes of the proposal on the 4 small standoffs
Tx(cx,by1+52,"carte proposée : 62 x 44 mm, coins découpés (10 x 10) pour les plots du couvercle,",F(20,True),GRN); Tx(cx,by1+80,"vissée sur les 4 petits plots (positions à relever au pied à coulisse)",F(20,True),GRN)
# dimensions
d.line([(bx0*S,(by0-40)*S),(bx1*S,(by0-40)*S)],fill=GRY,width=2*S); Tx(cx,by0-58,"≈ 71 mm (intérieur)",F(18),GRY)
d.line([((bx0-48)*S,by0*S),((bx0-48)*S,by1*S)],fill=GRY,width=2*S); Tx(bx0-70,cy,"≈ 52 mm",F(18),GRY)
# legend
lx=1000; 
Tx(lx,180,"Légende",F(24,True),INK,'lm')
E(lx-10,215,lx+10,235,fill=(30,30,34),outline=(110,110,118),width=2); Tx(lx+24,225,"gros plots d'angle : vis du couvercle",F(18),INK,'lm')
E(lx-10,255,lx+10,275,fill=(30,30,34),outline=(150,150,158),width=2); Tx(lx+24,265,"petits plots : fixation d'une carte (≈ 42 x 41 mm)",F(18),INK,'lm')
Tx(lx,330,"Profondeur de chaque moitié : environ 17 mm",F(18,True),INK,'lm')
Tx(lx,362,"(à vérifier : l'ESP32 sur ses supports",F(17),GRY,'lm'); Tx(lx,386,"+ le connecteur USB-C font environ 19 mm",F(17),GRY,'lm'); Tx(lx,410,"d'empilement : il faut les deux moitiés)",F(17),GRY,'lm')
Tx(lx,500,"Les 3 relais secteur ne rentrent pas",F(20,True),RED,'lm'); Tx(lx,436,"Le module MAX31865 (25 x 20) est trop large :",F(16),INK,'lm'); Tx(lx,456,"on soude la puce directement sur la carte.",F(16),INK,'lm')
Tx(lx,530,"sur cette carte : voir mes explications.",F(18),INK,'lm')
im=im.resize((W,H),Image.LANCZOS)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/box_fit.png'); print('ok')
