import math, sys
from PIL import Image, ImageDraw, ImageFont
base = Image.open(r'F:/Mes Documents/PlatformIO/Projects/261115-155749-nanoatmega328new/src/docs/images/steaming.png').convert('RGB')
W,H = base.size
OR=(255,186,107); CREAM=(254,245,228); BG=(33,16,2)
font = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 30)
small = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 26)
lab = ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf', 22)
cx=W//2

def wisps(d, x, y, h=70, color=OR, n=3, gap=24, w=5):
    # n wavy lines rising from (x,y) going up
    for i in range(n):
        xo = x + (i-(n-1)/2)*gap
        pts=[]
        for k in range(0,41):
            t=k/40
            yy = y - t*h*(1 if i!=1 else 1.15)
            xx = xo + math.sin(t*math.pi*2+i*1.2)*7
            pts.append((xx,yy))
        d.line(pts, fill=color, width=w, joint='curve')
        r=w/2
        for p in (pts[0],pts[-1]): d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r], fill=color)

def spaced(d, text, cxm, y, f, color, sp=6):
    widths=[d.textlength(c,font=f) for c in text]
    total=sum(widths)+sp*(len(text)-1)
    x=cxm-total/2
    for c,wc in zip(text,widths):
        d.text((x,y),c,font=f,fill=color); x+=wc+sp

def mk(name):
    im=base.copy(); return im, ImageDraw.Draw(im)

opts=[]
# A: text tag
im,d=mk('A'); spaced(d,'STEAM',cx,95,font,OR,8); opts.append(('A  Texte STEAM en haut',im))
# B: wisps above the number
im,d=mk('B'); wisps(d,cx+20,160,h=75); opts.append(('B  Volutes de vapeur au-dessus',im))
# C: wisps + text below
im,d=mk('C'); wisps(d,cx+20,150,h=60); spaced(d,'STEAM',cx,360,small,OR,8); opts.append(('C  Volutes + texte STEAM en bas',im))
# D: progress ring
im,d=mk('D')
R=H//2-14; frac=131/135
box=[cx-R,H//2-R,cx+R,H//2+R]
d.arc(box,0,360,fill=(70,45,20),width=9)
d.arc(box,-90,-90+360*frac,fill=OR,width=9)
wisps(d,cx+20,160,h=60,n=2,gap=22,w=4)
opts.append(('D  Anneau de progression + volutes',im))

pad=40
sheet=Image.new('RGB',(2*W+3*pad, 2*(H+pad+30)+pad),(24,24,28))
sd=ImageDraw.Draw(sheet)
for i,(t,im) in enumerate(opts):
    x=pad+(i%2)*(W+pad); y=pad+(i//2)*(H+pad+30)
    sd.text((x,y),t,font=lab,fill=(235,235,235))
    sheet.paste(im,(x,y+30))
sheet.save(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/steaming_options.png')
print(sheet.size)
