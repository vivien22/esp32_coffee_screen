# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
W,H=1800,1000
im=Image.new('RGB',(W,H),(250,250,247)); d=ImageDraw.Draw(im)
F=lambda s,b=False: ImageFont.truetype('C:/Windows/Fonts/%s.ttf'%('arialbd' if b else 'arial'),s)
INK=(30,30,36); RED=(200,40,40); GRN=(20,120,60); BLU=(30,90,170); GRY=(120,120,125)
def line(p,c=INK,w=5): d.line(p,fill=c,width=w)
def dot(x,y,r=9,c=INK): d.ellipse([x-r,y-r,x+r,y+r],fill=c)
def text(x,y,s,f=F(26),c=INK,a='la'): d.text((x,y),s,font=f,fill=c,anchor=a)
text(W//2,42,"Alimentation externe 5 V + USB : diode de protection",F(40,True),INK,'mm')
text(W//2,90,"La diode empêche le 5 V de l'USB de remonter dans l'alimentation externe",F(26),GRY,'mm')
yp=300; yg=800
# banner
d.rounded_rectangle([90,120,1000,172],14,outline=GRN,width=3,fill=(236,246,239))
text(545,146,"Sens de la diode : anode côté alimentation, cathode (trait) côté Nano",F(25,True),GRN,'mm')
# power supply
d.rounded_rectangle([90,230,330,870],16,outline=INK,width=5,fill=(255,255,255))
text(210,520,"Alimentation",F(30,True),INK,'mm'); text(210,558,"externe 5 V",F(30,True),INK,'mm'); text(210,598,"(2 A)",F(26),GRY,'mm')
text(316,yp-34,"V+",F(30,True),RED,'ra'); text(316,yg-34,"V−",F(30,True),INK,'ra')
dx0,dx1=940,1100
line([(330,yp),(dx0+35,yp)],RED,7)
line([(330,yg),(1220,yg)],INK,7)
text(350,yp-52,"+5 V externe (direct)",F(26,True),RED)
text(350,yg+14,"GND commun",F(26,True),INK)
# direct loads
jx=620
dot(jx,yp,10,RED); line([(jx,yp),(jx,420)],RED,6)
d.rounded_rectangle([jx-190,420,jx+190,640],16,outline=BLU,width=5,fill=(232,240,252))
text(jx,462,"Directement sur",F(26,True),BLU,'mm'); text(jx,498,"l'alimentation 5 V :",F(26,True),BLU,'mm')
text(jx,545,"écran GC9A01",F(26),INK,'mm'); text(jx,577,"capteurs de débit",F(26),INK,'mm'); text(jx,609,"MAX31865",F(26),INK,'mm')
line([(jx,640),(jx,yg)],INK,6); dot(jx,yg,10,INK)
# capacitor
cx=jx+250
line([(cx,yp),(cx,470)],RED,5); dot(cx,yp,9,RED)
line([(cx-34,470),(cx+34,470)],INK,6); line([(cx-34,496),(cx+34,496)],INK,6)
line([(cx,496),(cx,yg)],INK,5); dot(cx,yg,9,INK)
text(cx+48,468,"100 µF + 100 nF",F(24,True),INK); text(cx+48,498,"près de l'écran",F(22),GRY)
# diode
tx0=dx0+35; tx1=dx1-45
d.polygon([(tx0,yp-48),(tx0,yp+48),(tx1,yp)],outline=INK,fill=(255,235,200),width=5)
line([(tx1,yp-52),(tx1,yp+52)],INK,9)
line([(tx1,yp),(1220,yp)],RED,7)
text((dx0+dx1)//2+30,yp-122,"Diode Schottky",F(28,True),GRN,'mm'); text((dx0+dx1)//2+30,yp-90,"1N5819 ou SS14",F(26),GRN,'mm')
text(tx0-6,yp+62,"anode (+)",F(22),GRY,'ma'); text(tx1+8,yp+62,"cathode",F(22),GRY,'ma'); text(tx1+8,yp+86,"(trait)",F(22),GRY,'ma')
# Nano
nx0,nx1=1220,1500
d.rounded_rectangle([nx0,230,nx1,870],16,outline=INK,width=5,fill=(255,255,255))
dot(nx0,yp,9,RED)
text(nx0+14,yp-34,"5V",F(30,True),RED,'la'); text(nx0+14,yg-34,"GND",F(30,True),INK,'la')
text((nx0+nx1)//2,420,"sorties D4 / D5 / A3",F(24),GRY,'mm'); text((nx0+nx1)//2,452,"vers les entrées des SSR",F(24),GRY,'mm')
text((nx0+nx1)//2,520,"(la broche 5V alimente",F(24),GRY,'mm'); text((nx0+nx1)//2,552,"la Nano elle-même)",F(24),GRY,'mm')
text((nx0+nx1)//2,700,"Arduino Nano",F(32,True),INK,'mm')
# USB
d.rounded_rectangle([1590,420,1770,640],16,outline=BLU,width=5,fill=(232,240,252))
text(1680,480,"USB",F(34,True),BLU,'mm'); text(1680,525,"PC",F(28),BLU,'mm')
text(1680,570,"téléversement",F(21),GRY,'mm'); text(1680,596,"liaison série",F(21),GRY,'mm')
line([(nx1,560),(1590,560)],BLU,5)
# footer
d.rounded_rectangle([90,900,1710,968],14,outline=GRY,width=3,fill=(255,255,255))
text(900,934,"Chute de la diode : environ 0,3 V : la Nano voit environ 4,8 V. L'écran et les capteurs, branchés avant la diode, gardent le 5 V entier.",F(25),INK,'mm')
im.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/diode_schema.png')
print('ok')
