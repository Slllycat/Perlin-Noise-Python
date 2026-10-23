import math
import tkinter as tk

zoom=5#how far zoomed out           #5          10
depth=10#how many maps              #10         20
cl=1#0 for no color 1 for color     #1/0        1/0
biggnes=4#visuel size               #4          2
size=200#pixels                     #200        400
delay =1#let this be ;D

#window setup
window = tk.Tk()
window.title("Fuff")
window.geometry(str(size * biggnes) + "x" + str(size * biggnes))
canvas = tk.Canvas(window, width=(size * biggnes), height=(size * biggnes), bg="black")
canvas.pack()

def rad(s):
    import random
    rad=[]
    for _ in range(s**2):
        rad.append(math.radians(random.randint(0,359)))
    return rad

def fade(t):
    return t*t*t*(t*(t*6-15)+10)

def dotp(x,y,v,s):
    i=math.floor(x)+math.floor(y)*(s+1)
    xs,ys=x%1,y%1
    a=v[i]
    dx=-xs*math.cos(a)
    dy=-ys*math.sin(a)
    d1=dx+dy

    a=v[i+1]
    dx=(1-xs)*math.cos(a)
    dy=-ys*math.sin(a)
    d2=dx+dy

    a=v[i+(s+1)]
    dx=-xs*math.cos(a)
    dy=(1-ys)*math.sin(a)
    d3=dx+dy

    a=v[i+(s + 1)+1]
    dx=(1-xs)*math.cos(a)
    dy=(1-ys)*math.sin(a)
    d4=dx+dy
    u = fade(xs)
    v2 = fade(ys)
    lx1=(1-u)*d1+u*d2
    lx2=(1-u)*d3+u*d4
    l=(1-v2)*lx1+v2*lx2
    return l

def perlinpoint(x,y,v,s):
    p=dotp(x,y,v,s)
    return p


def perlinnoise(vsize,asize):
    v=rad(vsize+1)
    points=[]
    x,y=0,0
    for _ in range(asize):
        for _ in range(asize):
            points.append(perlinpoint(x,y,v,vsize))
            x+=(vsize/asize)
        x=0
        y+=(vsize/asize)
    return points

def multiperlinnoise(vsize,asize,depth):
    creat=0.5   # persistence
    amp=1.0
    vs=vsize
    points=[]
    for i in range(depth):
        v=rad(vsize+1)
        a=0
        x,y=0,0
        for _ in range(asize):
            for _ in range(asize):
                p = perlinpoint(x, y, v, vsize) * amp
                if i ==0:
                    points.append(p)
                else:
                    points[a] += p
                x+=(vsize/asize)
                a+=1
            x=0
            y+=(vsize/asize)
        vsize = vs*(i+2) # higher frequency
        amp *= creat                # lower strength
    return points

def valuetocolor(v,cl): #bleb RGB
    if cl==True:
        if v <= 0:
            c = int((v + 1) * 255)
            return f"#{0:02x}{0:02x}{c:02x}"
        elif v<0.1:
            c = int((v+0.1)*5*255)
            return f"#{c:02x}{c:02x}{0:02x}"
        else:
            c = int(255-(v* 255))
            return f"#{0:02x}{c:02x}{0:02x}"
    else:
        gray = int((v + 1) / 2 * 255)
        return f"#{gray:02x}{gray:02x}{gray:02x}"


a=multiperlinnoise(zoom,size,depth)
x,y,weg=0,0,0
for _ in range(size):
    for _ in range(size):
        color=valuetocolor(a[weg],cl)
        canvas.create_rectangle(x, y, x + biggnes, y + biggnes,fill=color, outline=color)
        x+=biggnes
        weg+=1
    y+=biggnes
    x=0

window.mainloop()