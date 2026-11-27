from PIL import Image
import numpy as np, sys, os
from scipy import ndimage
from collections import deque
def run(path,names,H=0.38):
    A=np.array(Image.open(path).convert('RGBA')); al=A[:,:,3]; cs=1024//3; meta=[]
    for i,nm in enumerate(names):
        r,c=divmod(i,3); x0,y0=c*cs,r*cs; cx,cy=x0+cs//2,y0+cs//2
        # nearest transparent pixel to center as seed
        if al[cy,cx]>=40:
            ys,xs=np.where(al[y0+100:y0+cs-100,x0+100:x0+cs-100]<40); k=np.argmin((ys+100-cs//2)**2+(xs+100-cs//2)**2); cy,cx=y0+100+ys[k],x0+100+xs[k]
        seen=np.zeros(al.shape,bool); q=deque([(cy,cx)]); seen[cy,cx]=1; P=[]
        while q:
            y,x=q.popleft(); P.append((y,x))
            for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)):
                ny,nx=y+dy,x+dx
                if y0<=ny<y0+cs and x0<=nx<x0+cs and not seen[ny,nx] and al[ny,nx]<40: seen[ny,nx]=1; q.append((ny,nx))
        P=np.array(P); (hy0,hx0),(hy1,hx1)=P.min(0),P.max(0); meta.append((nm,(hx0+hx1)/2,(hy0+hy1)/2,min(hx1-hx0,hy1-hy0)))
    Y,X=np.mgrid[0:1024,0:1024]; own=np.stack([(X-m[1])**2+(Y-m[2])**2 for m in meta]).argmin(0); lab,n=ndimage.label(al>12)
    for i,(nm,hcx,hcy,hd) in enumerate(meta):
        vor=own==i; keep=np.zeros_like(vor)
        for k in np.unique(lab[vor&(lab>0)]):
            m=lab==k; keep |= m if (m&vor).sum()/m.sum()>0.8 else (m&vor)
        B=A.copy(); B[~keep,3]=0; S=hd/H; box=(int(hcx-S/2),int(hcy-S/2),int(hcx+S/2),int(hcy+S/2))
        ys,xs=np.where(keep&(al>12)); clip=xs.min()<box[0] or ys.min()<box[1] or xs.max()>box[2] or ys.max()>box[3]
        out=np.array(Image.fromarray(B).crop(box).resize((256,256),Image.LANCZOS))
        l2,n2=ndimage.label(out[:,:,3]>3); sz=ndimage.sum(out[:,:,3]>3,l2,range(1,n2+1)); Yy,Xx=np.mgrid[0:256,0:256]; rm=0
        for k in range(n2):
            m=l2==k+1
            if sz[k]<sz.max()*0.03:
                d=((Xx[m].mean()-128)**2+(Yy[m].mean()-128)**2)**.5
                # stray from neighbour sits near canvas edge
                if d>100: out[m,3]=0; rm+=1
        Image.fromarray(out).save(f'out/frm_{nm}.webp',quality=90,method=6)
        print(nm,'hole',int(hd),'clip' if clip else 'ok','stray',rm)
run(sys.argv[1],sys.argv[2].split(','))
