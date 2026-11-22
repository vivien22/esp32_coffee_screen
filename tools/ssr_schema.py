from PIL import Image, ImageDraw, ImageFont
W,H=1800,1030
im=Image.new('RGB',(W,H),(250,250,247)); d=ImageDraw.Draw(im)
F=lambda s,b=False: ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s)
INK=(30,30,36); RED=(200,40,40); GRN=(20,120,60); BLU=(30,90,170); GRY=(120,120,125)
def line(p,c=INK,w=4): d.line(p,fill=c,width=w)
def dot(x,y,r=8,c=INK): d.ellipse([x-r,y-r,x+r,y+r],fill=c)
def text(x,y,s,f=F(26),c=INK,anchor='la'): d.text((x,y),s,font=f,fill=c,anchor=anchor)
d.text((W//2,40),"Commande d'un SSR par transistor (un montage par SSR)",font=F(40,True),fill=INK,anchor='mm')
d.text((W//2,88),"Le firmware ne change pas : la sortie reste active à l'état haut",font=F(26),fill=GRY,anchor='mm')

# rails
y5=170; yg=840
line([(120,y5),(1000,y5)],RED,6); text(120,y5-48,"+5 V  (broche 5V de la Nano)",F(28,True),RED)
line([(120,yg),(1000,yg)],INK,6); text(120,yg+14,"GND  (commun : Nano, transistors, entrées des SSR)",F(28,True),INK)

# SSR input block
sx,sy,sw,sh=662,270,200,150
d.rounded_rectangle([sx,sy,sx+sw,sy+sh],14,outline=BLU,width=5,fill=(232,240,252))
text(sx+sw//2,sy+sh//2-18,"ENTRÉE",F(30,True),BLU,'mm'); text(sx+sw//2,sy+sh//2+22,"du SSR",F(28),BLU,'mm')
text(sx+sw+14,sy-4,"+",F(40,True),RED); text(sx+sw+14,sy+sh-36,"−",F(40,True),INK)
# + to 5V
line([(sx+sw//2,y5),(sx+sw//2,sy)],RED,5); dot(sx+sw//2,y5,9,RED)
# - to collector
qx=740 ; qy=620  # transistor centre
line([(sx+sw//2,sy+sh),(sx+sw//2,qy-90)],INK,5)

# NPN transistor: circle centre (qx,qy) r=70
r=70
d.ellipse([qx-r,qy-r,qx+r,qy+r],outline=INK,width=5)
# base bar
line([(qx-30,qy-42),(qx-30,qy+42)],INK,7)
# base lead
line([(qx-30,qy),(qx-r-130,qy)],INK,5)
# collector / emitter
line([(qx-30,qy-18),(qx+22,qy-58)],INK,5); line([(qx+22,qy-58),(qx+22,qy-r-20)],INK,5)
line([(qx-30,qy+18),(qx+22,qy+58)],INK,5); line([(qx+22,qy+58),(qx+22,yg)],INK,5)
# arrow on emitter
d.polygon([(qx+22,qy+58),(qx+2,qy+50),(qx+14,qy+36)],fill=INK)
# collector wire to ssr minus (qx+22 vs sx+sw//2=740)
# adjust: make both x equal 762
line([(sx+sw//2,qy-90),(qx+22,qy-90)],INK,5)
text(qx+60,qy-100,"collecteur",F(24),GRY); text(qx+60,qy+70,"émetteur",F(24),GRY); text(qx-118,qy-40,"base",F(24),GRY)
dot(qx+22,yg,9,INK)

# base resistor 1k from pin
bx=qx-r-130
def res(x1,y1,x2,y2,label,lx,ly):
    d.rectangle([min(x1,x2)-0,min(y1,y2)-18,max(x1,x2),max(y1,y2)+18],outline=INK,width=4,fill=(255,255,255))
    text(lx,ly,label,F(26,True),INK,'mm')
# horizontal 1k: from x=330 to x=450 at y=qy
line([(300,qy),(360,qy)],INK,5); res(360,qy,500,qy,"1 kΩ",430,qy-40); line([(500,qy),(qx-30,qy)],INK,5)
# pin label
dot(300,qy,9,GRN); text(300,qy+24,"D4 (pompe)",F(28,True),GRN,'ma'); text(300,qy+58,"D5 (chaudière)",F(28,True),GRN,'ma'); text(300,qy+92,"A3 (vanne)",F(28,True),GRN,'ma')
# pull-down 10k from base to GND
px=560
dot(px,qy,8,INK)
line([(px,qy),(px,qy+60)],INK,5)
d.rectangle([px-18,qy+60,px+18,qy+150],outline=INK,width=4,fill=(255,255,255)); text(px+30,qy+105,"10 kΩ",F(26,True),INK,'lm')
line([(px,qy+150),(px,yg)],INK,5); dot(px,yg,9,INK)
text(px-8,qy+190,"(maintient le SSR éteint au démarrage)",F(22),GRY,'rt') if False else None

# annotation right
ax=1090
d.rounded_rectangle([ax,150,W-40,560],16,outline=GRN,width=4,fill=(236,246,239))
lines=[("Ce que ça change",True,GRN),("",False,INK),("Avant :  broche → entrée du SSR",False,INK),("   tension mesurée ≈ 3,4 V",False,RED),("   (juste au seuil du SSR)",False,RED),("",False,INK),("Après : le SSR est alimenté par",False,INK),("   le 5 V, le transistor commute",False,INK),("   tension d'entrée ≈ 4,8 V",False,GRN),("   la broche ne fournit que ~5 mA",False,GRN)]
y=170
for s,b,c in lines:
    text(ax+24,y,s,F(27,b),c); y+=36
d.rounded_rectangle([ax,590,W-40,900],16,outline=BLU,width=4,fill=(232,240,252))
lines=[("Composants (x3)",True,BLU),("",False,INK),("1 transistor NPN : 2N2222 ou BC337",False,INK),("  (ou MOSFET logique 2N7000)",False,INK),("1 résistance 1 kΩ  (base)",False,INK),("1 résistance 10 kΩ (base → GND)",False,INK),("Pas de diode : l'entrée d'un SSR",False,INK),("n'est pas inductive.",False,INK)]
y=610
for s,b,c in lines:
    text(ax+24,y,s,F(27,b),c); y+=32
# footnote
text(120,yg+70,"Un montage identique pour chacun des trois SSR : pompe (D4), chaudière (D5), vanne (A3).",F(24),GRY)
text(120,yg+104,"Les masses restent communes. Charges des SSR (secteur / pompe DC) : inchangées.",F(24),GRY)
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/ssr_drive_schema.png')
print('ok')
