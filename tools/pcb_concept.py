# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
W,H=1800,1100
im=Image.new('RGB',(W,H),(246,246,242)); d=ImageDraw.Draw(im)
F=lambda s,b=False: ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s)
INK=(30,30,36); GRN=(22,110,70); BLU=(30,90,170); RED=(190,40,40); ORG=(200,120,20); GRY=(120,120,125)
def T(x,y,s,f=F(24),c=INK,a='la'): d.text((x,y),s,font=f,fill=c,anchor=a)
T(W//2,40,"ESP32-S3 : concept de carte (basse tension uniquement, aucun secteur sur la carte)",F(38,True),INK,'mm')
T(W//2,86,"Carte d'environ 80 x 60 mm, 2 couches avec plan de masse. Les connecteurs sont sur les bords, l'antenne dépasse en haut.",F(24),GRY,'mm')
# board
bx0,by0,bx1,by1=330,200,1130,900
d.rounded_rectangle([bx0,by0,bx1,by1],24,outline=GRN,width=7,fill=(214,235,222))
# ESP32 module with antenna keep-out
d.rectangle([560,130,900,290],outline=RED,width=3,fill=(250,230,230))
T(730,185,"zone antenne",F(24,True),RED,'mm'); T(730,220,"pas de cuivre dessous",F(20),RED,'mm')
d.rectangle([590,290,870,520],outline=INK,width=5,fill=(50,50,58))
T(730,365,"ESP32-S3",F(30,True),(240,240,240),'mm'); T(730,405,"WROOM-1",F(24),(220,220,225),'mm'); T(730,445,"module, 3,3 V",F(20),(200,200,205),'mm')
def blk(x0,y0,x1,y1,title,sub,c=BLU,fill=(232,240,252)):
    d.rounded_rectangle([x0,y0,x1,y1],10,outline=c,width=4,fill=fill)
    T((x0+x1)//2,(y0+y1)//2-14,title,F(23,True),c,'mm'); T((x0+x1)//2,(y0+y1)//2+18,sub,F(17),INK,'mm')
blk(360,560,560,690,"Alimentation","LDO 3,3 V, 1 A",ORG,(252,240,222))
blk(360,300,560,430,"Protection","diode, fusible, TVS",ORG,(252,240,222))
blk(600,560,820,690,"MAX31865","RREF 430 Ω",BLU)
blk(840,560,1100,690,"Pilotes SSR (x3)","3 transistors, 5 V",GRN,(228,244,232))
blk(900,300,1100,430,"Entrées capteurs","niveau 5 V → 3,3 V",GRN,(228,244,232))
blk(360,720,560,860,"USB-C natif","programmation",BLU)
blk(600,720,820,860,"BOOT / RESET","+ LED d'état",BLU)
blk(840,720,1100,860,"Entrées commande","encodeur, bouton start",BLU)
# connectors on edges
def conn(x,y,w,h,label,sub,c=INK):
    d.rectangle([x,y,x+w,y+h],outline=c,width=4,fill=(255,255,255)); T(x+w//2,y+h//2-12,label,F(20,True),c,'mm'); T(x+w//2,y+h//2+16,sub,F(16),GRY,'mm')
# left edge
conn(90,230,230,90,"J1  5 V / GND","borne à vis")
conn(90,350,230,110,"J2  SSR x3","pompe, chaudière, vanne")
conn(90,490,230,100,"J3  débit In / Out","5 V, GND, signal x2")
# right edge
conn(1150,230,320,100,"J4  écran GC9A01","SPI + DC, RST, BL")
conn(1150,360,320,90,"J5  encodeur","A, B, GND (+ bouton)")
conn(1150,480,320,90,"J6  bouton start","+ entrée libre")
conn(1150,600,320,100,"J7  PT100","2, 3 ou 4 fils")
# bottom
conn(360,930,200,80,"USB-C","bord bas")
# arrows (lines to edges)
for (y,xa) in [(275,310),(405,310),(540,310)]:
    d.line([(310,y),(360,y)],fill=ORG if y<300 else GRN,width=4)
for (y) in [280,405,525,650]:
    d.line([(1100,y),(1150,y)],fill=BLU,width=4)
# legend on the side
T(1160,740,"Choix de conception",F(26,True),INK)
lines=["• Les 3 SSR sont commandés par transistor",
       "  depuis le 5 V (pas directement par les",
       "  3,3 V de l'ESP32, trop justes).",
       "• Résistance de rappel à 0 V sur chaque",
       "  sortie : relais éteints au démarrage.",
       "• Entrée capteurs : diviseur + trigger de",
       "  Schmitt (le 5 V ne touche pas l'ESP32)."]
y=780
for s in lines:
    T(1160,y,s,F(21),INK); y+=30
T(W//2,1060,"Le secteur reste hors de la carte : les SSR et leurs charges sont câblés ailleurs, la carte ne manipule que du 5 V.",F(24,True),RED,'mm')
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/pcb_esp32s3_concept.png')
print('ok')
