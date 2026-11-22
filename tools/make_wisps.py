import math
from PIL import Image, ImageDraw
W,H=36,40; S=8
im=Image.new('L',(W*S,H*S),0); d=ImageDraw.Draw(im)
def line(x0,top,bottom,phase,amp=3.2,lw=2.8):
    pts=[]
    n=80
    for k in range(n+1):
        t=k/n
        y=bottom-(bottom-top)*t
        x=x0+math.sin(t*math.pi*2+phase)*amp
        pts.append((x*S,y*S))
    d.line(pts,fill=255,width=int(lw*S),joint='curve')
    for p in (pts[0],pts[-1]):
        r=lw*S/2; d.ellipse([p[0]-r,p[1]-r,p[0]+r,p[1]+r],fill=255)
line(7,6,38,0.0)
line(18,1.5,38,1.2)
line(29,6,38,0.3)
sm=im.resize((W,H),Image.BOX)
px=[min(3,int(round(sm.getpixel((x,y))/255*3))) for y in range(H) for x in range(W)]
# print preview
for y in range(H): print(''.join(' .:#'[px[y*W+x]] for x in range(W)))
data=[]
for i in range(0,len(px),4):
    b=0
    for k in range(4):
        v=px[i+k] if i+k<len(px) else 0
        b|=v<<(6-2*k)
    data.append(b)
lines=[]
for i in range(0,len(data),12):
    lines.append('  '+', '.join('0x%02X'%b for b in data[i:i+12])+',')
out='#define ICON_STEAM_WIDTH %d\n#define ICON_STEAM_HEIGHT %d\nconst uint8_t ICON_STEAM[] PROGMEM = {\n%s\n};\n\n'%(W,H,'\n'.join(lines))
open(r'C:/Users/Vivien/AppData/Local/Temp/claude/9a374a450e84f4a0/9b614a51-daa0-4dfd-9a1e-6c27e3b84c8e/scratchpad/steam_icon.txt','w').write(out)
